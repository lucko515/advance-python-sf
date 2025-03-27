# 03: Asyncio Basics
print("Python Asyncio Basics")
print("--------------------")

import asyncio
import time
import random

# 1. INTRODUCING THE EVENT LOOP
print("\n1. The Event Loop: The Heart of Asyncio")

# Getting a reference to the event loop
print("\nGetting a reference to the event loop:")
# In older Python versions (pre-3.7):
# loop = asyncio.get_event_loop()

# In modern Python:
print("With Python 3.7+, asyncio.run() manages the event loop for you")
print("You rarely need to access the loop directly")
print("If needed, use asyncio.get_running_loop() from inside a coroutine")

# 2. COROUTINES: THE BUILDING BLOCKS
print("\n2. Coroutines: The Building Blocks of Asyncio")

# A simple coroutine
async def simple_coroutine():
    print("Coroutine started")
    # Simulate some asynchronous operation
    await asyncio.sleep(1)
    print("Coroutine completed after 1 second")
    return "Coroutine result"

# Running a coroutine (the modern way)
print("\nRunning a single coroutine:")
start = time.time()
result = asyncio.run(simple_coroutine())
end = time.time()
print(f"Result: {result}")
print(f"Took {end - start:.2f} seconds")

# 3. RUNNING MULTIPLE COROUTINES
print("\n3. Running Multiple Coroutines")
print("----------------------------")

async def task_with_delay(task_id, delay):
    print(f"Task {task_id} started, will take {delay}s")
    await asyncio.sleep(delay)  # Non-blocking sleep
    print(f"Task {task_id} completed after {delay}s")
    return f"Result from task {task_id}"

async def run_multiple_coroutines():
    # Create coroutines with different delays
    coroutine1 = task_with_delay(1, 2)
    coroutine2 = task_with_delay(2, 1)
    coroutine3 = task_with_delay(3, 3)
    
    # Execute them concurrently and wait for all to complete
    results = await asyncio.gather(coroutine1, coroutine2, coroutine3)
    return results

print("\nRunning multiple coroutines concurrently:")
start = time.time()
results = asyncio.run(run_multiple_coroutines())
end = time.time()
print(f"Results: {results}")
print(f"Took {end - start:.2f} seconds (notice it took ~3s, not 6s)")

# 4. TASKS: MANAGING COROUTINES
print("\n4. Tasks: Managing Coroutines")

async def demonstrate_tasks():
    print("Creating tasks from coroutines:")
    
    # Create a task
    task1 = asyncio.create_task(task_with_delay(1, 2))
    print(f"Task created: {task1}")
    
    # Do other work while task runs
    print("Main coroutine continues running...")
    await asyncio.sleep(0.5)
    print(f"Is task done? {task1.done()}")
    
    # Wait for task to complete
    result = await task1
    print(f"Task completed with result: {result}")
    
    # Create multiple tasks
    tasks = [
        asyncio.create_task(task_with_delay(2, 1)),
        asyncio.create_task(task_with_delay(3, 1.5))
    ]
    
    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)
    return results

print("\nDemonstrating asyncio Tasks:")
task_results = asyncio.run(demonstrate_tasks())
print(f"All task results: {task_results}")

# 5. HANDLING TIMEOUTS AND CANCELLATION
print("\n5. Timeouts and Cancellation")
print("--------------------------")

async def long_running_task():
    print("Long running task started")
    await asyncio.sleep(10)  # Simulate a task that takes too long
    print("Long running task completed")  # We won't see this due to timeout
    return "This result won't be seen"

async def demonstrate_timeout():
    try:
        # Wait for at most 2 seconds
        result = await asyncio.wait_for(long_running_task(), timeout=2)
        return result
    except asyncio.TimeoutError:
        print("Task timed out!")
        return "Timeout occurred"

print("\nDemonstrating timeout:")
timeout_result = asyncio.run(demonstrate_timeout())
print(f"Result: {timeout_result}")

async def demonstrate_cancellation():
    # Start a long-running task
    task = asyncio.create_task(long_running_task())
    
    # Let it run for a bit
    await asyncio.sleep(1)
    
    # Then cancel it
    print("Cancelling task...")
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("Task was cancelled successfully")
    
    return "Cancellation complete"

print("\nDemonstrating cancellation:")
cancel_result = asyncio.run(demonstrate_cancellation())
print(f"Result: {cancel_result}")

# 6. PRACTICAL EXAMPLE: SIMULATING A WEB SERVICE
print("\n6. Practical Example: Simulating a Web Service")
print("-------------------------------------------")

async def fetch_data(data_id):
    """Simulate fetching data from an API"""
    print(f"Fetching data {data_id}...")
    delay = random.uniform(0.5, 2)
    await asyncio.sleep(delay)
    print(f"Data {data_id} retrieved after {delay:.2f}s")
    return f"Data {data_id}: result={random.randint(0, 100)}"

async def process_data(data):
    """Simulate processing the fetched data"""
    print(f"Processing {data}...")
    await asyncio.sleep(0.5)
    result = data + " (processed)"
    print(f"Finished processing: {result}")
    return result

async def fetch_and_process(data_id):
    """Fetch and then process a piece of data"""
    raw_data = await fetch_data(data_id)
    result = await process_data(raw_data)
    return result

async def web_service_simulation():
    """Simulate a web service handling multiple requests"""
    print("Web service started, handling multiple requests...")
    
    # Handle 5 concurrent requests
    tasks = [fetch_and_process(i) for i in range(1, 6)]
    
    # Process all concurrently
    results = await asyncio.gather(*tasks)
    
    return results

print("\nRunning web service simulation:")
start = time.time()
service_results = asyncio.run(web_service_simulation())
end = time.time()
print("\nAll requests processed:")
for result in service_results:
    print(f"- {result}")
print(f"\nTotal processing time: {end - start:.2f}s")

# 7. ASYNCIO EVOLUTION IN PYTHON
print("\n7. Asyncio Evolution in Python")
print("---------------------------")
print("Python 3.4: asyncio introduced as a provisional package")
print("Python 3.5: 'async' and 'await' keywords added")
print("Python 3.6: asyncio stability improvements")
print("Python 3.7: asyncio.run() added, get_event_loop() no longer needed")
print("Python 3.8: asyncio REPL mode and improved debugging")
print("Python 3.9: asyncio.to_thread() for running blocking functions")
print("Python 3.10: Task groups for better task management")
print("Python 3.11: TaskGroup context manager, performance improvements")

print("\n--- Exercise ---")
print("1. Create a 'retry' decorator for async functions that attempts to run")
