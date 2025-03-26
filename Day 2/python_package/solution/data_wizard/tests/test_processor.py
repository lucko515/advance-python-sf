"""
Tests for the DataProcessor class.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from data_wizard.processor import DataProcessor

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        'id': [1, 2, 2, 3, 4],
        'value': [10.0, 20.0, 20.0, None, 40.0],
        'category': ['A', 'B', 'B', 'C', 'D']
    })

@pytest.fixture
def temp_csv(tmp_path, sample_data):
    """Create a temporary CSV file with sample data."""
    file_path = tmp_path / "test.csv"
    sample_data.to_csv(file_path, index=False)
    return str(file_path)

def test_init_with_file(temp_csv):
    """Test initialization with file path."""
    processor = DataProcessor(temp_csv)
    assert processor.data is not None
    assert len(processor.data) == 5

def test_init_without_file():
    """Test initialization without file path."""
    processor = DataProcessor()
    assert processor.data is None

def test_load_csv(temp_csv):
    """Test loading CSV file."""
    processor = DataProcessor()
    processor.load_csv(temp_csv)
    assert len(processor.data) == 5
    assert list(processor.data.columns) == ['id', 'value', 'category']

def test_load_csv_invalid_path():
    """Test loading non-existent CSV file."""
    processor = DataProcessor()
    with pytest.raises(ValueError):
        processor.load_csv("nonexistent.csv")

def test_clean_data(sample_data):
    """Test data cleaning functionality."""
    processor = DataProcessor()
    processor.data = sample_data.copy()
    
    processor.clean_data(drop_duplicates=True, fill_numeric=True)
    
    assert len(processor.data) == 4  # One duplicate removed
    assert not processor.data['value'].isnull().any()  # No null values
    assert processor.data['value'].iloc[2] == 22.5  # Mean value filled

def test_filter_by_column(sample_data):
    """Test column filtering."""
    processor = DataProcessor()
    processor.data = sample_data.copy()
    
    processor.filter_by_column('value', lambda x: x > 20)
    assert len(processor.data) == 1
    assert processor.data['value'].iloc[0] == 40.0

def test_save_csv(tmp_path, sample_data):
    """Test saving to CSV."""
    processor = DataProcessor()
    processor.data = sample_data.copy()
    
    output_path = tmp_path / "output.csv"
    processor.save_csv(str(output_path))
    
    assert output_path.exists()
    loaded_data = pd.read_csv(output_path)
    pd.testing.assert_frame_equal(loaded_data, sample_data)

def test_get_summary(sample_data):
    """Test summary statistics generation."""
    processor = DataProcessor()
    processor.data = sample_data.copy()
    
    summary = processor.get_summary()
    
    assert summary['row_count'] == 5
    assert summary['column_count'] == 3
    assert set(summary['numeric_columns']) == {'id', 'value'}
    assert summary['categorical_columns'] == ['category']
    assert summary['missing_values']['value'] == 1 