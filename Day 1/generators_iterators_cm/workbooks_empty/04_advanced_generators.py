# 04: Advanced Generator Features
print("Advanced Generator Features")
print("-------------------------")

# Reviewing basic generator syntax
print("Basic generator review:")

# TODO

gen = simple_gen()
print(f"Values from simple generator: {next(gen)}, {next(gen)}, {next(gen)}")

# yield from statement
print("\nThe 'yield from' statement:")
print("Simplifies delegation to sub-generators")

def subgenerator():
    """A generator that will be delegated to"""
    yield "A"
    yield "B"
    yield "C"

def delegating_generator():
    # TODO

print("\nUsing yield from:")
for value in delegating_generator():
    print(f"  Got value: {value}")

# Nested iteration without yield from (for comparison)
def nested_without_yield_from():
    # TODO

print("\nWithout yield from (more verbose):")
for value in nested_without_yield_from():
    print(f"  Got value: {value}")

# yield from with return values
print("\nyield from with return values:")

def subgen_with_return():
    """A subgenerator that returns a value"""
    # TODO

def delegating_with_return():
    # TODO

print("\nCapturing return values with yield from:")
for value in delegating_with_return():
    print(f"  Got value: {value}")

# Two-way communication with send()
print("\nTwo-way communication with send():")

def echo_generator():
    """A generator that echoes received values"""
    print("  Generator started")
    while True:
        received = yield  # Yield None and wait to receive a value
        print(f"  Generator received: {received}")

print("\nUsing send() with a generator:")
echo = echo_generator()
next(echo)  # Prime the generator (advance to the first yield)
echo.send("Hello")
echo.send(42)
echo.send("Python")

# Generator with both yield and send
print("\nGenerator with both yield and send:")

def counter_with_step():
    """A generator that counts with a configurable step"""
    count = 0
    step = 1
    
    while True:
        # Yield current count and potentially receive new step value
        new_step = yield count
        # If we received a new step value, update it
        if new_step is not None:
            step = new_step
        # Increment count by step
        count += step

print("\nCounting with configurable step:")
counter = counter_with_step()
print(f"  Initial: {next(counter)}")  # 0
print(f"  +1: {next(counter)}")       # 1
print(f"  +1: {next(counter)}")       # 2

# Change step to 10
counter.send(10)  
print(f"  +10: {next(counter)}")      # 12
print(f"  +10: {next(counter)}")      # 22

# Change step to 5
counter.send(5)
print(f"  +5: {next(counter)}")       # 27
print(f"  +5: {next(counter)}")       # 32

# Exception handling with throw()
print("\nException handling with throw():")

def generator_with_exceptions():
    """A generator that handles exceptions"""
    try:
        yield 1
        yield 2
        yield 3
    except ValueError:
        print("  Caught ValueError inside generator")
        yield "Error handled"
    finally:
        print("  Generator cleanup (finally block)")

print("\nThrowing exceptions into a generator:")
gen_exc = generator_with_exceptions()
print(f"  First value: {next(gen_exc)}")  # 1
print(f"  Second value: {next(gen_exc)}")  # 2

# Throw exception into the generator
print("  Throwing ValueError into generator...")
result = gen_exc.throw(ValueError, "Something went wrong")
print(f"  After exception: {result}")  # "Error handled"


# Building a generator pipeline
print("\nBuilding a generator pipeline:")

def data_source():
    """Simulates a data source"""
    for i in range(1, 6):
        print(f"  [Source] Yielding: {i}")
        yield i

def filter_even(data):
    """Filters out odd numbers"""
    for item in data:
        if item % 2 == 0:
            print(f"  [Filter] Keeping even number: {item}")
            yield item
        else:
            print(f"  [Filter] Discarding odd number: {item}")

def multiply_by_ten(data):
    """Multiplies each item by 10"""
    for item in data:
        result = item * 10
        print(f"  [Processor] {item} * 10 = {result}")
        yield result

# Connect the pipeline components
print("\nRunning a multi-stage generator pipeline:")
pipeline = multiply_by_ten(filter_even(data_source()))

# Execute the pipeline
print("Pipeline results:")
for result in pipeline:
    print(f"  Final result: {result}")

# A more practical example: processing log files
print("\nPractical Example: Processing Log Files")

def read_logs(filename):
    """Simulate reading a log file"""
    logs = [
        "INFO: System started",
        "DEBUG: Configuration loaded",
        "WARNING: Low disk space",
        "ERROR: Connection failed",
        "INFO: User logged in"
    ]
    for log in logs:
        print(f"  [Reader] Read log: {log}")
        yield log

def filter_errors(logs):
    """Filter for error level logs only"""
    for log in logs:
        if "ERROR" in log:
            print(f"  [Filter] Found error: {log}")
            yield log
        else:
            print(f"  [Filter] Ignoring non-error: {log}")

def extract_message(logs):
    """Extract just the message part of the log"""
    for log in logs:
        message = log.split(": ", 1)[1]
        print(f"  [Extractor] Extracted message: {message}")
        yield message

def alert_formatter(messages):
    """Format messages as alerts"""
    for message in messages:
        alert = f"ALERT: {message}!"
        print(f"  [Formatter] Formatted alert: {alert}")
        yield alert

# Connect the logging pipeline
print("\nProcessing logs with a generator pipeline:")
error_alerts = alert_formatter(extract_message(filter_errors(read_logs("server.log"))))

# Execute the pipeline
print("Generated alerts:")
for alert in error_alerts:
    print(f"  {alert}")