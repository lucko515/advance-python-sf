import pandas as pd
import numpy as np
from typing import Dict, Union, List

def calculate_basic_stats(data: Union[List[float], pd.Series]) -> Dict[str, float]:
    """Calculate basic statistical measures."""
    stats = {
        'mean': np.mean(data),
        'median': np.median(data),
        'std': np.std(data),
        'min': np.min(data),
        'max': np.max(data)
    }
    return stats

def calculate_percentiles(data: Union[List[float], pd.Series], 
                        percentiles: List[float] = [25, 50, 75]) -> Dict[str, float]:
    """Calculate percentiles of the data."""
    return {f'p{p}': np.percentile(data, p) for p in percentiles}

def detect_outliers(data: Union[List[float], pd.Series], threshold: float = 1.5) -> List[float]:
    """Detect outliers using IQR method."""
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - threshold * iqr
    upper_bound = q3 + threshold * iqr
    
    return [x for x in data if x < lower_bound or x > upper_bound]

if __name__ == "__main__":
    # Example usage
    sample_data = [1, 2, 2, 3, 4, 5, 5, 6, 100]
    print("Basic stats:", calculate_basic_stats(sample_data))
    print("Percentiles:", calculate_percentiles(sample_data))
    print("Outliers:", detect_outliers(sample_data)) 