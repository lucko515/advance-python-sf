# Advanced Python for Salesforce Engineers

A comprehensive 3-day course focusing on advanced Object-Oriented Programming concepts in Python.

## Course Overview

This course is designed for experienced Python developers who want to deepen their understanding of Python's Object-Oriented Programming capabilities. The focus is on advanced topics including metaclasses, descriptors, and decorators, with practical applications for building better software and frameworks.

## Prerequisites

- Solid experience with Python programming
- Understanding of basic OOP concepts (classes, inheritance, polymorphism)
- Familiarity with Python's special methods (`__init__`, `__str__`, etc.)
- Experience with exception handling and context managers

## Course Structure

### Day 1: Understanding Python's Object Model

1. **Python's Object Model Fundamentals**
   - Deep dive into Python's object model
   - Understanding classes and instances
   - Object initialization and lifecycle
   - Attribute lookup and the descriptor protocol
   - The importance of the `type` class

2. **Introduction to Metaclasses**
   - What are metaclasses and why do they exist?
   - The `type` metaclass
   - Understanding class creation
   - Customizing class creation with metaclasses
   - Examples of metaclass usage

3. **Practical Applications of Metaclasses**
   - Class registration patterns
   - Enforcing class invariants
   - Attribute validation at class definition time
   - Extending classes declaratively
   - Real-world use cases in frameworks

### Day 2: Descriptors and Properties

4. **Advanced Method Decorators**
   - Review of basic decorators
   - Function vs. class decorators
   - Decorators with parameters
   - Useful built-in decorators (`@classmethod`, `@staticmethod`, `@property`)
   - Creating robust reusable decorators

5. **Method Resolution and Multiple Inheritance**
   - Python's Method Resolution Order (MRO)
   - The C3 linearization algorithm
   - Multiple inheritance patterns
   - Mixins and composition
   - Understanding `super()` in depth

6. **Property Descriptors**
   - Introduction to the descriptor protocol
   - How properties work as descriptors
   - Building custom property-like descriptors
   - Advanced property patterns
   - Inspecting property objects

7. **Custom Descriptors**
   - When to create custom descriptors
   - Descriptor state storage patterns
   - Validation descriptors
   - Lazy evaluation descriptors
   - Real-world examples from frameworks

### Day 3: Building Frameworks and Practical Applications

8. **Combining Metaclasses, Decorators, and Descriptors**
   - Design patterns leveraging multiple techniques
   - Understanding execution order
   - Building declarative APIs
   - Practical examples of combined techniques
   - Performance and design considerations

9. **Practical Real-world Examples**
   - Django-inspired models system
   - SQLAlchemy-inspired declarative system
   - Flask-inspired routing
   - Attrs-inspired class generation
   - Entity-component systems for games
   - Pydantic-inspired data validation
