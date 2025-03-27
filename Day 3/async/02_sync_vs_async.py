import time
import asyncio
import requests
import aiohttp
import concurrent.futures
from urllib.parse import quote_plus

# Helper function to display execution time
def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

# SYNCHRONOUS APPROACH
print("\n1. Synchronous Web Requests Example")
print("----------------------------------")

@time_it
def fetch_url_sync(url):
    """Fetch a URL synchronously"""
    print(f"Fetching {url}")
    response = requests.get(url)
    return f"Finished {url}, status: {response.status_code}, length: {len(response.text)} chars"

@time_it
def fetch_multiple_urls_sync(urls):
    """Fetch multiple URLs synchronously (blocking)"""
    results = []
    for url in urls:
        results.append(fetch_url_sync(url))
    return results

# Example URLs to fetch
urls = [
    "https://www.python.org",
    "https://www.salesforce.com",
    "https://www.github.com",
]

# Run synchronous version
print("\nRunning synchronous version...")
sync_results = fetch_multiple_urls_sync(urls)
for result in sync_results:
    print(f"  {result}")

# ASYNCHRONOUS APPROACH
print("\n2. Asynchronous Web Requests Example")
print("-----------------------------------")

async def fetch_url_async(url, session):
    """Fetch a URL asynchronously"""
    print(f"Starting fetch for {url}")
    async with session.get(url) as response:
        text = await response.text()
        print(f"Finished {url}")
        return f"Finished {url}, status: {response.status}, length: {len(text)} chars"

async def fetch_multiple_urls_async(urls):
    """Fetch multiple URLs asynchronously (non-blocking)"""
    async with aiohttp.ClientSession() as session:
        # Create a list of tasks
        tasks = [fetch_url_async(url, session) for url in urls]
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)
        return results

@time_it
def run_async_requests():
    """Run the async event loop"""
    return asyncio.run(fetch_multiple_urls_async(urls))

# Run asynchronous version
print("\nRunning asynchronous version...")
async_results = run_async_requests()
for result in async_results:
    print(f"  {result}")

# THREADED APPROACH (for comparison)
print("\n3. Threaded Web Requests Example")
print("-------------------------------")

@time_it
def fetch_multiple_urls_threaded(urls):
    """Fetch multiple URLs using a thread pool"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_url_sync, urls))
    return results

# Run threaded version
print("\nRunning threaded version...")
threaded_results = fetch_multiple_urls_threaded(urls)
for result in threaded_results:
    print(f"  {result}")

# SIMULATING I/O OPERATIONS
print("\n4. Simulating I/O Operations")
print("---------------------------")

def simulate_io_sync(task_id, duration):
    """Simulate an I/O operation synchronously"""
    print(f"Task {task_id}: Starting I/O operation")
    time.sleep(duration)  # Blocking sleep
    print(f"Task {task_id}: Finished after {duration}s")
    return f"Result from task {task_id}"

@time_it
def run_io_tasks_sync():
    """Run I/O tasks synchronously"""
    results = []
    # Three tasks that take different amounts of time
    results.append(simulate_io_sync(1, 2))
    results.append(simulate_io_sync(2, 1))
    results.append(simulate_io_sync(3, 3))
    return results

async def simulate_io_async(task_id, duration):
    """Simulate an I/O operation asynchronously"""
    print(f"Task {task_id}: Starting I/O operation")
    await asyncio.sleep(duration)  # Non-blocking sleep
    print(f"Task {task_id}: Finished after {duration}s")
    return f"Result from task {task_id}"

async def run_io_tasks_async():
    """Run I/O tasks asynchronously"""
    # Create tasks
    task1 = simulate_io_async(1, 2)
    task2 = simulate_io_async(2, 1)
    task3 = simulate_io_async(3, 3)
    
    # Wait for all tasks to complete
    results = await asyncio.gather(task1, task2, task3)
    return results

@time_it
def run_async_io_simulation():
    """Run the async event loop for I/O simulation"""
    return asyncio.run(run_io_tasks_async())

# Run synchronous I/O simulation
print("\nRunning synchronous I/O simulation:")
sync_io_results = run_io_tasks_sync()
print(f"Synchronous results: {sync_io_results}")

# Run asynchronous I/O simulation
print("\nRunning asynchronous I/O simulation:")
async_io_results = run_async_io_simulation()
print(f"Asynchronous results: {async_io_results}")

# VISUALLY EXPLAINING THE DIFFERENCES
print("\n5. Visualizing Sync vs Async Execution")
print("------------------------------------")

print("\nSynchronous execution (sequential):")
print("┌─────────┐ ┌─────────┐ ┌─────────┐")
print("│ Task 1  │ │ Task 2  │ │ Task 3  │")
print("└─────────┘ └─────────┘ └─────────┘")
print("Time →")

print("\nAsynchronous execution (concurrent):")
print("┌─────────────────┐")
print("│ Task 1          │")
print("├────────┐        │")
print("│ Task 2 │        │")
print("├──────────────┐  │")
print("│ Task 3       │  │")
print("└──────────────┘  │")
print("                  │")
print("                  │")
print("Time →            │")
print("                  │")
print("                  │")
print("└─────────────────┘")

print("\n--- Exercise ---")
print("1. Modify the asynchronous web request example to include error handling.")
print("2. Create a mixed workload with both CPU-bound and I/O-bound tasks, and")
print("   determine the best approach for handling this mixed scenario.")