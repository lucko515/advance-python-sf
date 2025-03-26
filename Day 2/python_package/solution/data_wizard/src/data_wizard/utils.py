"""
Utility functions for the Data Wizard package.
"""

import os
import json
import logging
from typing import Dict, Any
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_file_path(file_path: str) -> bool:
    """
    Check if file exists and has correct extension.
    
    Args:
        file_path: Path to the file to validate
        
    Returns:
        True if file exists and has .csv extension, False otherwise
    """
    path = Path(file_path)
    
    if not path.exists():
        logger.error(f"File not found: {file_path}")
        return False
    
    if path.suffix.lower() != '.csv':
        logger.error(f"Invalid file extension. Expected .csv, got: {path.suffix}")
        return False
    
    return True

def save_json_report(data: Dict[str, Any], output_path: str) -> None:
    """
    Save dictionary data as JSON file.
    
    Args:
        data: Dictionary to save
        output_path: Path where to save the JSON file
        
    Raises:
        IOError: If there's an error writing the file
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"Report saved successfully to {output_path}")
    except Exception as e:
        logger.error(f"Error saving report: {str(e)}")
        raise

def format_number(value: float, decimal_places: int = 2) -> str:
    """
    Format number with specified decimal places.
    
    Args:
        value: Number to format
        decimal_places: Number of decimal places to show
        
    Returns:
        Formatted string representation of the number
    """
    try:
        return f"{value:.{decimal_places}f}"
    except (ValueError, TypeError) as e:
        logger.error(f"Error formatting number {value}: {str(e)}")
        return str(value)

def ensure_directory(directory: str) -> None:
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        directory: Path to the directory
        
    Raises:
        OSError: If directory cannot be created
    """
    path = Path(directory)
    try:
        path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {str(e)}")
        raise 