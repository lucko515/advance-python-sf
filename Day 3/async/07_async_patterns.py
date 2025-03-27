import asyncio
import random
import time
from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass

# 1. PRODUCER-CONSUMER PATTERN
print("\n1. Producer-Consumer Pattern")
print("-------------------------")
print("- Producer generates data asynchronously")
print("- Queue buffers data between producer and consumer")
print("- Consumer processes data as it becomes available")
print("- Decouples data production from consumption")
print("- Controls flow between fast producers and slow consumers")

async def producer(queue: asyncio.Queue, items: int):
    """Produces items and puts them in the queue"""
    for i in range(items):
        # Simulate variable production time
        await asyncio.sleep(random.uniform(0.1, 0.5))
        item = f"Item {i}"
        
        # Put the item in the queue
        await queue.put(item)
        print(f"Produced {item}")
    
    # Signal that production is complete
    await queue.put(None)
    print("Producer finished")

async def consumer(queue: asyncio.Queue):
    """Consumes items from the queue"""
    while True:
        # Wait for an item from the queue
        item = await queue.get()
        
        # None is our signal to stop
        if item is None:
            break
            
        # Simulate variable processing time
        await asyncio.sleep(random.uniform(0.2, 0.7))
        print(f"Consumed {item}")
        
        # Mark the task as done
        queue.task_done()
    
    print("Consumer finished")

async def demonstrate_producer_consumer():
    # Create a queue
    queue = asyncio.Queue(maxsize=5)  # Limit queue size to control memory usage
    
    # Create producer and consumer tasks
    producer_task = asyncio.create_task(producer(queue, 10))
    consumer_task = asyncio.create_task(consumer(queue))
    
    # Wait for both tasks to complete
    await producer_task
    await consumer_task
    
    print("Producer-consumer demo completed")

# 2. WORKER POOL PATTERN
print("\n2. Worker Pool Pattern")
print("-------------------")
print("- Fixed pool of workers processes tasks concurrently")
print("- Tasks are distributed among workers")
print("- Controls level of concurrency")
print("- Good for CPU or I/O intensive operations")

async def worker(name: str, queue: asyncio.Queue):
    """Worker that processes tasks from the queue"""
    while True:
        # Get a task from the queue
        task = await queue.get()
        
        # None signals worker to exit
        if task is None:
            print(f"Worker {name} shutting down")
            queue.task_done()
            break
        
        # Process the task
        print(f"Worker {name} started processing task: {task}")
        await asyncio.sleep(random.uniform(0.5, 2.0))  # Simulate processing
        print(f"Worker {name} completed task: {task}")
        
        # Mark the task as done
        queue.task_done()

async def submit_tasks(queue: asyncio.Queue, num_tasks: int):
    """Submit tasks to the queue"""
    for i in range(num_tasks):
        task = f"Task {i}"
        await queue.put(task)
        print(f"Submitted {task}")
        
        # Small delay between task submissions
        await asyncio.sleep(random.uniform(0.1, 0.3))

async def demonstrate_worker_pool():
    # Create a queue
    queue = asyncio.Queue()
    
    # Number of workers in the pool
    num_workers = 3
    
    # Start workers
    workers = [asyncio.create_task(worker(f"Worker-{i}", queue)) 
               for i in range(num_workers)]
    
    # Submit tasks
    await submit_tasks(queue, 10)
    
    # Wait for all tasks to be processed
    await queue.join()
    
    # Send shutdown signal to workers
    for _ in range(num_workers):
        await queue.put(None)
    
    # Wait for all workers to shut down
    await asyncio.gather(*workers)
    
    print("Worker pool demo completed")

# 3. SCATTER-GATHER PATTERN (MAP-REDUCE)
print("\n3. Scatter-Gather Pattern (Map-Reduce)")
print("-----------------------------------")
print("- Distribute (scatter) work across multiple coroutines")
print("- Process each piece of work concurrently")
print("- Collect (gather) results for final processing")
print("- Good for parallelizable tasks with aggregated results")

async def process_chunk(chunk: List[int]) -> int:
    """Process a chunk of data and return a result"""
    print(f"Processing chunk: {chunk}")
    await asyncio.sleep(random.uniform(0.5, 1.5))
    return sum(chunk)  # Example processing: sum the numbers

async def scatter_gather_demo(data: List[int], num_chunks: int):
    # Split the data into chunks
    chunk_size = len(data) // num_chunks
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    
    print(f"Split data into {len(chunks)} chunks")
    
    # Scatter: process each chunk concurrently
    tasks = [process_chunk(chunk) for chunk in chunks]
    results = await asyncio.gather(*tasks)
    
    # Gather: combine results (e.g., sum all the sums)
    total = sum(results)
    
    print(f"Scattered processing completed. Results: {results}")
    print(f"Gathered result: {total}")
    
    return total

async def demonstrate_scatter_gather():
    # Example: summing numbers from 1 to 100
    data = list(range(1, 101))
    result = await scatter_gather_demo(data, 5)
    print(f"Final result: {result}")

# 4. FAN-OUT/FAN-IN PATTERN
print("\n4. Fan-Out/Fan-In Pattern")
print("-----------------------")
print("- Fan-out: Single task spawns multiple related tasks")
print("- Each spawned task operates independently")
print("- Fan-in: Collect results from all tasks")
print("- Good for running the same operation against multiple items")

async def process_item(item: str) -> Dict[str, Any]:
    """Process a single item"""
    await asyncio.sleep(random.uniform(0.2, 1.0))
    return {
        "item": item,
        "timestamp": time.time(),
        "result": f"Processed {item}"
    }

async def demonstrate_fan_out_fan_in():
    items = [f"item-{i}" for i in range(10)]
    
    print("Starting fan-out phase...")
    
    # Fan-out: create a task for each item
    tasks = [asyncio.create_task(process_item(item)) for item in items]
    
    # Process other work while tasks are running
    print("Main task continues working while subtasks run...")
    await asyncio.sleep(0.5)
    
    print("Starting fan-in phase...")
    
    # Fan-in: collect all results
    results = await asyncio.gather(*tasks)
    
    print(f"All {len(results)} items processed")
    for i, result in enumerate(results[:3]):
        print(f"Sample result {i+1}: {result}")
    if len(results) > 3:
        print(f"... and {len(results) - 3} more")
    
    return results

# 5. THROTTLING AND RATE LIMITING
print("\n5. Throttling and Rate Limiting")
print("----------------------------")
print("- Limit the number of concurrent operations")
print("- Ensure fair resource usage")
print("- Respect API rate limits")
print("- Prevent system overload")

class RateLimiter:
    """Limit the rate of operations"""
    
    def __init__(self, rate_limit: int, time_period: float = 1.0):
        """
        Initialize the rate limiter
        
        Args:
            rate_limit: Maximum number of operations per time period
            time_period: Time period in seconds
        """
        self.rate_limit = rate_limit
        self.time_period = time_period
        self.tokens = rate_limit
        self.updated_at = time.time()
        self.lock = asyncio.Lock()
    
    async def acquire(self):
        """Acquire a token, waiting if necessary"""
        async with self.lock:
            # Replenish tokens based on elapsed time
            now = time.time()
            elapsed = now - self.updated_at
            self.updated_at = now
            
            self.tokens = min(
                self.rate_limit,
                self.tokens + elapsed * (self.rate_limit / self.time_period)
            )
            
            if self.tokens < 1:
                # Calculate wait time to get a token
                wait_time = (1 - self.tokens) * (self.time_period / self.rate_limit)
                await asyncio.sleep(wait_time)
                self.tokens = 0
            else:
                self.tokens -= 1

async def make_api_request(limiter: RateLimiter, request_id: int):
    """Simulate making an API request with rate limiting"""
    print(f"Request {request_id}: waiting for rate limiter...")
    await limiter.acquire()
    print(f"Request {request_id}: starting")
    
    # Simulate API request
    await asyncio.sleep(random.uniform(0.1, 0.5))
    
    print(f"Request {request_id}: completed")
    return f"Result {request_id}"

async def demonstrate_rate_limiting():
    # Create a rate limiter: 5 requests per second
    limiter = RateLimiter(rate_limit=5, time_period=1.0)
    
    # Create 20 API requests
    requests = [make_api_request(limiter, i) for i in range(20)]
    
    # Wait for all requests to complete
    results = await asyncio.gather(*requests)
    
    print(f"All {len(results)} requests completed with rate limiting")

# 6. CIRCUIT BREAKER PATTERN
print("\n6. Circuit Breaker Pattern")
print("-----------------------")
print("- Protects against failures in distributed systems")
print("- Prevents cascading failures")
print("- Gives failing services time to recover")
print("- Has three states: Closed (normal), Open (failing), Half-Open (testing)")

class CircuitBreaker:
    """Circuit breaker for protecting against service failures"""
    
    def __init__(self, 
                 failure_threshold: int = 5,
                 recovery_timeout: float = 5.0,
                 expected_exceptions: tuple = (Exception,)):
        """
        Initialize the circuit breaker
        
        Args:
            failure_threshold: Number of failures before opening the circuit
            recovery_timeout: Time in seconds before attempting recovery
            expected_exceptions: Exceptions that count as failures
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exceptions = expected_exceptions
        
        # State tracking
        self.failures = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF-OPEN
        self.last_failure_time = 0
    
    async def call(self, coro):
        """Call a coroutine with circuit breaker protection"""
        if self.state == "OPEN":
            # Check if recovery timeout has elapsed
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                print("Circuit half-open, testing service...")
                self.state = "HALF-OPEN"
            else:
                raise RuntimeError(f"Circuit breaker open, failing fast")
        
        try:
            result = await coro
            
            # Success - reset if in half-open state
            if self.state == "HALF-OPEN":
                print("Service recovered, closing circuit")
                self.failures = 0
                self.state = "CLOSED"
                
            return result
            
        except self.expected_exceptions as e:
            self.failures += 1
            self.last_failure_time = time.time()
            
            if self.state == "CLOSED" and self.failures >= self.failure_threshold:
                print(f"Failure threshold reached ({self.failures}), opening circuit")
                self.state = "OPEN"
            
            if self.state == "HALF-OPEN":
                print("Failure in half-open state, opening circuit")
                self.state = "OPEN"
                
            raise

async def unreliable_service(fail_probability: float = 0.7):
    """Simulate an unreliable service"""
    await asyncio.sleep(0.1)
    if random.random() < fail_probability:
        raise ConnectionError("Service unavailable")
    return "Service response"

async def demonstrate_circuit_breaker():
    # Create a circuit breaker
    breaker = CircuitBreaker(
        failure_threshold=3,
        recovery_timeout=2.0,
        expected_exceptions=(ConnectionError,)
    )
    
    # Make requests with circuit breaker
    for i in range(15):
        try:
            # Use a high failure probability initially, then reduce it to simulate recovery
            fail_prob = 0.8 if i < 10 else 0.2
            result = await breaker.call(unreliable_service(fail_prob))
            print(f"Request {i}: Success - {result}")
        except Exception as e:
            print(f"Request {i}: Failed - {str(e)}")
        
        # Small delay between requests
        await asyncio.sleep(0.5)

# 7. TIMEOUT PATTERNS
print("\n7. Timeout Patterns")
print("----------------")
print("- Prevent operations from hanging indefinitely")
print("- Ensure responsiveness even when services are slow")
print("- Different strategies: per-operation, cascading, and retry with backoff")

async def operation_with_timeout(timeout: float):
    """Execute an operation with a timeout"""
    try:
        # Use wait_for to timeout the operation
        result = await asyncio.wait_for(
            asyncio.sleep(random.uniform(0.5, 2.0)),  # Simulated operation
            timeout=timeout
        )
        print("Operation completed within timeout")
        return "Success"
    except asyncio.TimeoutError:
        print(f"Operation timed out after {timeout}s")
        return "Timeout"

async def retry_with_backoff(func, max_retries: int = 3, 
                             base_delay: float = 0.5, 
                             backoff_factor: float = 2.0):
    """Retry an operation with exponential backoff"""
    last_exception = None
    
    for attempt in range(max_retries + 1):
        try:
            return await func()
        except Exception as e:
            last_exception = e
            if attempt == max_retries:
                break
                
            # Calculate backoff delay
            delay = base_delay * (backoff_factor ** attempt)
            print(f"Attempt {attempt+1} failed, retrying in {delay:.2f}s")
            
            # Wait before retrying
            await asyncio.sleep(delay)
    
    raise last_exception

async def unreliable_operation():
    """A function that sometimes fails"""
    if random.random() < 0.7:
        raise ConnectionError("Service unavailable")
    return "Operation successful"

async def demonstrate_timeout_patterns():
    # Simple timeout
    print("\nSimple timeout example:")
    result1 = await operation_with_timeout(1.0)
    print(f"Result: {result1}")
    
    # Retry with backoff
    print("\nRetry with backoff example:")
    try:
        result2 = await retry_with_backoff(
            unreliable_operation,
            max_retries=5, 
            base_delay=0.5,
            backoff_factor=1.5
        )
        print(f"Result: {result2}")
    except Exception as e:
        print(f"All retries failed: {e}")

# Main demonstration function
async def main():
    # Demonstrate producer-consumer pattern
    print("\n--- PRODUCER-CONSUMER PATTERN ---")
    await demonstrate_producer_consumer()
    
    # Demonstrate worker pool pattern
    print("\n--- WORKER POOL PATTERN ---")
    await demonstrate_worker_pool()
    
    # Demonstrate scatter-gather pattern
    print("\n--- SCATTER-GATHER PATTERN ---")
    await demonstrate_scatter_gather()
    
    # Demonstrate fan-out/fan-in pattern
    print("\n--- FAN-OUT/FAN-IN PATTERN ---")
    await demonstrate_fan_out_fan_in()
    
    # Demonstrate rate limiting
    print("\n--- RATE LIMITING PATTERN ---")
    await demonstrate_rate_limiting()
    
    # Demonstrate circuit breaker pattern
    print("\n--- CIRCUIT BREAKER PATTERN ---")
    await demonstrate_circuit_breaker()
    
    # Demonstrate timeout patterns
    print("\n--- TIMEOUT PATTERNS ---")
    await demonstrate_timeout_patterns()

# Run all demonstrations
print("\nDemonstrating async patterns:")
asyncio.run(main())