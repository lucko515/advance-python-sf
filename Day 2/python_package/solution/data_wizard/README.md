# Data Wizard

A Python package for easy data processing and statistical analysis.

## Features

- CSV file handling with data validation
- Data cleaning and preprocessing
- Statistical analysis and outlier detection
- Report generation in JSON format
- Comprehensive error handling and logging

## Installation

```bash
pip install data-wizard
```

## Quick Start

```python
from data_wizard import DataProcessor
from data_wizard.stats import calculate_basic_stats

# Initialize and load data
processor = DataProcessor('data.csv')

# Clean and process data
processor.clean_data(drop_duplicates=True, fill_numeric=True)

# Calculate statistics
stats = calculate_basic_stats(processor.data['value'])
print(stats)
```

## Example Usage

```python
from data_wizard import DataProcessor
from data_wizard.stats import detect_outliers
from data_wizard.utils import save_json_report

# Load and process data
processor = DataProcessor('sales_data.csv')
processor.clean_data()

# Filter data
processor.filter_by_column('revenue', lambda x: x > 1000)

# Detect outliers
outliers = detect_outliers(processor.data['revenue'])

# Generate report
report = {
    'outliers': outliers,
    'summary': processor.get_summary()
}
save_json_report(report, 'analysis_report.json')
```

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/data-wizard.git
   cd data-wizard
   ```

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

For test coverage report:
```bash
pytest --cov=data_wizard tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details. 