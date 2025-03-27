# 01: Concurrency Introduction
print("Introduction to Concurrency in Python")
print("------------------------------------")

# Simple demonstration of I/O-bound vs CPU-bound tasks
import time
import math

def io_bound_task():
    """Simulates an I/O-bound task like a network request or file read"""
    print("Starting I/O-bound task...")
    # Simulate waiting for I/O
    time.sleep(2)
    print("I/O-bound task completed")
    return "I/O result"

def cpu_bound_task():
    """Simulates a CPU-bound task like complex calculations"""
    print("Starting CPU-bound task...")
    # Simulate heavy CPU computation
    result = 0
    for i in range(10_000_000):
        result += math.sqrt(i)
    print("CPU-bound task completed")
    return f"CPU result: {result:.2f}"

# Run tasks sequentially
print("\nRunning tasks sequentially:")
start = time.time()
io_bound_task()
cpu_bound_task()
end = time.time()
print(f"Sequential execution took {end - start:.2f} seconds")