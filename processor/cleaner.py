"""
Cleaner Module
Standardizes dirty ERP datasets, removes duplicates, validates business records.
"""

from typing import Dict, Any, Tuple
import pandas as pd
from .validator import validate_polish_nip, parse_and_validate_date, verify_vat_math


def clean_erp_dataset(input_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Ingests raw sales/invoice export, standardizes schema, and validates integrity.
    """
    # 1. Load data
    if input_path.endswith(".csv"):
        df = pd.read_csv(input_path, dtype=str)
    else:
        df = pd.read_excel(input_path, dtype=str)

    initial_row_count = len(df)

    # 2. Normalize column headers
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Required columns check
    expected_cols = ["invoice_number", "contractor_name", "nip", "issue_date", "netto", "vat_rate"]
    for col in expected_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required ERP column in dataset: '{col}'")

    # 3. Clean string values
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    # 4. Remove duplicate invoices
    df = df.drop_duplicates(subset=["invoice_number"], keep="first").copy()
    duplicates_removed = initial_row_count - len(df)

    # 5. Validate & Standardize NIP
    df["nip_clean"] = df["nip"].str.replace(r"[^0-9]", "", regex=True)
    df["is_nip_valid"] = df["nip_clean"].apply(validate_polish_nip)

    # 6. Standardize Dates
    parsed_dates = df["issue_date"].apply(parse_and_validate_date)
    df["standard_issue_date"] = parsed_dates.apply(lambda d: d.strftime("%Y-%m-%d") if d else "INVALID_DATE")

    # 7. Convert & verify financial figures
    df["netto"] = df["netto"].str.replace(",", ".").astype(float)
    df["vat_rate"] = df["vat_rate"].str.replace("%", "").str.replace(",", ".").astype(float)

    if "brutto" in df.columns:
        df["brutto"] = df["brutto"].str.replace(",", ".").astype(float)
    else:
        # Compute brutto if omitted in raw export
        df["brutto"] = (df["netto"] * (1 + df["vat_rate"] / 100.0)).round(2)

    df["vat_amount"] = (df["brutto"] - df["netto"]).round(2)

    # 8. Mark row validation status
    def determine_row_status(row) -> str:
        issues = []
        if not row["is_nip_valid"]:
            issues.append("INVALID_NIP")
        if row["standard_issue_date"] == "INVALID_DATE":
            issues.append("INVALID_DATE")
        return "OK" if not issues else " | ".join(issues)

    df["audit_status"] = df.apply(determine_row_status, axis=1)

    metrics = {
        "initial_rows": initial_row_count,
        "clean_rows": len(df),
        "duplicates_removed": duplicates_removed,
        "invalid_nips": int((~df["is_nip_valid"]).sum()),
        "total_revenue_netto": round(float(df["netto"].sum()), 2),
        "total_vat": round(float(df["vat_amount"].sum()), 2),
        "total_revenue_brutto": round(float(df["brutto"].sum()), 2),
    }

    return df, metrics
