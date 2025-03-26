"""
Core data processing functionality for the Data Wizard package.
"""

import pandas as pd
from typing import Optional, Union, List, Dict, Any
from pathlib import Path

from data_wizard.utils import validate_file_path, save_json_report


class DataProcessor:
    """Main class for data processing operations."""
    
    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize the DataProcessor.
        
        Args:
            file_path: Optional path to CSV file to load
        """
        self.data: Optional[pd.DataFrame] = None
        if file_path:
            self.load_csv(file_path)
    
    def load_csv(self, file_path: str) -> 'DataProcessor':
        """
        Load data from a CSV file.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            self for method chaining
            
        Raises:
            ValueError: If file path is invalid or file doesn't exist
        """
        if not validate_file_path(file_path):
            raise ValueError(f"Invalid file path: {file_path}")
        
        self.data = pd.read_csv(file_path)
        return self
    
    def clean_data(self, 
                  drop_duplicates: bool = True, 
                  fill_numeric: bool = True) -> 'DataProcessor':
        """
        Clean the loaded data.
        
        Args:
            drop_duplicates: Whether to remove duplicate rows
            fill_numeric: Whether to fill missing numeric values with mean
            
        Returns:
            self for method chaining
            
        Raises:
            ValueError: If no data is loaded
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_csv first.")
        
        if drop_duplicates:
            self.data = self.data.drop_duplicates()
        
        if fill_numeric:
            numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
            self.data[numeric_cols] = self.data[numeric_cols].fillna(
                self.data[numeric_cols].mean()
            )
        
        return self
    
    def filter_by_column(self, 
                        column: str, 
                        condition: callable) -> 'DataProcessor':
        """
        Filter data based on a condition for a specific column.
        
        Args:
            column: Column name to filter on
            condition: Callable that takes a series and returns a boolean mask
            
        Returns:
            self for method chaining
            
        Raises:
            ValueError: If no data is loaded or column doesn't exist
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_csv first.")
        
        if column not in self.data.columns:
            raise ValueError(f"Column {column} not found in data.")
        
        self.data = self.data[condition(self.data[column])]
        return self
    
    def save_csv(self, file_path: str) -> None:
        """
        Save the processed data to a CSV file.
        
        Args:
            file_path: Path where to save the CSV file
            
        Raises:
            ValueError: If no data is loaded
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_csv first.")
        
        self.data.to_csv(file_path, index=False)
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the data.
        
        Returns:
            Dictionary containing summary statistics
            
        Raises:
            ValueError: If no data is loaded
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_csv first.")
        
        numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
        summary = {
            'row_count': len(self.data),
            'column_count': len(self.data.columns),
            'numeric_columns': list(numeric_cols),
            'categorical_columns': list(set(self.data.columns) - set(numeric_cols)),
            'missing_values': self.data.isnull().sum().to_dict()
        }
        
        return summary 