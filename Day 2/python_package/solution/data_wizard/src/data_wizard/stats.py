"""
Statistical operations for data analysis.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Union, Optional

NumericData = Union[List[float], pd.Series, np.ndarray]

def calculate_basic_stats(data: NumericData) -> Dict[str, float]:
    """
    Calculate basic statistical measures.
    
    Args:
        data: Numeric data to analyze
        
    Returns:
        Dictionary containing basic statistics
        
    Raises:
        ValueError: If input data is empty
    """
    data = np.array(data)
    if len(data) == 0:
        raise ValueError("Cannot calculate statistics on empty data")
    
    stats = {
        'mean': float(np.mean(data)),
        'median': float(np.median(data)),
        'std': float(np.std(data)),
        'min': float(np.min(data)),
        'max': float(np.max(data)),
        'count': int(len(data))
    }
    return stats

def calculate_percentiles(data: NumericData, 
                        percentiles: Optional[List[float]] = None) -> Dict[str, float]:
    """
    Calculate percentiles of the data.
    
    Args:
        data: Numeric data to analyze
        percentiles: List of percentiles to calculate (0-100)
        
    Returns:
        Dictionary mapping percentile names to values
        
    Raises:
        ValueError: If input data is empty or percentiles are invalid
    """
    data = np.array(data)
    if len(data) == 0:
        raise ValueError("Cannot calculate percentiles on empty data")
    
    if percentiles is None:
        percentiles = [25, 50, 75]
    
    if not all(0 <= p <= 100 for p in percentiles):
        raise ValueError("Percentiles must be between 0 and 100")
    
    return {f'p{p}': float(np.percentile(data, p)) for p in percentiles}

def detect_outliers(data: NumericData, threshold: float = 1.5) -> List[float]:
    """
    Detect outliers using IQR method.
    
    Args:
        data: Numeric data to analyze
        threshold: IQR multiplier for outlier detection
        
    Returns:
        List of values identified as outliers
        
    Raises:
        ValueError: If input data is empty
    """
    data = np.array(data)
    if len(data) == 0:
        raise ValueError("Cannot detect outliers in empty data")
    
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    
    lower_bound = q1 - threshold * iqr
    upper_bound = q3 + threshold * iqr
    
    outliers = [float(x) for x in data if x < lower_bound or x > upper_bound]
    return outliers

def calculate_correlation(x: NumericData, y: NumericData) -> float:
    """
    Calculate Pearson correlation coefficient between two variables.
    
    Args:
        x: First variable
        y: Second variable
        
    Returns:
        Correlation coefficient
        
    Raises:
        ValueError: If inputs have different lengths or are empty
    """
    x, y = np.array(x), np.array(y)
    if len(x) != len(y):
        raise ValueError("Inputs must have the same length")
    if len(x) == 0:
        raise ValueError("Cannot calculate correlation for empty data")
    
    return float(np.corrcoef(x, y)[0, 1]) 