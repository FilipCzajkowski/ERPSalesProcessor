# 📊 ERPSalesProcessor

> **Enterprise Invoicing Pipeline & Data Quality Auditor for ERP Systems (Comarch Optima / SAP)**  
> Built for Data Analysts, ERP System Assistants, and Python Automation Engineers.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Excel](https://img.shields.io/badge/OpenPyXL-Executive_Spreadsheets-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📌 Overview

**ERPSalesProcessor** is a robust, modular Python pipeline designed to ingest, clean, validate, and audit messy sales and invoice data exported from ERP systems (such as Comarch ERP Optima, Subiekt, or SAP).

In business environments, raw ERP exports frequently suffer from human error: inconsistent date notations, formatting flaws, duplicate invoice entries, and invalid tax identification numbers. This tool automates the entire audit lifecycle and produces an executive-ready, multi-tab Excel workbook.

---

## 🚀 Key Features

- 🇵🇱 **Official Polish NIP Checksum Validation:** Algorithmic verification of Polish Tax Identification Numbers (NIP) using standard Ministry of Finance Modulo-11 weights (`[6, 5, 7, 2, 3, 4, 5, 6, 7]`).
- 🧹 **Automated Deduplication & Cleaning:** Strips whitespace, standardizes column headers, and eliminates duplicate invoices.
- 📅 **Smart Date Parser:** Unifies mixed date formats (`YYYY-MM-DD`, `DD.MM.YYYY`, `DD/MM/YYYY`) into standard ISO format.
- 🧮 **VAT Mathematical Verification:** Verifies Netto + VAT = Brutto calculations and recalculates variances.
- 📈 **Executive Multi-Tab Excel Workbook:**
  - **Executive Summary:** Clean KPI metrics (total turnover, VAT collected, invalid tax IDs detected, and top 5 contractors by revenue).
  - **Audited Invoices:** Fully formatted table with currency formatting (`#,##0.00 zł`), color-coded audit status flags, and auto-adjusted column widths.
- 🧪 **Comprehensive Unit Test Suite:** Powered by `pytest` ensuring 100% calculation and validation fidelity.

---

## 🛠️ Project Structure

```text
ERPSalesProcessor/
├── processor/
│   ├── __init__.py
│   ├── validator.py           # NIP checksum algorithm, date parser & VAT math
│   ├── cleaner.py             # Data ingestion, deduplication, schema normalization
│   └── excel_reporter.py      # Styled openpyxl workbook generator with KPI cards
├── sample_data/
│   └── invoices_raw.csv       # Benchmark raw dataset with dirty entries
├── tests/
│   └── test_validator.py      # Pytest unit tests for business validation rules
├── main.py                    # CLI entry point with logging
├── requirements.txt           # Project dependencies
└── README.md
```

---

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/FilipCzajkowski/ERPSalesProcessor.git
   cd ERPSalesProcessor
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage Examples

### 1. Run Pipeline with Default Sample Data
Processes `sample_data/invoices_raw.csv` and outputs `sales_audit_report.xlsx`:
```bash
python main.py
```

### 2. Process Custom Export File with Custom Output Name
```bash
python main.py --input path/to/my_invoices.csv --output monthly_report_october.xlsx
```

### 3. Verbose Mode with Debug Logging
```bash
python main.py --verbose
```

---

## 🧪 Running Unit Tests

Execute the unit tests via `pytest`:
```bash
pytest -v
```

---

## 👤 Author

**Filip Czajkowski**
- LinkedIn: [linkedin.com/in/CzajkowskiFilip](https://linkedin.com/in/CzajkowskiFilip)
- GitHub: [@FilipCzajkowski](https://github.com/FilipCzajkowski)
- Email: `CzajkowskiFilip@proton.me`

---

## 📄 License
This project is licensed under the MIT License.
