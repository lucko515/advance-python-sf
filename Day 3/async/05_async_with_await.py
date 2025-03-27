# 05: Working with Async/Await Syntax
print("Advanced Async/Await Syntax")
print("-------------------------")

import asyncio
import time
import random

# 1. ASYNC CONTEXT MANAGERS
print("\n1. Async Context Managers with 'async with'")
print("----------------------------------------")

class AsyncTimer:
    """A context manager that times async code execution"""
    
    def __init__(self, name):
        self.name = name
        self.start_time = None
    
    async def __aenter__(self):
        print(f"Starting timer '{self.name}'")
        self.start_time = time.time()
        await asyncio.sleep(0.1)  # Simulating async setup work
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        elapsed = end_time - self.start_time
        await asyncio.sleep(0.1)  # Simulating async cleanup work
        print(f"Timer '{self.name}' finished: {elapsed:.2f} seconds")
        return False  # Don't suppress exceptions
    
    def elapsed(self):
        """Get current elapsed time without exiting the context"""
        if self.start_time is None:
            return 0
        return time.time() - self.start_time

async def demonstrate_async_context_manager():
    async with AsyncTimer("example operation") as timer:
        print(f"Inside the context, elapsed: {timer.elapsed():.2f}s")
        await asyncio.sleep(0.5)
        print(f"Still inside, elapsed: {timer.elapsed():.2f}s")

# 2. ASYNC ITERATORS AND FOR LOOPS
print("\n2. Async Iterators and 'async for' Loops")
print("-------------------------------------")

class AsyncRange:
    """Asynchronous version of range()"""
    
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
        
    def __aiter__(self):
        return self
        
    async def __anext__(self):
        if self.start >= self.stop:
            raise StopAsyncIteration
        await asyncio.sleep(0.1)
        value = self.start
        self.start += 1
        return value

async def demonstrate_async_iterator():
    async for i in AsyncRange(1, 5):
        print(f"Got value: {i}")
    
    # Using async comprehension
    results = [i async for i in AsyncRange(5, 9)]
    print(f"Collected results: {results}")

# 3. ASYNC GENERATORS
print("\n3. Async Generators")
print("----------------")

async def async_countdown(start):
    """An async generator that counts down from start to 1"""
    print(f"Starting countdown from {start}")
    
    for i in range(start, 0, -1):
        await asyncio.sleep(0.2)
        yield i

async def demonstrate_async_generator():
    async for num in async_countdown(5):
        print(f"Countdown: {num}")

# 4. ASYNC COMPREHENSIONS
print("\n4. Async Comprehensions")
print("--------------------")

async def demonstrate_async_comprehensions():
    # Async list comprehension
    numbers = [i async for i in AsyncRange(1, 6)]
    print(f"List comprehension: {numbers}")
    
    # Async dict comprehension
    mapping = {f"key-{i}": i*i async for i in AsyncRange(1, 5)}
    print(f"Dict comprehension: {mapping}")
    
    # With if-expressions
    even_squares = [i*i async for i in AsyncRange(1, 10) if i % 2 == 0]
    print(f"Even squares: {even_squares}")

# 5. ASYNC METHODS IN CLASSES
print("\n5. Async Methods in Classes")
print("------------------------")

class DataFetcher:
    """A class demonstrating async methods"""
    
    def __init__(self, base_url="https://api.example.com"):
        self.base_url = base_url
        self._cache = {}
        
    async def fetch_data(self, endpoint):
        """Async method to fetch data from an API endpoint"""
        url = f"{self.base_url}/{endpoint}"
        
        # Check cache first
        if url in self._cache:
            print(f"Cache hit for {url}")
            return self._cache[url]
        
        # Simulate API request
        print(f"Fetching {url}...")
        await asyncio.sleep(0.5)  # Simulate network delay
        
        # Simulate response data
        data = {
            "endpoint": endpoint,
            "timestamp": time.time(),
            "value": random.randint(1, 100)
        }
        
        # Cache the result
        self._cache[url] = data
        return data
    
    @property
    def cache_size(self):
        """Synchronous property - works normally"""
        return len(self._cache)

async def demonstrate_async_class_methods():
    fetcher = DataFetcher()
    data1 = await fetcher.fetch_data("users")
    print(f"Fetched data: {data1}")
    print(f"Cache size: {fetcher.cache_size}")
    data2 = await fetcher.fetch_data("products")
    print(f"Fetched more data: {data2}")

# 6. BRIDGING SYNC AND ASYNC CODE
print("\n6. Bridging Synchronous and Asynchronous Code")
print("------------------------------------------")

async def demonstrate_bridging():
    # Synchronous function we want to call from async context
    def slow_computation(n):
        print(f"Starting computation with n={n}")
        result = 0
        for i in range(n):
            result += i * i
        print("Computation finished")
        return result
    
    # Run in executor to avoid blocking
    loop = asyncio.get_running_loop()
    print("Using run_in_executor:")
    result = await loop.run_in_executor(None, slow_computation, 10000)
    print(f"Result: {result}")

# Main demo function
async def main():
    print("\nDemonstrating async context managers:")
    await demonstrate_async_context_manager()
    
    print("\nDemonstrating async iteration:")
    await demonstrate_async_iterator()
    
    print("\nDemonstrating async generators:")
    await demonstrate_async_generator()
    
    print("\nDemonstrating async comprehensions:")
    await demonstrate_async_comprehensions()
    
    print("\nDemonstrating async class methods:")
    await demonstrate_async_class_methods()
    
    print("\nDemonstrating sync/async code bridging:")
    await demonstrate_bridging()

# Run all demos
print("Running all async/await demos:")
asyncio.run(main())