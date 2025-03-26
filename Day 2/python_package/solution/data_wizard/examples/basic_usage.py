"""
Basic usage examples for the Data Wizard package.
"""

import pandas as pd
from data_wizard import DataProcessor
from data_wizard.stats import calculate_basic_stats, detect_outliers
from data_wizard.utils import save_json_report

def main():
    # Create example dataset
    data = {
        'age': [25, 30, 35, 40, 45, 90, 35, 25],
        'salary': [30000, 45000, 50000, 60000, 70000, 150000, 50000, 30000],
        'experience': [1, 3, 5, 8, 10, 20, 5, 1]
    }
    df = pd.DataFrame(data)
    df.to_csv('example.csv', index=False)
    
    # Initialize processor and load data
    processor = DataProcessor('example.csv')
    
    # Clean the data
    processor.clean_data(drop_duplicates=True, fill_numeric=True)
    
    # Filter for experienced employees
    processor.filter_by_column('experience', lambda x: x >= 5)
    
    # Save filtered data
    processor.save_csv('experienced_employees.csv')
    
    # Calculate statistics
    salary_stats = calculate_basic_stats(processor.data['salary'])
    salary_outliers = detect_outliers(processor.data['salary'])
    
    # Generate and save report
    report = {
        'salary_statistics': salary_stats,
        'salary_outliers': salary_outliers,
        'data_summary': processor.get_summary()
    }
    save_json_report(report, 'analysis_report.json')
    
    # Print results
    print("\nSalary Statistics:")
    for key, value in salary_stats.items():
        print(f"{key}: {value}")
    
    print("\nOutliers detected:", salary_outliers)
    
    print("\nData Summary:")
    for key, value in processor.get_summary().items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main() 