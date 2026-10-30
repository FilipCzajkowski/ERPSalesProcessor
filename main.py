"""
ERPSalesProcessor - Main CLI Entry Point
Author: Filip Czajkowski
"""

import argparse
import logging
import sys
from pathlib import Path

# Ensure UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

from processor.cleaner import clean_erp_dataset
from processor.excel_reporter import generate_styled_excel_report


def setup_logger(verbose: bool = False) -> logging.Logger:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)-8s %(message)s",
        datefmt="%H:%M:%S",
        level=level,
    )
    return logging.getLogger("ERPSalesProcessor")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ERPSalesProcessor",
        description="📊 Enterprise Sales & Invoice Data Processing Pipeline (ERP / Comarch Optima)",
    )
    parser.add_argument(
        "-i", "--input",
        type=str,
        default="sample_data/invoices_raw.csv",
        help="Path to raw invoice data file (CSV or XLSX)",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="sales_audit_report.xlsx",
        help="Path to destination formatted Excel report (default: sales_audit_report.xlsx)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose debugging logs",
    )

    args = parser.parse_args()
    logger = setup_logger(args.verbose)

    input_file = Path(args.input)
    if not input_file.exists():
        logger.error(f"Input file not found: {args.input}")
        sys.exit(1)

    logger.info("======================================================")
    logger.info("Starting ERP Invoicing Pipeline Processing")
    logger.info(f"Source file: {input_file.resolve()}")
    logger.info("======================================================")

    # 1. Clean and validate dataset
    try:
        clean_df, metrics = clean_erp_dataset(str(input_file))
    except Exception as e:
        logger.error(f"Failed to process dataset: {e}", exc_info=args.verbose)
        sys.exit(1)

    logger.info(f"Ingested {metrics['initial_rows']} raw records.")
    logger.info(f"Removed {metrics['duplicates_removed']} duplicate records.")
    logger.info(f"Detected {metrics['invalid_nips']} invalid tax identification numbers (NIP).")
    logger.info(f"Total Clean Netto Revenue: {metrics['total_revenue_netto']:,.2f} PLN")
    logger.info(f"Total Turnover Brutto:     {metrics['total_revenue_brutto']:,.2f} PLN")

    # 2. Generate executive Excel report
    output_path = Path(args.output)
    logger.info(f"Generating formatted multi-sheet Excel workbook -> {output_path.name}")
    try:
        generate_styled_excel_report(clean_df, metrics, str(output_path))
        logger.info(f"✅ Report successfully saved at: {output_path.resolve()}")
    except Exception as e:
        logger.error(f"Failed to create Excel report: {e}", exc_info=args.verbose)
        sys.exit(1)


if __name__ == "__main__":
    main()
