import asyncio
import random
import time
from typing import List, Dict, Any

# 1. UNDERSTANDING TASKS AND FUTURES
print("\n1. Understanding Tasks and Futures")
print("-------------------------------")
print("Tasks:")
print("- High-level wrappers for coroutines")
print("- Schedule coroutines to run on the event loop")
print("- Can be awaited, cancelled, and monitored for completion")
print("- Subclass of Future")

print("\nFutures:")
print("- Low-level awaitable objects representing eventual results")
print("- Can be in various states: pending, cancelled, or done")
print("- Store results or exceptions once complete")
print("- Rarely created directly in asyncio (used internally)")

# 2. CREATING AND MANAGING TASKS
print("\n2. Creating and Managing Tasks")
print("---------------------------")

async def background_task(name, delay):
    """A simple coroutine we'll turn into a task"""
    print(f"Task {name}: starting, will take {delay}s")
    await asyncio.sleep(delay)
    print(f"Task {name}: completed after {delay}s")
    return f"Result from {name}"

async def demonstrate_task_creation():
    print("\nCreating and managing tasks:")
    
    # Method 1: create_task (preferred way since Python 3.7)
    task1 = asyncio.create_task(
        background_task("A", 2),
        name="task-A"  # Optional name (Python 3.8+)
    )
    
    # Method 2: ensure_future (older method, still works)
    task2 = asyncio.ensure_future(background_task("B", 1))
    
    print(f"Task 1 created: {task1}")
    print(f"Task 1 name: {task1.get_name() if hasattr(task1, 'get_name') else 'unnamed'}")
    print(f"Task 1 done? {task1.done()}")
    
    # Let's do other work while the tasks run
    print("Main coroutine: doing other work...")
    await asyncio.sleep(0.5)
    
    # Check on the tasks
    print(f"Task 1 done now? {task1.done()}")
    print(f"Task 2 done now? {task2.done()}")
    
    # Wait for tasks to complete
    results = await asyncio.gather(task1, task2)
    print(f"All tasks completed with results: {results}")
    
    # Creating a task that's already done
    completed_task = asyncio.create_task(asyncio.sleep(0))
    await completed_task
    print(f"Completed task: {completed_task}, done? {completed_task.done()}")

# Run the task creation demo
print("\nDemonstrating task creation and management:")
asyncio.run(demonstrate_task_creation())

# 3. WORKING WITH MULTIPLE TASKS
print("\n3. Working with Multiple Tasks")
print("---------------------------")
print("Key functions for working with task groups:")
print("- gather(): Run tasks concurrently and wait for all to complete")
print("- wait(): Wait for tasks to complete with more control")
print("- as_completed(): Process tasks as they complete (any order)")
print("- TaskGroup: Structured concurrency (Python 3.11+)")

async def task_with_random_delay(task_id):
    """Task that completes after a random delay"""
    delay = random.uniform(0.5, 3)
    print(f"Task {task_id}: starting (delay: {delay:.2f}s)")
    await asyncio.sleep(delay)
    print(f"Task {task_id}: finished")
    return f"Result {task_id} (took {delay:.2f}s)"

async def demonstrate_gather():
    """Demonstrate asyncio.gather() for waiting on multiple tasks"""
    print("\nUsing asyncio.gather():")
    
    # Create a list of coroutines
    coroutines = [task_with_random_delay(i) for i in range(1, 6)]
    
    # Wait for all to complete
    print("Waiting for all tasks...")
    start = time.time()
    results = await asyncio.gather(*coroutines)
    elapsed = time.time() - start
    
    print(f"All tasks completed in {elapsed:.2f}s")
    print(f"Results: {results}")
    
    # Handling exceptions with gather
    print("\nHandling exceptions with gather:")
    
    async def failing_task():
        await asyncio.sleep(0.5)
        raise ValueError("This task failed!")
    
    # With return_exceptions=True
    try:
        results = await asyncio.gather(
            task_with_random_delay(10),
            failing_task(),
            task_with_random_delay(11),
            return_exceptions=True
        )
        print(f"Results with return_exceptions=True: {results}")
        print("Notice the exception object in the results")
    except Exception as e:
        print(f"This won't execute because we caught the exception: {e}")
    
    # With return_exceptions=False (default)
    try:
        results = await asyncio.gather(
            task_with_random_delay(20),
            failing_task(),
            task_with_random_delay(21)
        )
        print("This line won't execute")
    except Exception as e:
        print(f"Exception propagated with return_exceptions=False: {e}")

# Run the gather demo
print("\nDemonstrating asyncio.gather():")
asyncio.run(demonstrate_gather())

async def demonstrate_wait():
    """Demonstrate asyncio.wait() for waiting on multiple tasks"""
    print("\nUsing asyncio.wait():")
    
    # Create tasks
    tasks = [
        asyncio.create_task(task_with_random_delay(i)) 
        for i in range(1, 6)
    ]
    
    # Wait for all tasks to complete or timeout
    print("Waiting for all tasks or timeout...")
    done, pending = await asyncio.wait(
        tasks,
        timeout=2.0  # Wait at most 2 seconds
    )
    
    print(f"Completed tasks: {len(done)}")
    print(f"Pending tasks: {len(pending)}")
    
    # Get results from completed tasks
    for task in done:
        try:
            result = task.result()
            print(f"Task result: {result}")
        except Exception as e:
            print(f"Task raised {type(e).__name__}: {e}")
    
    # Cancel any pending tasks
    for task in pending:
        print(f"Cancelling {task}")
        task.cancel()
    
    # Wait for the pending tasks to be cancelled
    if pending:
        await asyncio.wait(pending)
        print("All pending tasks cancelled")
    
    # Wait with FIRST_COMPLETED
    print("\nWaiting for first task to complete:")
    tasks = [
        asyncio.create_task(task_with_random_delay(i)) 
        for i in range(10, 15)
    ]
    
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED
    )
    
    print(f"First task completed: {done}")
    for task in done:
        print(f"Result: {task.result()}")
    
    # Cancel remaining tasks
    for task in pending:
        task.cancel()
    await asyncio.wait(pending)

# Run the wait demo
print("\nDemonstrating asyncio.wait():")
asyncio.run(demonstrate_wait())

async def demonstrate_as_completed():
    """Demonstrate asyncio.as_completed() for processing tasks as they finish"""
    print("\nUsing asyncio.as_completed():")
    
    # Create tasks with different delays
    tasks = [
        task_with_random_delay(i) 
        for i in range(1, 6)
    ]
    
    # Process tasks as they complete (in completion order, not creation order)
    for i, future in enumerate(asyncio.as_completed(tasks), 1):
        result = await future
        print(f"Finished task #{i}: {result}")

# Run the as_completed demo
print("\nDemonstrating asyncio.as_completed():")
asyncio.run(demonstrate_as_completed())

async def demonstrate_task_group():
    """Demonstrate TaskGroup (Python 3.11+) for structured concurrency"""
    print("\nUsing TaskGroup (Python 3.11+):")
    
    try:
        # Check if running on Python 3.11+
        if not hasattr(asyncio, "TaskGroup"):
            print("TaskGroup not available (requires Python 3.11+)")
            return
        
        async with asyncio.TaskGroup() as tg:
            # Create tasks within the group
            task1 = tg.create_task(task_with_random_delay(1))
            task2 = tg.create_task(task_with_random_delay(2))
            task3 = tg.create_task(task_with_random_delay(3))
            
            # All tasks will be awaited when the context exits
            print("Tasks created within TaskGroup")
        
        # At this point, all tasks are guaranteed to be done
        print("All tasks in the group completed")
        print(f"Results: {[task1.result(), task2.result(), task3.result()]}")
        
    except (ImportError, AttributeError):
        print("Failed to use TaskGroup - likely not on Python 3.11+")

# Run the TaskGroup demo if possible
print("\nDemonstrating TaskGroup (if available):")
asyncio.run(demonstrate_task_group())

# 4. TASK CANCELLATION AND TIMEOUTS
print("\n4. Task Cancellation and Timeouts")
print("------------------------------")

async def cancellable_task():
    """A task that can be cancelled, with cleanup"""
    try:
        print("Cancellable task: starting")
        for i in range(10):
            print(f"Cancellable task: working ({i+1}/10)")
            try:
                await asyncio.sleep(0.5)  # This can be interrupted by cancellation
            except asyncio.CancelledError:
                print("Cancellable task: sleep was cancelled, re-raising")
                raise  # Re-raise to propagate cancellation
    except asyncio.CancelledError:
        print("Cancellable task: cancelled, cleaning up...")
        await asyncio.sleep(0.5)  # Cleanup operation
        print("Cancellable task: cleanup complete")
        raise  # Re-raise to signal we've been cancelled
    finally:
        print("Cancellable task: in finally block")
    
    return "Task completed normally"

async def demonstrate_cancellation():
    """Demonstrate task cancellation"""
    print("\nCancelling a task:")
    
    # Create a task
    task = asyncio.create_task(cancellable_task())
    
    # Let it run for a bit
    await asyncio.sleep(1.5)
    
    # Then cancel it
    print("Main: cancelling the task")
    task.cancel()
    
    try:
        await task
        print("This line won't execute if task is cancelled")
    except asyncio.CancelledError:
        print("Main: task was cancelled successfully")
    
    print(f"Task cancelled? {task.cancelled()}")

# Run the cancellation demo
print("\nDemonstrating task cancellation:")
asyncio.run(demonstrate_cancellation())

async def demonstrate_timeout():
    """Demonstrate asyncio timeouts"""
    print("\nUsing timeouts:")
    
    # Method 1: wait_for
    print("\nUsing asyncio.wait_for():")
    try:
        # Wait for at most 1 second
        result = await asyncio.wait_for(
            task_with_random_delay(100),  # This would take 0.5-3s
            timeout=1.0
        )
        print(f"Task completed within timeout: {result}")
    except asyncio.TimeoutError:
        print("Task timed out after 1 second")
    
    # Method 2: timeout context manager (Python 3.11+)
    print("\nUsing asyncio.timeout() context manager (Python 3.11+):")
    try:
        if hasattr(asyncio, "timeout"):
            async with asyncio.timeout(1.0):
                # This will time out if it takes more than 1 second
                result = await task_with_random_delay(200)
                print(f"Task completed within timeout: {result}")
        else:
            print("asyncio.timeout() not available (requires Python 3.11+)")
    except asyncio.TimeoutError:
        print("Task timed out after 1 second")

# Run the timeout demo
print("\nDemonstrating timeouts:")
asyncio.run(demonstrate_timeout())

# 5. HANDLING EXCEPTIONS IN TASKS
print("\n5. Handling Exceptions in Tasks")
print("----------------------------")

async def task_that_fails(task_id):
    """A task that raises an exception"""
    await asyncio.sleep(0.5)
    if task_id % 2 == 0:
        raise ValueError(f"Task {task_id} failed deliberately")
    return f"Task {task_id} succeeded"

async def demonstrate_exception_handling():
    """Demonstrate handling exceptions in tasks"""
    print("\nHandling exceptions in tasks:")
    
    # Method 1: Try-except when awaiting
    task = asyncio.create_task(task_that_fails(2))
    try:
        result = await task
        print(f"Task result: {result}")
    except ValueError as e:
        print(f"Caught exception: {e}")
    
    # Method 2: Check for exception with result()
    task = asyncio.create_task(task_that_fails(4))
    # Let the task complete
    await asyncio.sleep(1)
    
    try:
        result = task.result()  # This will re-raise the exception
        print(f"Task result: {result}")
    except ValueError as e:
        print(f"Caught exception from result(): {e}")
    
    # Method 3: exception() to get the exception without raising
    task = asyncio.create_task(task_that_fails(6))
    await asyncio.sleep(1)
    
    if task.done() and not task.cancelled():
        exception = task.exception()
        if exception:
            print(f"Task had exception: {exception}")
        else:
            print(f"Task completed successfully: {task.result()}")
    
    # Method 4: gather with return_exceptions
    tasks = [
        task_that_fails(i) for i in range(1, 5)
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i+1} failed: {result}")
        else:
            print(f"Task {i+1} succeeded: {result}")

# Run the exception handling demo
print("\nDemonstrating exception handling in tasks:")
asyncio.run(demonstrate_exception_handling())