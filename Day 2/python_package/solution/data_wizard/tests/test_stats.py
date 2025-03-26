"""
Tests for statistical functions.
"""

import pytest
import numpy as np
import pandas as pd
from data_wizard.stats import (
    calculate_basic_stats,
    calculate_percentiles,
    detect_outliers,
    calculate_correlation
)

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return [1, 2, 3, 4, 5]

@pytest.fixture
def outlier_data():
    """Create sample data with outliers."""
    return [1, 2, 2, 3, 3, 3, 4, 100]

def test_calculate_basic_stats(sample_data):
    """Test basic statistics calculation."""
    stats = calculate_basic_stats(sample_data)
    
    assert stats['mean'] == 3.0
    assert stats['median'] == 3.0
    assert stats['min'] == 1.0
    assert stats['max'] == 5.0
    assert stats['count'] == 5
    assert 1.4 < stats['std'] < 1.6  # Approximately 1.58

def test_calculate_basic_stats_empty():
    """Test basic statistics with empty data."""
    with pytest.raises(ValueError):
        calculate_basic_stats([])

def test_calculate_basic_stats_pandas(sample_data):
    """Test basic statistics with pandas Series."""
    series = pd.Series(sample_data)
    stats = calculate_basic_stats(series)
    
    assert stats['mean'] == 3.0
    assert stats['median'] == 3.0

@pytest.mark.parametrize("data,expected", [
    ([1, 2, 3], {'p25': 1.5, 'p50': 2.0, 'p75': 2.5}),
    ([1], {'p25': 1.0, 'p50': 1.0, 'p75': 1.0}),
    ([1, 1, 1, 1], {'p25': 1.0, 'p50': 1.0, 'p75': 1.0}),
])
def test_calculate_percentiles(data, expected):
    """Test percentile calculations with various inputs."""
    result = calculate_percentiles(data)
    assert result == pytest.approx(expected)

def test_calculate_percentiles_custom():
    """Test custom percentile calculations."""
    data = [1, 2, 3, 4, 5]
    result = calculate_percentiles(data, percentiles=[10, 90])
    
    assert result['p10'] == pytest.approx(1.4)
    assert result['p90'] == pytest.approx(4.6)

def test_calculate_percentiles_invalid():
    """Test percentile calculation with invalid percentiles."""
    with pytest.raises(ValueError):
        calculate_percentiles([1, 2, 3], percentiles=[150])

def test_detect_outliers(outlier_data):
    """Test outlier detection."""
    outliers = detect_outliers(outlier_data)
    assert len(outliers) == 1
    assert outliers[0] == 100.0

def test_detect_outliers_no_outliers(sample_data):
    """Test outlier detection with no outliers."""
    outliers = detect_outliers(sample_data)
    assert len(outliers) == 0

def test_detect_outliers_custom_threshold(outlier_data):
    """Test outlier detection with custom threshold."""
    outliers = detect_outliers(outlier_data, threshold=3.0)
    assert len(outliers) == 1
    assert outliers[0] == 100.0

def test_calculate_correlation():
    """Test correlation calculation."""
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    
    correlation = calculate_correlation(x, y)
    assert correlation == 1.0

def test_calculate_correlation_negative():
    """Test negative correlation calculation."""
    x = [1, 2, 3, 4, 5]
    y = [5, 4, 3, 2, 1]
    
    correlation = calculate_correlation(x, y)
    assert correlation == -1.0

def test_calculate_correlation_no_correlation():
    """Test correlation calculation with uncorrelated data."""
    x = [1, 2, 3, 4, 5]
    y = [1, 1, 1, 1, 1]
    
    correlation = calculate_correlation(x, y)
    assert correlation == 0.0

def test_calculate_correlation_invalid():
    """Test correlation calculation with invalid inputs."""
    with pytest.raises(ValueError):
        calculate_correlation([1, 2], [1, 2, 3]) 