import asyncio
import inspect
import types
import time

# 1. FROM GENERATORS TO COROUTINES
print("\n1. The Evolution: From Generators to Coroutines")
print("---------------------------------------------")
print("Python's coroutines evolved from generators:")
print("1. Python 2.5 (2006): Simple generators with 'yield'")
print("2. Python 3.3 (2012): 'yield from' for delegation")
print("3. Python 3.4 (2014): @asyncio.coroutine decorator with generators")
print("4. Python 3.5 (2015): Native coroutines with 'async/await'")

# Generator-based coroutine (older style)
@asyncio.coroutine
def old_style_coroutine():
    """Generator-based coroutine (Python 3.4 style)"""
    print("Old-style coroutine starting")
    yield from asyncio.sleep(1)
    print("Old-style coroutine finished")
    return "Old result"

# Native coroutine (modern style)
async def native_coroutine():
    """Native coroutine (Python 3.5+ style)"""
    print("Native coroutine starting")
    await asyncio.sleep(1)
    print("Native coroutine finished")
    return "Native result"

print("\nComparing coroutine implementations:")
print(f"Old-style type: {type(old_style_coroutine())}")
print(f"Native type: {type(native_coroutine())}")

# 2. COROUTINE STATES
print("\n2. Coroutine States and Lifecycle")
print("-------------------------------")
print("Coroutines have several states during their lifecycle:")
print("- Created: When defined with 'async def' but not yet awaited")
print("- Awaiting: When waiting for another coroutine to complete")
print("- Running: When actively executing code")
print("- Done: When completed or raised an exception")
print("- Cancelled: When explicitly cancelled")

async def track_coroutine_state():
    print("\nDemonstrating coroutine states:")
    
    # Create a coroutine object
    coro = native_coroutine()
    print(f"1. Created coroutine: {coro}")
    
    # Wrap in a task to schedule it
    task = asyncio.create_task(coro)
    print(f"2. Scheduled as task: {task}")
    
    # Let it start running
    await asyncio.sleep(0.1)
    print(f"3. Running/Awaiting: {task}")
    
    # Wait for it to complete
    result = await task
    print(f"4. Completed with result: {result}")
    print(f"5. Final state: {task}")

# Run the state tracking coroutine
print("\nTracking coroutine states:")
asyncio.run(track_coroutine_state())

# 3. COROUTINES UNDER THE HOOD
print("\n3. Coroutines Under the Hood")
print("-------------------------")
print("Coroutines build on generator machinery:")
print("- Both can suspend and resume execution")
print("- Both maintain their local state while suspended")
print("- Both use similar implementation mechanisms")
print("- Native coroutines are optimized for async workflows")

# A simple generator for comparison
def simple_generator():
    print("Generator: started")
    yield "First"
    print("Generator: after first yield")
    yield "Second"
    print("Generator: finished")
    return "Done"  # Only reachable via exception

# A simple coroutine
async def simple_coroutine():
    print("Coroutine: started")
    await asyncio.sleep(0.1)
    print("Coroutine: after first await")
    await asyncio.sleep(0.1)
    print("Coroutine: finished")
    return "Done"  # Returned value

print("\nComparing generator and coroutine behavior:")
print("Generator step-by-step:")
gen = simple_generator()
try:
    print(f"Yield 1: {next(gen)}")
    print(f"Yield 2: {next(gen)}")
    print(f"Yield 3: {next(gen)}")  # This will raise StopIteration
except StopIteration as e:
    print(f"StopIteration with value: {e.value}")

print("\nCoroutine execution:")
asyncio.run(simple_coroutine())

# 4. INSPECTING COROUTINES
print("\n4. Inspecting Coroutines")
print("---------------------")

async def sample_coroutine():
    await asyncio.sleep(1)
    return "Result"

coro = sample_coroutine()

print("\nInspecting a coroutine object:")
print(f"Type: {type(coro)}")
print(f"Is coroutine: {asyncio.iscoroutine(coro)}")
print(f"Is coroutine function: {asyncio.iscoroutinefunction(sample_coroutine)}")
print(f"Is generator: {isinstance(coro, types.GeneratorType)}")
print(f"Coroutine attributes: {dir(coro)[:5]} ...")
print(f"Coroutine repr: {repr(coro)}")

# Clean up the coroutine to avoid runtime warning
coro.close()

# 5. COOPERATIVE SCHEDULING
print("\n5. Cooperative Scheduling with Coroutines")
print("--------------------------------------")
print("Coroutines use cooperative multitasking:")
print("- Each coroutine must explicitly yield control with 'await'")
print("- The event loop decides which coroutine to run next")
print("- Long-running operations without awaits block everything")

# Good coroutine - yields control
async def good_coroutine():
    print("Good coroutine: starting work")
    for i in range(3):
        print(f"Good coroutine: doing step {i}")
        await asyncio.sleep(0.01)  # Yields control back to event loop
    print("Good coroutine: finished")
    return "Good result"

# Bad coroutine - doesn't yield control
async def bad_coroutine():
    print("Bad coroutine: starting CPU-intensive work")
    print("Bad coroutine: calculating...")
    # CPU-bound work that doesn't yield control
    sum_val = 0
    for i in range(10_000_000):
        sum_val += i
    print(f"Bad coroutine: finished calculation, sum={sum_val}")
    return "Bad result"

async def demonstrate_cooperation():
    # Run both concurrently
    good_task = asyncio.create_task(good_coroutine())
    bad_task = asyncio.create_task(bad_coroutine())
    
    # Wait for both to complete
    results = await asyncio.gather(good_task, bad_task)
    return results

print("\nDemonstrating cooperative scheduling:")
print("Notice how the bad coroutine blocks the good one:")
start = time.time()
coop_results = asyncio.run(demonstrate_cooperation())
end = time.time()
print(f"Total time: {end - start:.2f}s")
print(f"Results: {coop_results}")

# 6. AWAIT EXPLAINED
print("\n6. Understanding the 'await' Keyword")
print("--------------------------------")
print("The 'await' keyword:")
print("- Pauses execution of the current coroutine")
print("- Yields control back to the event loop")
print("- Waits for the awaitable to complete")
print("- Extracts the result or propagates exceptions")
print("- Can only be used inside an async function")

# What can be awaited?
print("\nThings that can be awaited:")
print("1. Coroutine objects created from async functions")
print("2. Tasks created with asyncio.create_task()")
print("3. Futures from low-level APIs")
print("4. Objects implementing the __await__ method")

async def demonstrate_awaitable_types():
    # 1. Awaiting a coroutine
    print("\nAwaiting a coroutine:")
    result1 = await native_coroutine()
    print(f"Got result: {result1}")
    
    # 2. Awaiting a task
    print("\nAwaiting a task:")
    task = asyncio.create_task(native_coroutine())
    result2 = await task
    print(f"Got result: {result2}")
    
    # 3. Creating a custom awaitable
    print("\nAwaiting a custom awaitable:")
    
    class CustomAwaitable:
        def __await__(self):
            # Must return an iterator
            async def async_work():
                await asyncio.sleep(0.5)
                return "Custom result"
            return async_work().__await__()
    
    result3 = await CustomAwaitable()
    print(f"Got result: {result3}")
    
    return [result1, result2, result3]

print("\nDemonstrating different awaitable types:")
awaitable_results = asyncio.run(demonstrate_awaitable_types())
print(f"All results: {awaitable_results}")

# 7. BEST PRACTICES FOR COROUTINES
print("\n7. Coroutine Best Practices")
print("------------------------")
print("1. Always await coroutines - never leave them hanging")
print("2. Use asyncio.create_task() for fire-and-forget operations")
print("3. Group related coroutines with asyncio.gather()")
print("4. Handle exceptions properly in async code")
print("5. Avoid CPU-intensive operations in coroutines")
print("6. Use asyncio.shield() to protect critical operations from cancellation")
print("7. Name your tasks for easier debugging")

# Example of good practices
async def demonstrate_best_practices():
    print("\nDemonstrating coroutine best practices:")
    
    # Named tasks for better debugging
    task1 = asyncio.create_task(
        task_with_delay(1, 0.5),
        name="important-task-1"
    )
    
    # Proper error handling
    try:
        async with asyncio.timeout(1):
            result = await task1
        print(f"Task completed with result: {result}")
    except asyncio.TimeoutError:
        print("Task timed out")
        # Proper cleanup
        if not task1.done():
            task1.cancel()
            try:
                await task1
            except asyncio.CancelledError:
                pass
    
    return "Best practices demonstrated"

async def task_with_delay(task_id, delay):
    await asyncio.sleep(delay)
    return f"Task {task_id} result"

print("\nRunning best practices demo:")
asyncio.run(demonstrate_best_practices())

print("\n--- Exercise ---")
print("1. Create a custom awaitable class that can be used with the await keyword.")
print("2. Implement a technique to run a CPU-bound operation without blocking the event loop.")