import itertools
import contextlib
import time
import os
import random
import csv
from io import StringIO

# Case Study 1: Log File Analysis System

# First, let's create a simulated large log file
def generate_log_file(filename, entries=100):
    """Generate a sample log file for demonstration"""
    log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
    services = ["web", "api", "db", "auth", "cache"]
    messages = [
        "Request processed successfully",
        "Connection timeout",
        "Authentication failed",
        "Database query executed",
        "Cache miss",
        "Rate limit exceeded",
        "Invalid request parameters",
        "Session expired",
        "New user registered",
        "Payment processed"
    ]
    
    with open(filename, 'w') as f:
        for i in range(entries):
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - random.randint(0, 86400)))
            level = random.choice(log_levels)
            service = random.choice(services)
            message = random.choice(messages)
            ip = f"192.168.1.{random.randint(1, 255)}"
            user_id = f"user_{random.randint(1, 20)}" if random.random() > 0.3 else "-"
            f.write(f"{timestamp} [{level}] {service}: {message} (IP: {ip}, User: {user_id})\n")

# Create our log file
log_filename = "sample_logs.txt"
generate_log_file(log_filename, entries=1000)
print(f"Generated sample log file: {log_filename} with 1000 entries")

# Now let's build our log analysis pipeline
class LogEntry:
    """Represents a parsed log entry"""
    
    def __init__(self, timestamp, level, service, message, ip, user_id):
        self.timestamp = timestamp
        self.level = level
        self.service = service
        self.message = message
        self.ip = ip
        self.user_id = user_id
    
    def __str__(self):
        return f"{self.timestamp} [{self.level}] {self.service}: {self.message}"

# Step 1: Log File Reader (Context Manager & Generator)
@contextlib.contextmanager
def log_reader(filename):
    """Context manager for reading log files"""
    print(f"Opening log file: {filename}")
    try:
        file = open(filename, 'r')
        yield file
    finally:
        file.close()
        print(f"Closed log file: {filename}")

# Step 2: Line Parser (Generator)
def parse_log_lines(log_file):
    """Generator that parses log lines into structured LogEntry objects"""
    for line_num, line in enumerate(log_file, 1):
        try:
            # Extract components with a simple parser
            # Format: timestamp [LEVEL] service: message (IP: ip, User: user_id)
            timestamp = line[:19]
            level_start = line.find('[') + 1
            level_end = line.find(']')
            level = line[level_start:level_end]
            
            service_end = line.find(':', level_end)
            service = line[level_end+2:service_end].strip()
            
            # Extract message and metadata
            metadata_start = line.rfind('(')
            message = line[service_end+1:metadata_start].strip()
            
            # Parse metadata
            metadata = line[metadata_start+1:].strip(')\n')
            ip = metadata.split('User:')[0].replace('IP:', '').strip()
            user_id = metadata.split('User:')[1].strip()
            
            yield LogEntry(timestamp, level, service, message, ip, user_id)
        except Exception as e:
            print(f"Error parsing line {line_num}: {line.strip()} - {str(e)}")

# Step 3: Filtering (Generator)
def filter_logs(log_entries, level=None, service=None):
    """Filter log entries by level and/or service"""
    for entry in log_entries:
        if (level is None or entry.level == level) and \
           (service is None or entry.service == service):
            yield entry

# Step 4: Analysis (Itertools & Generator)
def analyze_logs(log_entries):
    """Generate analysis metrics from log entries"""
    # Make copies of the iterator for different analyses
    entries1, entries2, entries3 = itertools.tee(log_entries, 3)
    
    # Count by level
    level_counts = {}
    for entry in entries1:
        level_counts[entry.level] = level_counts.get(entry.level, 0) + 1
    
    # Count by service
    service_counts = {}
    for entry in entries2:
        service_counts[entry.service] = service_counts.get(entry.service, 0) + 1
    
    # Find most active users
    user_counts = {}
    for entry in entries3:
        if entry.user_id != "-":
            user_counts[entry.user_id] = user_counts.get(entry.user_id, 0) + 1
    
    # Sort user counts to find most active
    top_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "level_counts": level_counts,
        "service_counts": service_counts,
        "top_users": top_users
    }

# Step 5: Reporting (Context Manager)
@contextlib.contextmanager
def report_writer(filename):
    """Context manager for writing reports"""
    print(f"Creating report file: {filename}")
    try:
        file = open(filename, 'w')
        yield file
    finally:
        file.close()
        print(f"Closed report file: {filename}")

# Bringing it all together
def analyze_log_file(log_file, report_file, filter_level=None, filter_service=None):
    """Complete log analysis pipeline"""
    with contextlib.ExitStack() as stack:
        # Setup both file handlers
        logs = stack.enter_context(log_reader(log_file))
        report = stack.enter_context(report_writer(report_file))
        
        # Create the pipeline
        parsed_logs = parse_log_lines(logs)
        filtered_logs = filter_logs(parsed_logs, level=filter_level, service=filter_service)
        
        # Start timing
        start_time = time.time()
        
        # Write report header
        report.write("LOG ANALYSIS REPORT\n")
        report.write("==================\n\n")
        
        if filter_level or filter_service:
            report.write("Filters applied:\n")
            if filter_level:
                report.write(f"- Level: {filter_level}\n")
            if filter_service:
                report.write(f"- Service: {filter_service}\n")
            report.write("\n")
        
        # Process the data and get analysis
        print("Processing log entries...")
        
        # Calculate metrics
        metrics = analyze_logs(filtered_logs)
        
        # Write metrics to report
        report.write("Level Distribution:\n")
        for level, count in metrics["level_counts"].items():
            report.write(f"- {level}: {count}\n")
        
        report.write("\nService Distribution:\n")
        for service, count in metrics["service_counts"].items():
            report.write(f"- {service}: {count}\n")
        
        report.write("\nMost Active Users:\n")
        for user, count in metrics["top_users"]:
            report.write(f"- {user}: {count} entries\n")
        
        # End timing
        end_time = time.time()
        report.write(f"\nAnalysis completed in {end_time - start_time:.2f} seconds\n")
        
        print(f"Analysis completed in {end_time - start_time:.2f} seconds")

# Run the analysis
print("\nRunning log analysis pipeline...")
analyze_log_file(log_filename, "log_report.txt", filter_level="ERROR")

# Display a sample of the report
with open("log_report.txt", "r") as f:
    report_sample = f.read(500)  # Read a portion
    print("\nSample of generated report:")
    print("--------------------------")
    print(report_sample + "...")


# Case Study 2: Data Transformation Pipeline
print("\n\n2. Data Transformation Pipeline")


# First, create a sample CSV file
def generate_sample_csv(filename, rows=100):
    """Generate a sample CSV with some invalid data"""
    headers = ["id", "name", "email", "age", "subscription"]
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for i in range(1, rows + 1):
            # Occasionally generate invalid data
            if i % 20 == 0:
                age = "invalid_age"  # Invalid age
            else:
                age = random.randint(18, 80)
            
            if i % 15 == 0:
                email = "invalid_email"  # Invalid email
            else:
                email = f"user{i}@example.com"
            
            name = f"User {i}"
            subscription = random.choice(["free", "basic", "premium", "enterprise"])
            
            writer.writerow([i, name, email, age, subscription])

# Create sample CSV
csv_filename = "sample_data.csv"
generate_sample_csv(csv_filename, rows=100)
print(f"Generated sample CSV file: {csv_filename} with 100 entries")

# Create the data transformation pipeline

# Step 1: CSV Reader Context Manager
@contextlib.contextmanager
def csv_file_manager(input_file, output_file):
    """Context manager to handle CSV input and output files"""
    print(f"Opening input file: {input_file}")
    print(f"Preparing output file: {output_file}")
    
    try:
        in_file = open(input_file, 'r', newline='')
        out_file = open(output_file, 'w', newline='')
        
        reader = csv.DictReader(in_file)
        
        # Get field names from the reader, add transformation metadata
        fieldnames = reader.fieldnames + ["processed_at", "validated"]
        
        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()
        
        yield reader, writer
    finally:
        in_file.close()
        out_file.close()
        print(f"Closed input file: {input_file}")
        print(f"Closed output file: {output_file}")

# Step 2: Validation functions
def validate_email(email):
    """Simple email validation"""
    return '@' in email and '.' in email.split('@')[1]

def validate_age(age):
    """Validate age is a number between 18 and 120"""
    try:
        age_num = int(age)
        return 18 <= age_num <= 120
    except (ValueError, TypeError):
        return False

# Step 3: Data transformation generator
def transform_data(reader, error_log=None):
    """Generator that transforms and validates data rows"""
    for row_num, row in enumerate(reader, 2):  # Start at 2 to account for header row
        # Create a copy of the row for transformation
        transformed = row.copy()
        
        # Add metadata
        transformed['processed_at'] = time.strftime("%Y-%m-%d %H:%M:%S")
        transformed['validated'] = "true"
        
        # Validate email
        if not validate_email(row['email']):
            transformed['validated'] = "false"
            if error_log:
                error_log.write(f"Row {row_num}: Invalid email: {row['email']}\n")
        
        # Validate and convert age
        if not validate_age(row['age']):
            transformed['validated'] = "false"
            if error_log:
                error_log.write(f"Row {row_num}: Invalid age: {row['age']}\n")
        else:
            # Convert age to integer
            transformed['age'] = int(row['age'])
        
        # Normalize subscription to lowercase
        transformed['subscription'] = row['subscription'].lower()
        
        yield transformed

# Step 4: Data statistics calculator
def calculate_statistics(transformed_data):
    """Calculate statistics from transformed data"""
    # Need multiple passes, so tee the iterator
    data1, data2, data3 = itertools.tee(transformed_data, 3)
    
    # Count valid and invalid records
    valid_count = sum(1 for row in data1 if row['validated'] == "true")
    invalid_count = sum(1 for row in data2 if row['validated'] == "false")
    
    # Count by subscription type
    subscription_counts = {}
    valid_ages = []
    
    for row in data3:
        sub_type = row['subscription']
        subscription_counts[sub_type] = subscription_counts.get(sub_type, 0) + 1
        
        # Collect valid ages for average calculation
        if row['validated'] == "true":
            try:
                valid_ages.append(int(row['age']))
            except (ValueError, TypeError):
                pass
    
    # Calculate average age if we have valid ages
    avg_age = sum(valid_ages) / len(valid_ages) if valid_ages else 0
    
    return {
        'total_records': valid_count + invalid_count,
        'valid_records': valid_count,
        'invalid_records': invalid_count,
        'subscription_distribution': subscription_counts,
        'average_age': avg_age
    }

# Bringing it all together
def process_csv_data(input_file, output_file, error_file):
    """Complete data transformation pipeline"""
    with contextlib.ExitStack() as stack:
        # Open all files with proper context management
        error_log = stack.enter_context(open(error_file, 'w'))
        csv_context = stack.enter_context(csv_file_manager(input_file, output_file))
        reader, writer = csv_context
        
        # Write error log header
        error_log.write("DATA VALIDATION ERRORS\n")
        error_log.write("=====================\n\n")
        
        print("Processing data...")
        start_time = time.time()
        
        # Create transformation pipeline
        transformed_data = transform_data(reader, error_log)
        
        # Generate a copy for statistics while writing rows
        data_for_stats, data_for_writing = itertools.tee(transformed_data)
        
        # Write transformed data to output
        for row in data_for_writing:
            writer.writerow(row)
        
        # Calculate statistics
        stats = calculate_statistics(data_for_stats)
        
        end_time = time.time()
        
        # Write statistics to error log
        error_log.write("\nPROCESSING STATISTICS\n")
        error_log.write("====================\n\n")
        error_log.write(f"Total records processed: {stats['total_records']}\n")
        error_log.write(f"Valid records: {stats['valid_records']}\n")
        error_log.write(f"Invalid records: {stats['invalid_records']}\n")
        error_log.write(f"Average age: {stats['average_age']:.1f}\n\n")
        
        error_log.write("Subscription distribution:\n")
        for sub_type, count in stats['subscription_distribution'].items():
            error_log.write(f"- {sub_type}: {count}\n")
        
        error_log.write(f"\nProcessing completed in {end_time - start_time:.2f} seconds\n")
        
        print(f"Data processing completed in {end_time - start_time:.2f} seconds")
        print(f"Processed {stats['total_records']} records ({stats['valid_records']} valid, {stats['invalid_records']} invalid)")
        print(f"Results written to {output_file}")
        print(f"Error log written to {error_file}")

# Run the data transformation
print("\nRunning data transformation pipeline...")
process_csv_data(csv_filename, "transformed_data.csv", "data_errors.log")

# Display a sample of the transformed data
with open("transformed_data.csv", "r") as f:
    transformed_sample = f.read(300)  # Read a portion
    print("\nSample of transformed data:")
    print("--------------------------")
    print(transformed_sample + "...")

# Display a sample of the error log
with open("data_errors.log", "r") as f:
    error_sample = f.read(300)  # Read a portion
    print("\nSample of error log:")
    print("------------------")
    print(error_sample + "...")


# Case Study 3: Memory-Efficient Data Pipeline
print("\n\n3. Memory-Efficient Data Pipeline")
print("==============================")
print("Problem: Calculate moving averages on large datasets")
print("Requirements:")
print("- Process data larger than available memory")
print("- Calculate sliding window statistics")
print("- Clean resource handling")

# Create a sample time series data file
def generate_timeseries_data(filename, points=10000):
    """Generate sample time series data for demonstration"""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "value"])
        
        # Generate a sine wave with noise
        for i in range(points):
            timestamp = time.strftime(
                "%Y-%m-%d %H:%M:%S", 
                time.localtime(time.time() - (points - i) * 60)
            )
            # Sine wave with period of 1000 points plus random noise
            value = 100 + 50 * math.sin(i * 2 * math.pi / 1000) + random.uniform(-10, 10)
            writer.writerow([timestamp, f"{value:.2f}"])

import math
# Generate sample time series data
timeseries_filename = "timeseries_data.csv"
generate_timeseries_data(timeseries_filename, points=10000)
print(f"Generated sample time series data: {timeseries_filename} with 10,000 data points")

# Build the data processing pipeline

# Step 1: Memory-efficient CSV reader
def read_csv_values(filename):
    """Generator to read CSV values lazily"""
    with open(filename, 'r', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Skip header row
        
        for row in reader:
            timestamp = row[0]
            try:
                value = float(row[1])
                yield timestamp, value
            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row} - {str(e)}")

# Step 2: Sliding window calculator
def moving_average(data, window_size):
    """Calculate moving average using a sliding window"""
    window = []
    
    for timestamp, value in data:
        window.append((timestamp, value))
        if len(window) > window_size:
            window.pop(0)  # Remove oldest item
        
        if len(window) == window_size:
            avg_value = sum(v for _, v in window) / window_size
            yield window[-1][0], avg_value  # Use latest timestamp

# Step 3: Moving standard deviation
def moving_stddev(data, window_size):
    """Calculate moving standard deviation"""
    window = []
    
    for timestamp, value in data:
        window.append((timestamp, value))
        if len(window) > window_size:
            window.pop(0)  # Remove oldest item
        
        if len(window) == window_size:
            values = [v for _, v in window]
            mean = sum(values) / window_size
            variance = sum((v - mean) ** 2 for v in values) / window_size
            stddev = math.sqrt(variance)
            yield window[-1][0], stddev

# Step 4: Outlier detection
def detect_outliers(data, stddev_threshold=2.0):
    """Detect values that are outliers based on distance from moving average"""
    for timestamp, (avg, stddev, actual) in data:
        is_outlier = abs(actual - avg) > stddev_threshold * stddev
        yield timestamp, avg, stddev, actual, is_outlier

# Bringing it all together
def analyze_timeseries(input_file, output_file, window_size=20, stddev_threshold=2.0):
    """Complete time series analysis pipeline"""
    
    with open(output_file, 'w', newline='') as out_file:
        # Set up CSV writer
        writer = csv.writer(out_file)
        writer.writerow(["timestamp", "actual", "moving_avg", "moving_stddev", "is_outlier"])
        
        print(f"Processing time series with window size {window_size}...")
        start_time = time.time()
        
        # Read data once and create copies for different calculations
        raw_data = read_csv_values(input_file)
        avg_data, stddev_data, original_data = itertools.tee(raw_data, 3)
        
        # Calculate moving average
        ma_data = moving_average(avg_data, window_size)
        
        # Calculate moving standard deviation
        mstd_data = moving_stddev(stddev_data, window_size)
        
        # Create a dictionary to store original values for later lookup
        original_values = {}
        for timestamp, value in itertools.islice(original_data, window_size):
            original_values[timestamp] = value
        
        # Create a dictionary to store moving averages
        ma_values = {}
        
        # Process moving averages while collecting needed values
        for timestamp, avg in ma_data:
            ma_values[timestamp] = avg
            
            # Keep only necessary timestamps in original_values
            # This keeps memory usage minimal even for huge datasets
            if len(original_values) > window_size * 2:
                oldest_timestamp = min(original_values.keys())
                del original_values[oldest_timestamp]
        
        # Process outliers using moving average and standard deviation
        outlier_data = []
        for timestamp, stddev in mstd_data:
            if timestamp in ma_values and timestamp in original_values:
                avg = ma_values[timestamp]
                actual = original_values[timestamp]
                is_outlier = abs(actual - avg) > stddev_threshold * stddev
                outlier_data.append((timestamp, actual, avg, stddev, is_outlier))
                
                # Remove processed data to free memory
                del ma_values[timestamp]
                del original_values[timestamp]
        
        # Write results
        for timestamp, actual, avg, stddev, is_outlier in outlier_data:
            writer.writerow([timestamp, f"{actual:.2f}", f"{avg:.2f}", f"{stddev:.2f}", is_outlier])
        
        end_time = time.time()
        
        print(f"Time series analysis completed in {end_time - start_time:.2f} seconds")
        print(f"Results written to {output_file}")
        
        # Count outliers
        outlier_count = sum(1 for _, _, _, _, is_outlier in outlier_data if is_outlier)
        print(f"Detected {outlier_count} outliers out of {len(outlier_data)} data points")

# Run the time series analysis
print("\nRunning time series analysis pipeline...")
analyze_timeseries(timeseries_filename, "timeseries_analysis.csv", window_size=30)

# Display a sample of the analysis results
with open("timeseries_analysis.csv", "r") as f:
    analysis_sample = f.read(300)  # Read a portion
    print("\nSample of time series analysis:")
    print("-----------------------------")
    print(analysis_sample + "...")

# Clean up generated files
print("\nCleaning up generated files...")
for file in [log_filename, csv_filename, timeseries_filename, 
             "log_report.txt", "transformed_data.csv", "data_errors.log", 
             "timeseries_analysis.csv", "example.txt", "temp_config.txt"]:
    if os.path.exists(file):
        os.remove(file)
        print(f"Removed: {file}")

print("\n--- Exercise ---")
print("Build a complete data processing system that:")
print("1. Reads multiple data sources (CSV, JSON, etc.) using the appropriate iterator patterns")
print("2. Transforms and validates the data with a generator pipeline")
print("3. Handles errors gracefully, logging issues without crashing")
print("4. Uses context managers to manage resources properly")
print("5. Produces summary statistics and exports processed data")
print("6. Optimizes for memory efficiency with large datasets")

print("\nYour solution should incorporate all the key concepts from this course:")
print("- Custom iterators for specialized data access patterns")
print("- Generators for lazy evaluation and memory efficiency")
print("- Context managers for clean resource management")
print("- Itertools for powerful data transformations")
print("- Error handling and recovery mechanisms") 