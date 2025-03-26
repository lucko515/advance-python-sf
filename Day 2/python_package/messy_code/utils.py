import os
from typing import List, Dict, Any
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_file_path(file_path: str) -> bool:
    """Check if file exists and has correct extension."""
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return False
    
    if not file_path.endswith('.csv'):
        logger.error(f"Invalid file extension. Expected .csv, got: {file_path}")
        return False
    
    return True

def save_json_report(data: Dict[str, Any], output_path: str) -> None:
    """Save dictionary data as JSON file."""
    try:
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Report saved successfully to {output_path}")
    except Exception as e:
        logger.error(f"Error saving report: {str(e)}")

def format_number(value: float, decimal_places: int = 2) -> str:
    """Format number with specified decimal places."""
    return f"{value:.{decimal_places}f}"

if __name__ == "__main__":
    # Example usage
    print(validate_file_path("data.csv"))
    print(format_number(3.14159, 3)) 