"""
Unit tests for ERPSalesProcessor validator module
"""

import pytest
from processor.validator import validate_polish_nip, parse_and_validate_date, verify_vat_math


def test_valid_polish_nips():
    """Validates real Polish entity NIP numbers."""
    # Comarch S.A.: 677-00-65-406
    assert validate_polish_nip("6770065406") is True
    assert validate_polish_nip("PL 677-00-65-406") is True

    # Asseco Poland S.A.: 522-00-03-782
    assert validate_polish_nip("5220003782") is True

    # Politechnika Lubelska: 712-010-46-51
    assert validate_polish_nip("7120104651") is True


def test_invalid_polish_nips():
    """Rejects invalid, malformed, or fake NIP numbers."""
    assert validate_polish_nip("1234567890") is False  # Invalid checksum
    assert validate_polish_nip("0000000000") is False  # Invalid checksum
    assert validate_polish_nip("12345") is False       # Too short
    assert validate_polish_nip("") is False            # Empty
    assert validate_polish_nip(None) is False          # None


def test_date_parser_formats():
    """Tests parsing of various Polish ERP date formats."""
    d1 = parse_and_validate_date("2026-10-15")
    assert d1 is not None and d1.year == 2026 and d1.month == 10 and d1.day == 15

    d2 = parse_and_validate_date("15.10.2026")
    assert d2 is not None and d2.year == 2026 and d2.month == 10 and d2.day == 15

    d3 = parse_and_validate_date("15/10/2026")
    assert d3 is not None and d3.year == 2026 and d3.month == 10 and d3.day == 15

    assert parse_and_validate_date("invalid-date-string") is None


def test_vat_math_verification():
    """Tests accuracy of VAT and Brutto recalculation."""
    is_valid, expected_brutto = verify_vat_math(netto=100.0, vat_rate=23.0, brutto=123.0)
    assert is_valid is True
    assert expected_brutto == 123.0

    is_valid_mismatch, _ = verify_vat_math(netto=100.0, vat_rate=23.0, brutto=150.0)
    assert is_valid_mismatch is False
