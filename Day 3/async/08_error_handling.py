import asyncio
import random
import sys
import traceback
import time
from typing import List, Dict, Any, Optional

# 1. EXCEPTION FUNDAMENTALS
print("\n1. Exception Handling Fundamentals")
print("-------------------------------")
print("- async/await code uses the same try/except/finally mechanism")
print("- Exceptions propagate through the await chain")
print("- Unhandled exceptions in tasks can be lost if not properly awaited")
print("- asyncio has special exception types like CancelledError and TimeoutError")

# Basic exception handling in coroutines
async def exception_demo():
    print("\nBasic exception handling in coroutines:")
    
    # Define a coroutine that raises an exception
    async def failing_coroutine():
        await asyncio.sleep(0.1)
        raise ValueError("Something went wrong!")
    
    # Handle exception with try/except
    try:
        await failing_coroutine()
    except ValueError as e:
        print(f"Caught exception: {e}")
    
    print("Coroutine continued after exception")

# Run the exception demo
print("\nDemonstrating basic exception handling:")
asyncio.run(exception_demo())

# 2. HANDLING EXCEPTIONS IN TASKS
print("\n2. Handling Exceptions in Tasks")
print("----------------------------")
print("- Exceptions in tasks don't propagate automatically")
print("- Unhandled exceptions are only raised when the task is awaited")
print("- Fire-and-forget tasks can silently fail")
print("- gather() with return_exceptions=True collects exceptions")

async def task_exception_demo():
    print("\nException handling with tasks:")
    
    # A task that will fail
    async def failing_task():
        await asyncio.sleep(0.2)
        raise RuntimeError("Task failed!")
    
    # Method 1: Try-except when awaiting
    print("\nMethod 1: Try-except when awaiting the task:")
    task1 = asyncio.create_task(failing_task())
    try:
        await task1
    except RuntimeError as e:
        print(f"Caught exception from task1: {e}")
    
    # Method 2: Check for exception after task completes
    print("\nMethod 2: Check exception after task completes:")
    task2 = asyncio.create_task(failing_task())
    # Let the task complete
    await asyncio.sleep(0.3)
    
    if task2.done():
        if task2.exception():
            print(f"Task2 failed with: {task2.exception()}")
        else:
            print("Task2 completed without exception")
    
    # Method 3: Fire-and-forget task (BAD PRACTICE)
    print("\nMethod 3: Fire-and-forget task (BAD PRACTICE):")
    task3 = asyncio.create_task(failing_task())
    await asyncio.sleep(0.3)
    print("Notice that we didn't see the exception from task3! It was lost.")
    
    # Method 4: Add an exception handler
    print("\nMethod 4: Add done callback to handle exception:")
    
    def handle_task_result(task):
        try:
            # This will re-raise the exception if any
            task.result()
        except Exception as e:
            print(f"Task exception caught in callback: {e}")
    
    task4 = asyncio.create_task(failing_task())
    task4.add_done_callback(handle_task_result)
    await asyncio.sleep(0.3)  # Give time for the task to complete

# Run the task exception demo
print("\nDemonstrating exception handling in tasks:")
asyncio.run(task_exception_demo())

# 3. HANDLING EXCEPTIONS WITH GATHER
print("\n3. Handling Exceptions with gather()")
print("---------------------------------")
print("- gather() collects all exceptions when return_exceptions=True")
print("- Without return_exceptions=True, the first exception will propagate")
print("- Allows for handling all exceptions after all tasks complete")

async def gather_exception_demo():
    print("\nException handling with gather():")
    
    # Define coroutines, some of which will fail
    async def success_coro(id):
        await asyncio.sleep(random.uniform(0.1, 0.5))
        return f"Success {id}"
    
    async def fail_coro(id, error_msg):
        await asyncio.sleep(random.uniform(0.1, 0.5))
        raise ValueError(f"Error in {id}: {error_msg}")
    
    # Create a mix of successful and failing coroutines
    coroutines = [
        success_coro(1),
        fail_coro(2, "Something went wrong"),
        success_coro(3),
        fail_coro(4, "Another error")
    ]
    
    # Method 1: gather with return_exceptions=True
    print("\nGather with return_exceptions=True:")
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i+1} raised exception: {result}")
        else:
            print(f"Task {i+1} succeeded with result: {result}")
    
    # Method 2: gather with return_exceptions=False (default)
    print("\nGather with return_exceptions=False (default):")
    try:
        results = await asyncio.gather(
            success_coro(5),
            fail_coro(6, "This will halt all other tasks"),
            success_coro(7)
        )
        print("This line won't execute due to the exception")
    except ValueError as e:
        print(f"Gather failed with first exception: {e}")
        print("Other tasks were still running but their results are lost")

# Run the gather exception demo
print("\nDemonstrating exception handling with gather():")
asyncio.run(gather_exception_demo())

# 4. EXCEPTION HANDLING WITH WAIT
print("\n4. Exception Handling with wait()")
print("------------------------------")
print("- wait() returns done and pending tasks")
print("- Exceptions are stored in the task objects")
print("- Access exceptions with task.exception()")
print("- More granular control over exception handling")

async def wait_exception_demo():
    print("\nException handling with wait():")
    
    # Create several tasks, some will fail
    tasks = [
        asyncio.create_task(asyncio.sleep(0.5, result=f"Result {i}"))
        for i in range(1, 4)
    ]
    
    # Add a failing task
    async def failing_task():
        await asyncio.sleep(0.3)
        raise RuntimeError("Task deliberately failed")
    
    tasks.append(asyncio.create_task(failing_task()))
    
    # Wait for all tasks to complete or fail
    done, pending = await asyncio.wait(tasks)
    
    # Process completed tasks
    print(f"Completed tasks: {len(done)}")
    for i, task in enumerate(done):
        try:
            result = task.result()
            print(f"Task {i+1} succeeded: {result}")
        except Exception as e:
            print(f"Task {i+1} failed: {e}")

# Run the wait exception demo
print("\nDemonstrating exception handling with wait():")
asyncio.run(wait_exception_demo())

# 5. HANDLING ASYNCIO-SPECIFIC EXCEPTIONS
print("\n5. Handling AsyncIO-Specific Exceptions")
print("------------------------------------")
print("- CancelledError: Raised when a task is cancelled")
print("- TimeoutError: Raised when an operation times out")
print("- InvalidStateError: Raised when an operation is not valid for the current state")

async def asyncio_exceptions_demo():
    print("\nHandling asyncio-specific exceptions:")
    
    # 1. TimeoutError
    print("\nHandling TimeoutError:")
    async def slow_operation():
        await asyncio.sleep(2)
        return "This result won't be seen"
    
    try:
        # Wait for at most 1 second
        result = await asyncio.wait_for(slow_operation(), timeout=1.0)
        print(f"Result: {result}")
    except asyncio.TimeoutError:
        print("Operation timed out")
    
    # 2. CancelledError
    print("\nHandling CancelledError:")
    
    async def cancellable_operation():
        try:
            print("Operation started")
            await asyncio.sleep(2)
            return "Operation completed"
        except asyncio.CancelledError:
            print("Operation was cancelled, cleaning up...")
            # Perform cleanup here
            raise  # Re-raise to propagate cancellation
    
    task = asyncio.create_task(cancellable_operation())
    await asyncio.sleep(0.5)
    
    # Cancel the task
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("Task was cancelled successfully")
    
    # 3. InvalidStateError
    print("\nHandling InvalidStateError:")
    
    # Create a future and try to set its result twice
    future = asyncio.Future()
    future.set_result("First result")
    
    try:
        future.set_result("Second result")
    except asyncio.InvalidStateError:
        print("Cannot set result on a future that's already done")

# Run the asyncio exceptions demo
print("\nDemonstrating asyncio-specific exceptions:")
asyncio.run(asyncio_exceptions_demo())

# 6. PROPAGATING EXCEPTIONS BETWEEN COROUTINES
print("\n6. Propagating Exceptions Between Coroutines")
print("-----------------------------------------")
print("- Exceptions propagate through the 'await' chain")
print("- Nested coroutines pass exceptions to their caller")
print("- Choose appropriate levels for handling exceptions")

async def propagation_demo():
    print("\nException propagation between coroutines:")
    
    async def level3():
        print("Level 3: Raising exception")
        raise ValueError("Error in deepest level")
    
    async def level2():
        print("Level 2: Calling deeper level")
        try:
            await level3()
        except ValueError as e:
            print(f"Level 2: Caught exception: {e}")
            raise RuntimeError("Converted to different exception") from e
    
    async def level1():
        print("Level 1: Calling deeper level")
        await level2()
    
    try:
        await level1()
    except Exception as e:
        print(f"Top level: Caught exception: {e}")
        print(f"Original cause: {e.__cause__}")

# Run the propagation demo
print("\nDemonstrating exception propagation:")
asyncio.run(propagation_demo())

# 7. HANDLING EXCEPTIONS WITH CONTEXT MANAGERS
print("\n7. Handling Exceptions with Context Managers")
print("----------------------------------------")
print("- async with can handle exceptions in __aexit__")
print("- Good for resource management and cleanup")
print("- Can decide whether to suppress exceptions")

class DatabaseConnection:
    """Simulated async database connection with error handling"""
    
    async def __aenter__(self):
        print("Opening database connection")
        await asyncio.sleep(0.1)  # Simulate connection time
        self.connection = {"status": "connected"}
        return self.connection
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing database connection. Exception: {exc_type}")
        if self.connection:
            await asyncio.sleep(0.1)  # Simulate cleanup
            self.connection = None
        
        if exc_type is ValueError:
            print("Suppressing ValueError")
            return True  # Suppress the exception
            
        # Don't suppress other exceptions
        return False

async def context_manager_demo():
    print("\nException handling with context managers:")
    
    # Case 1: No exception
    print("\nCase 1: No exception:")
    async with DatabaseConnection() as conn:
        print(f"Connection established: {conn}")
        await asyncio.sleep(0.1)
        print("Operation completed successfully")
    
    # Case 2: ValueError (will be suppressed)
    print("\nCase 2: ValueError (will be suppressed):")
    async with DatabaseConnection() as conn:
        print(f"Connection established: {conn}")
        await asyncio.sleep(0.1)
        raise ValueError("Database query error")
    print("Execution continues after suppressed exception")
    
    # Case 3: RuntimeError (will propagate)
    print("\nCase 3: RuntimeError (will propagate):")
    try:
        async with DatabaseConnection() as conn:
            print(f"Connection established: {conn}")
            await asyncio.sleep(0.1)
            raise RuntimeError("Serious error")
    except RuntimeError as e:
        print(f"Caught RuntimeError: {e}")

# Run the context manager demo
print("\nDemonstrating exception handling with context managers:")
asyncio.run(context_manager_demo())

# 8. DEBUGGING ASYNCHRONOUS EXCEPTIONS
print("\n8. Debugging Asynchronous Exceptions")
print("---------------------------------")
print("- Asynchronous traceback can be confusing")
print("- Use asyncio debug mode for better diagnostics")
print("- Consider structured logging for async operations")
print("- Techniques for finding the root cause")

async def debug_demo():
    print("\nDebugging asynchronous exceptions:")
    
    # Helper to capture and print exception traceback
    def print_exception_details(e):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(f"Exception type: {exc_type.__name__}")
        print(f"Exception message: {exc_value}")
        print("Traceback:")
        traceback_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for line in traceback_lines:
            print(f"  {line}", end="")
    
    # Create a nested structure of coroutines with an exception
    async def nested_function():
        await asyncio.sleep(0.1)
        raise ValueError("Something went wrong in nested function")
    
    async def middle_function():
        try:
            await nested_function()
        except ValueError:
            print("\nRe-raising with traceback:")
            raise  # Re-raise preserves traceback
    
    # Demonstrate exception details
    try:
        await middle_function()
    except Exception as e:
        print_exception_details(e)
    
    # Demonstrate asyncio debug mode
    print("\nEnabling asyncio debug mode can help with diagnostics")
    print("Set by: asyncio.run(main(), debug=True)")
    print("Or environment variable: PYTHONASYNCIODEBUG=1")

# Run the debug demo
print("\nDemonstrating exception debugging:")
asyncio.run(debug_demo())

# 9. BEST PRACTICES FOR ERROR HANDLING
print("\n9. Best Practices for Error Handling")
print("---------------------------------")
print("- Always await tasks or ensure they're properly collected")
print("- Use appropriate granularity for exception handling")
print("- Log detailed error information in production code")
print("- Design for failures - assume things will go wrong")
print("- Consider retry mechanisms for transient failures")
print("- Fail fast and gracefully for unrecoverable errors")

async def best_practices_demo():
    print("\nBest practices demonstration:")
    
    # Example: Retry mechanism for transient failures
    async def unreliable_operation():
        if random.random() < 0.7:  # 70% chance of failure
            await asyncio.sleep(0.1)
            raise ConnectionError("Temporary connection error")
        await asyncio.sleep(0.2)
        return "Operation succeeded"
    
    async def with_retry(coro_func, max_attempts=3, base_delay=1.0):
        """Retry a coroutine with exponential backoff"""
        last_exception = None
        for attempt in range(max_attempts):
            try:
                result = await coro_func()
                print(f"Succeeded on attempt {attempt + 1}")
                return result
            except Exception as e:
                last_exception = e
                if attempt < max_attempts - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"Attempt {attempt + 1} failed: {e}, retrying in {delay}s")
                    await asyncio.sleep(delay)
                else:
                    print(f"All {max_attempts} attempts failed")
        
        # Re-raise the last exception
        raise last_exception
    
    try:
        result = await with_retry(unreliable_operation, max_attempts=4)
        print(f"Final result: {result}")
    except Exception as e:
        print(f"Operation failed after retries: {e}")
    
    # Example: Graceful shutdown with cancellation
    print("\nGraceful shutdown example:")
    async def cleanup_resources():
        print("Cleaning up resources...")
        await asyncio.sleep(0.2)
        print("Cleanup complete")
    
    async def long_running_task():
        try:
            print("Task started")
            await asyncio.sleep(10)  # Long operation
            return "Task completed"
        except asyncio.CancelledError:
            print("Task cancelled, performing cleanup...")
            await cleanup_resources()
            raise  # Re-raise cancellation to signal completion
    
    task = asyncio.create_task(long_running_task())
    
    # Let the task start
    await asyncio.sleep(0.5)
    
    # Initiate cancellation
    print("Initiating cancellation")
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("Task was cancelled and cleanup was performed")

# Run the best practices demo
print("\nDemonstrating error handling best practices:")
asyncio.run(best_practices_demo())
