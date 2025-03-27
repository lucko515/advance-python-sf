# 01: Introduction to Databases and Python
print("Introduction to Databases and Python")
print("-----------------------------------")


# Types of databases
print("\n3. Types of databases:")
db_types = {
    "Relational (SQL)": [
        "Structured data in tables with predefined schema",
        "Relationships between tables",
        "Examples: PostgreSQL, MySQL, SQLite, Oracle"
    ],
    "NoSQL": [
        "More flexible schema or schema-less",
        "Different types: Document, Key-Value, Column-family, Graph",
        "Examples: MongoDB, Redis, Cassandra, Neo4j"
    ]
}

for db_type, details in db_types.items():
    print(f"\n   {db_type}:")
    for detail in details:
        print(f"   - {detail}")

# When to use what?
print("\n4. When to use which type of database?")
use_cases = {
    "Relational databases": [
        "Complex queries and transactions",
        "When data integrity is critical",
        "Financial applications",
        "When data structure is well-defined and unlikely to change"
    ],
    "NoSQL databases": [
        "Rapid development with evolving schemas",
        "Very large scale distributed systems",
        "Real-time big data applications",
        "Content management systems"
    ]
}

for db, cases in use_cases.items():
    print(f"\n   {db} are ideal for:")
    for case in cases:
        print(f"   - {case}")

# Python and databases
print("\n5. Python's database ecosystem:")
python_db = {
    "SQLAlchemy": "Powerful ORM for SQL databases with both high and low-level APIs",
    "Django ORM": "Part of the Django web framework",
    "PyMongo": "Native Python driver for MongoDB",
    "sqlite3": "Built-in module for SQLite databases",
    "psycopg2": "PostgreSQL adapter",
    "mysql-connector": "MySQL driver"
}

for lib, desc in python_db.items():
    print(f"   - {lib}: {desc}")