from data_processor import load_csv, clean_data, filter_by_column, save_csv
from stats_calculator import calculate_basic_stats, detect_outliers
from utils import validate_file_path, save_json_report
import pandas as pd

def main():
    # Example dataset
    data = {
        'age': [25, 30, 35, 40, 45, 90, 35, 25],
        'salary': [30000, 45000, 50000, 60000, 70000, 150000, 50000, 30000],
        'experience': [1, 3, 5, 8, 10, 20, 5, 1]
    }
    
    # Save example data
    df = pd.DataFrame(data)
    df.to_csv('example.csv', index=False)
    
    # Process data
    if validate_file_path('example.csv'):
        # Load and clean data
        df = load_csv('example.csv')
        df = clean_data(df)
        
        # Filter data
        experienced_employees = filter_by_column(df, 'experience', lambda x: x >= 5)
        
        # Calculate statistics
        salary_stats = calculate_basic_stats(df['salary'])
        salary_outliers = detect_outliers(df['salary'])
        
        # Save results
        save_csv(experienced_employees, 'experienced_employees.csv')
        save_json_report({
            'salary_statistics': salary_stats,
            'salary_outliers': salary_outliers
        }, 'analysis_report.json')

if __name__ == "__main__":
    main() 