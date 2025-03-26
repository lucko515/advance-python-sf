# 06: Real-World Debugging Scenarios
print("Real-World Debugging Scenarios")
print("----------------------------")

# Let's simulate a small application with interconnected components
# to demonstrate realistic debugging scenarios

import logging
import random
import json
import datetime
import time
from collections import defaultdict

# Configure logging for our debugging session
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('debugging_demo')

# 1. The Data Processing Pipeline
print("\n1. Debugging a Data Processing Pipeline")
print("------------------------------------")

class DataSource:
    """Simulates a data source like a database or API."""
    def __init__(self, data=None):
        self.data = data or []
    
    def get_data(self, limit=None):
        """Get data with occasional simulated failures."""
        if random.random() < 0.1:  # 10% chance of failure
            raise ConnectionError("Failed to connect to data source")
        
        if limit:
            return self.data[:limit]
        return self.data

class DataProcessor:
    """Processes data from the data source."""
    def __init__(self, data_source):
        self.data_source = data_source
        self.logger = logging.getLogger('debugging_demo.processor')
    
    def process(self, limit=None):
        try:
            self.logger.info("Starting data processing")
            data = self.data_source.get_data(limit)
            
            # Process the data
            results = []
            for item in data:
                # Bug 1: TypeError when processing non-dict items (KeyError)
                processed = self._transform_item(item)
                results.append(processed)
            
            self.logger.info(f"Processed {len(results)} items")
            return results
        
        except Exception as e:
            self.logger.error(f"Error in data processing: {e}")
            raise
    
    def _transform_item(self, item):
        """Transform a data item - contains a bug."""
        # Bug: Doesn't check if 'value' exists
        if isinstance(item, dict) and 'value' in item:
            return item['value'] * 2
        return item  # This will cause issues later if not a number

class DataAnalyzer:
    """Analyzes processed data."""
    def __init__(self):
        self.logger = logging.getLogger('debugging_demo.analyzer')
    
    def analyze(self, data):
        try:
            self.logger.info("Starting data analysis")
            
            if not data:
                return {"error": "No data to analyze"}
            
            # Calculate statistics
            # Bug 2: TypeError when data contains non-numeric values
            total = sum(data)
            avg = total / len(data)
            
            # Bug 3: Logic error - max calculation is incorrect for negative numbers
            max_val = 0
            for item in data:
                if item > max_val:
                    max_val = item
            
            results = {
                "count": len(data),
                "total": total,
                "average": avg,
                "maximum": max_val
            }
            
            self.logger.info(f"Analysis complete: {results}")
            return results
        
        except Exception as e:
            self.logger.error(f"Error in data analysis: {e}")
            raise

class ReportGenerator:
    """Generates reports from analyzed data."""
    def __init__(self):
        self.logger = logging.getLogger('debugging_demo.reporter')
    
    def generate_report(self, analysis):
        try:
            self.logger.info("Generating report")
            
            # Bug 4: KeyError when expected keys are missing
            report = f"""
            Data Analysis Report
            --------------------
            Count: {analysis['count']}
            Total: {analysis['total']:.2f}
            Average: {analysis['average']:.2f}
            Maximum: {analysis['maximum']:.2f}
            
            Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            self.logger.info("Report generated successfully")
            return report
        
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            raise

# 2. Debugging Exercise: Find and Fix the Pipeline Bugs
print("\n2. Debugging Exercise: Data Pipeline")
print("---------------------------------")

def run_pipeline(data):
    """Run the full pipeline with the given data."""
    print("\nRunning data pipeline with sample data...")
    
    # Set up the pipeline components
    data_source = DataSource(data)
    processor = DataProcessor(data_source)
    analyzer = DataAnalyzer()
    reporter = ReportGenerator()
    
    try:
        # Process the data
        processed_data = processor.process()
        print(f"Processed data: {processed_data[:5]}...")
        
        # Analyze the results
        analysis = analyzer.analyze(processed_data)
        print(f"Analysis results: {analysis}")
        
        # Generate a report
        report = reporter.generate_report(analysis)
        print("\nFinal Report:")
        print(report)
        
        return True
    
    except Exception as e:
        print(f"Pipeline failed: {e}")
        return False

# Sample data with bugs
sample_data = [
    {"id": 1, "value": 10},
    {"id": 2, "value": 20},
    {"id": 3, "value": 30},
    {"id": 4},  # Missing 'value' key - will cause Bug 1
    "invalid",  # Not a dict - will cause Bug 1
    {"id": 5, "value": -40}  # Negative value - will trigger Bug 3
]

success = run_pipeline(sample_data)
print(f"Pipeline {'succeeded' if success else 'failed'} with buggy data")


# 3. Web API Debugging Scenario
print("\n3. Debugging a Web API Integration")
print("-------------------------------")

class APIClient:
    """Simulates a client for an external API."""
    def __init__(self, base_url="https://api.example.com"):
        self.base_url = base_url
        self.logger = logging.getLogger('debugging_demo.api_client')
    
    def get_data(self, endpoint, params=None):
        """Simulate fetching data from an API."""
        self.logger.info(f"Fetching data from {endpoint} with params {params}")
        
        # Simulate API latency
        time.sleep(0.1)
        
        # Simulate API responses with potential issues
        if endpoint == "/users":
            return [
                {"id": 1, "name": "Alice", "email": "alice@example.com"},
                {"id": 2, "name": "Bob", "email": "bob@example.com"},
                # Missing email
                {"id": 3, "name": "Charlie"},
            ]
        elif endpoint == "/products":
            return [
                {"id": 101, "name": "Widget", "price": 19.99},
                {"id": 102, "name": "Gadget", "price": "29.99"},  # Price as string
                {"id": 103, "name": "Doohickey", "price": None}  # None price
            ]
        else:
            # Simulate a 404 error
            raise ValueError(f"Unknown endpoint: {endpoint}")

class DataTransformer:
    """Transforms API data for our application."""
    def __init__(self):
        self.logger = logging.getLogger('debugging_demo.transformer')
    
    def transform_users(self, users):
        """Transform user data - contains bugs."""
        self.logger.info(f"Transforming {len(users)} users")
        
        transformed = []
        for user in users:
            try:
                # Bug: KeyError if 'email' is missing
                transformed.append({
                    "user_id": user["id"],
                    "full_name": user["name"],
                    "contact": user["email"],
                    "welcome_message": f"Hello, {user['name']}!"
                })
            except KeyError as e:
                self.logger.error(f"Missing required field in user data: {e}")
                # Bug: Continues without adding this user
        
        return transformed
    
    def transform_products(self, products):
        """Transform product data - contains bugs."""
        self.logger.info(f"Transforming {len(products)} products")
        
        transformed = []
        for product in products:
            try:
                # Bug: TypeError when price is not a number or is None
                price = product["price"]
                discounted_price = price * 0.9  # Apply 10% discount
                
                transformed.append({
                    "product_id": product["id"],
                    "title": product["name"],
                    "regular_price": price,
                    "sale_price": round(discounted_price, 2)
                })
            except (KeyError, TypeError) as e:
                self.logger.error(f"Error processing product: {e}")
                # Bug: Continues without adding this product
        
        return transformed

def debug_api_integration():
    """Exercise to debug the API integration."""
    print("\nDebugging API integration issues...")
    
    client = APIClient()
    transformer = DataTransformer()
    
    try:
        # Fetch and transform user data
        users = client.get_data("/users")
        transformed_users = transformer.transform_users(users)
        print(f"\nTransformed users ({len(transformed_users)} of {len(users)}):")
        for user in transformed_users:
            print(f"  - {user['full_name']} ({user['contact']})")
        
        # Fetch and transform product data
        products = client.get_data("/products")
        transformed_products = transformer.transform_products(products)
        print(f"\nTransformed products ({len(transformed_products)} of {len(products)}):")
        for product in transformed_products:
            print(f"  - {product['title']}: ${product['regular_price']} (Sale: ${product['sale_price']})")
        
        return True
    
    except Exception as e:
        print(f"API integration failed: {e}")
        return False

debug_api_integration()

# 4. Performance Debugging Scenario
print("\n4. Debugging Performance Issues")
print("----------------------------")

def simulate_slow_function():
    """A function with performance issues to debug."""
    print("\nSimulating a slow function...")
    
    # Generate test data
    data_size = 10000
    test_data = [random.randint(1, 100) for _ in range(data_size)]
    
    start_time = time.time()
    
    # Bug 1: Inefficient way to count occurrences
    counts = {}
    for item in test_data:
        found = False
        for key in counts:
            if key == item:
                counts[key] += 1
                found = True
                break
        if not found:
            counts[item] = 1
    
    # Bug 2: Inefficient way to find keys with specific counts
    specific_count = 50
    matching_keys = []
    for item in range(1, 101):  # Check all possible values 1-100
        for key, count in counts.items():
            if key == item and count > specific_count:
                matching_keys.append(key)
    
    # Bug 3: Inefficient string building
    result_str = ""
    for key in matching_keys:
        result_str += f"Item {key} appeared {counts[key]} times. "
    
    end_time = time.time()
    
    print(f"Processed {data_size} items in {end_time - start_time:.6f} seconds")
    print(f"Found {len(matching_keys)} items appearing more than {specific_count} times")
    print(f"First 100 chars of result: {result_str[:100]}...")
    
    return end_time - start_time

slow_time = simulate_slow_function()

# Example of optimized version (for instructor reference)
def optimized_function():
    """The same function after optimization."""
    print("\nSimulating the optimized function...")
    
    # Generate test data
    data_size = 10000
    test_data = [random.randint(1, 100) for _ in range(data_size)]
    
    start_time = time.time()
    
    # Optimization 1: Use Counter for efficient counting
    counts = defaultdict(int)
    for item in test_data:
        counts[item] += 1
    
    # Optimization 2: Direct filtering of values
    specific_count = 50
    matching_keys = [key for key, count in counts.items() if count > specific_count]
    
    # Optimization 3: Use join for string building
    result_parts = [f"Item {key} appeared {counts[key]} times. " for key in matching_keys]
    result_str = "".join(result_parts)
    
    end_time = time.time()
    
    print(f"Processed {data_size} items in {end_time - start_time:.6f} seconds")
    print(f"Found {len(matching_keys)} items appearing more than {specific_count} times")
    print(f"First 100 chars of result: {result_str[:100]}...")
    
    return end_time - start_time

optimized_time = optimized_function()

print(f"\nPerformance comparison:")
print(f"Original function: {slow_time:.6f} seconds")
print(f"Optimized function: {optimized_time:.6f} seconds")
print(f"Speedup factor: {slow_time / optimized_time:.1f}x")

# 5. Memory Leak Debugging
print("\n5. Debugging Memory Leaks")
print("----------------------")

class CacheManager:
    """A class with a memory leak bug."""
    def __init__(self):
        self.cache = {}
        self._reference_history = []  # Bug: Keeps growing without cleanup
    
    def add_to_cache(self, key, value):
        """Add an item to the cache."""
        self.cache[key] = value
        # Bug: Stores a reference that's never cleaned up
        self._reference_history.append((key, value, datetime.datetime.now()))
    
    def get_from_cache(self, key):
        """Get an item from the cache."""
        return self.cache.get(key)
    
    def clear_cache(self):
        """Clear the cache - bug: doesn't clear history."""
        self.cache.clear()
        # Bug: _reference_history is not cleared

def simulate_memory_leak():
    """Simulate a program with a memory leak."""
    print("\nSimulating a program with a memory leak...")
    
    cache = CacheManager()
    
    # Simulate program running over time
    for i in range(1000):
        # Add large objects to the cache
        key = f"key_{i}"
        value = "x" * 10000  # 10KB string
        cache.add_to_cache(key, value)
        
        # Every 100 operations, clear the cache but not the history (bug)
        if i % 100 == 0:
            cache.clear_cache()
            print(f"Iteration {i}: Cache cleared")
    
    # Check memory usage
    cache_size = len(cache.cache)
    history_size = len(cache._reference_history)
    history_memory = sum(len(key) + len(value) for key, value, _ in cache._reference_history)
    
    print(f"Final cache size: {cache_size} items")
    print(f"History size: {history_size} items")
    print(f"Estimated history memory usage: {history_memory / 1024:.2f} KB")
    
simulate_memory_leak()

# 6. Multi-threaded Debugging
print("\n6. Debugging Multi-threaded Code")
print("-----------------------------")