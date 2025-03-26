"""
Tests for utility functions.
"""

import pytest
import json
import logging
from pathlib import Path
from data_wizard.utils import (
    validate_file_path,
    save_json_report,
    format_number,
    ensure_directory
)

@pytest.fixture
def temp_csv(tmp_path):
    """Create a temporary CSV file."""
    file_path = tmp_path / "test.csv"
    file_path.write_text("a,b,c\n1,2,3")
    return str(file_path)

@pytest.fixture
def temp_json(tmp_path):
    """Create a temporary JSON file path."""
    return str(tmp_path / "test.json")

def test_validate_file_path_valid(temp_csv):
    """Test file path validation with valid file."""
    assert validate_file_path(temp_csv) is True

def test_validate_file_path_nonexistent():
    """Test file path validation with non-existent file."""
    assert validate_file_path("nonexistent.csv") is False

def test_validate_file_path_wrong_extension(tmp_path):
    """Test file path validation with wrong extension."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("test")
    assert validate_file_path(str(file_path)) is False

def test_save_json_report(temp_json):
    """Test saving JSON report."""
    data = {"test": "value", "number": 42}
    save_json_report(data, temp_json)
    
    # Verify file contents
    with open(temp_json, 'r', encoding='utf-8') as f:
        loaded_data = json.load(f)
    
    assert loaded_data == data

def test_save_json_report_unicode(temp_json):
    """Test saving JSON report with Unicode characters."""
    data = {"test": "值", "number": 42}
    save_json_report(data, temp_json)
    
    with open(temp_json, 'r', encoding='utf-8') as f:
        loaded_data = json.load(f)
    
    assert loaded_data == data

def test_save_json_report_invalid_path():
    """Test saving JSON report to invalid path."""
    data = {"test": "value"}
    with pytest.raises(Exception):
        save_json_report(data, "/nonexistent/path/file.json")

@pytest.mark.parametrize("value,decimals,expected", [
    (3.14159, 2, "3.14"),
    (42.0, 0, "42"),
    (1.23456, 3, "1.235"),
    (0, 2, "0.00"),
])
def test_format_number(value, decimals, expected):
    """Test number formatting with various inputs."""
    assert format_number(value, decimals) == expected

def test_format_number_invalid():
    """Test number formatting with invalid input."""
    assert format_number("not a number") == "not a number"

def test_ensure_directory(tmp_path):
    """Test directory creation."""
    test_dir = tmp_path / "test_dir" / "nested"
    ensure_directory(str(test_dir))
    assert test_dir.exists()
    assert test_dir.is_dir()

def test_ensure_directory_exists(tmp_path):
    """Test ensuring existing directory."""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    ensure_directory(str(test_dir))  # Should not raise
    assert test_dir.exists()

def test_ensure_directory_invalid():
    """Test ensuring directory with invalid path."""
    with pytest.raises(Exception):
        ensure_directory("/nonexistent/path/that/should/fail") 