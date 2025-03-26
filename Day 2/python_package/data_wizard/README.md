# Data Wizard

A Python package for easy data processing and statistical analysis.

## Features

- CSV file handling with data validation
- Basic statistical calculations
- Outlier detection
- Data cleaning utilities
- Easy-to-use data filtering

## Installation

```bash
pip install data-wizard
```

## Quick Start

```python
from data_wizard import DataProcessor
from data_wizard.stats import calculate_basic_stats

# Load and process data
processor = DataProcessor('data.csv')
cleaned_data = processor.clean_data()

# Calculate statistics
stats = calculate_basic_stats(cleaned_data['column_name'])
print(stats)
```

## Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Running Tests

```bash
pytest tests/
```

## License

MIT License - see LICENSE file for details. 