"""
Data Wizard - A Python package for easy data processing and statistical analysis.
"""

from data_wizard.processor import DataProcessor
from data_wizard.stats import calculate_basic_stats, calculate_percentiles, detect_outliers
from data_wizard.utils import validate_file_path, save_json_report, format_number

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    'DataProcessor',
    'calculate_basic_stats',
    'calculate_percentiles',
    'detect_outliers',
    'validate_file_path',
    'save_json_report',
    'format_number',
] 