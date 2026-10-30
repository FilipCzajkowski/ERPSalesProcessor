"""
Validator Module
Implements business validation logic including Polish NIP checksum algorithm,
dates consistency, and VAT calculation verification.
"""

from datetime import datetime
import re
from typing import Optional, Tuple


def validate_polish_nip(nip_raw: str) -> bool:
    """
    Validates Polish Tax Identification Number (NIP) using standard modulo-11 checksum.
    Weights: 6, 5, 7, 2, 3, 4, 5, 6, 7.
    """
    if not nip_raw or not isinstance(nip_raw, str):
        return False

    # Strip dashes, spaces, and country prefix (e.g. 'PL')
    clean_nip = re.sub(r"[^0-9]", "", nip_raw)

    if len(clean_nip) != 10 or len(set(clean_nip)) == 1:
        return False

    weights = [6, 5, 7, 2, 3, 4, 5, 6, 7]
    try:
        digits = [int(ch) for ch in clean_nip]
    except ValueError:
        return False

    checksum = sum(w * d for w, d in zip(weights, digits[:9])) % 11

    # Checksum 10 is invalid according to Polish Ministry of Finance specifications
    if checksum == 10:
        return False

    return checksum == digits[9]


def parse_and_validate_date(date_str: str) -> Optional[datetime]:
    """
    Parses date strings commonly encountered in Polish ERP exports:
    Supported formats: YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY, YYYY/MM/DD.
    """
    if not date_str or not isinstance(date_str, str):
        return None

    cleaned = date_str.strip()
    formats = ["%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%Y/%m/%d"]

    for fmt in formats:
        try:
            return datetime.strptime(cleaned, fmt)
        except ValueError:
            continue
    return None


def verify_vat_math(
    netto: float, vat_rate: float, brutto: float, tolerance: float = 0.05
) -> Tuple[bool, float]:
    """
    Verifies that Brutto = Netto * (1 + vat_rate).
    Returns (is_valid, expected_brutto).
    """
    expected_vat = round(netto * (vat_rate / 100.0), 2)
    expected_brutto = round(netto + expected_vat, 2)
    difference = abs(expected_brutto - brutto)
    return (difference <= tolerance, expected_brutto)
