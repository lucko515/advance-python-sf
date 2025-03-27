# What is NoSQL?
print("\n1. What is NoSQL?")
print("   'NoSQL' (Not Only SQL) refers to database systems that store and retrieve data")
print("   using models other than the traditional relational tables of SQL databases.")
print("   These databases are designed for specific data models with flexible schemas,")
print("   and are optimized for specific types of operations.")

# Types of NoSQL Databases
print("\n2. Types of NoSQL Databases:")
nosql_types = {
    "Document Stores": [
        "Store data in document format (JSON, BSON, XML)",
        "Each document is self-contained with all its data",
        "Examples: MongoDB, CouchDB, Firestore"
    ],
    "Key-Value Stores": [
        "Simple key-value pairs, like a hash table or dictionary",
        "Highly optimized for read/write operations",
        "Examples: Redis, DynamoDB, Riak"
    ],
    "Column-Family Stores": [
        "Store data in column families, optimized for queries over large datasets",
        "Good for analytical workloads",
        "Examples: Cassandra, HBase, Scylla"
    ],
    "Graph Databases": [
        "Store entities and the relationships between them",
        "Optimized for querying complex networks of relationships",
        "Examples: Neo4j, JanusGraph, Amazon Neptune"
    ]
}

for db_type, details in nosql_types.items():
    print(f"\n   {db_type}:")
    for detail in details:
        print(f"   - {detail}")

# SQL vs. NoSQL
print("\n3. SQL vs. NoSQL Comparison:")
comparisons = [
    ("Data Model", "Tabular (rows and columns)", "Varies (documents, key-value, graph, etc.)"),
    ("Schema", "Fixed schema", "Flexible/dynamic schema"),
    ("Scaling", "Primarily vertical", "Primarily horizontal"),
    ("ACID Compliance", "Strong ACID support", "Varies (many now support ACID)"),
    ("Query Language", "SQL (standardized)", "Database-specific APIs"),
    ("Relationships", "Tables connected via keys", "Embedded documents or references"),
    ("Use Cases", "Complex transactions, reporting", "High volume, variable data, rapid development")
]

print("   {:<15} {:<30} {:<30}".format("Feature", "SQL", "NoSQL"))
print("   {:<15} {:<30} {:<30}".format("-" * 15, "-" * 30, "-" * 30))
for feature, sql, nosql in comparisons:
    print("   {:<15} {:<30} {:<30}".format(feature, sql, nosql))

# When to use NoSQL
print("\n4. When to Use NoSQL Databases:")
use_cases = [
    "Handling large volumes of unstructured or semi-structured data",
    "Rapid development with evolving data requirements",
    "Horizontally scalable architecture for distributed systems",
    "Real-time big data applications",
    "Content management and delivery systems",
    "IoT and time-series data",
    "Caching and session storage"
]
for i, case in enumerate(use_cases, 1):
    print(f"   {i}. {case}")

# Introduction to MongoDB
print("\n5. Introduction to MongoDB:")
print("   MongoDB is a document-oriented NoSQL database designed for:")
mongo_features = [
    "High performance",
    "High availability",
    "Automatic scaling",
    "Flexible document schemas",
    "Rich query language",
    "Secondary indexes",
    "Aggregation framework"
]
for feature in mongo_features:
    print(f"   - {feature}")

# MongoDB vs. SQL Terminology
print("\n6. MongoDB vs. SQL Terminology:")
terminology = [
    ("Database", "Database"),
    ("Table", "Collection"),
    ("Row", "Document"),
    ("Column", "Field"),
    ("Primary Key", "ObjectId (_id)"),
    ("Index", "Index"),
    ("JOIN", "Embedding or $lookup"),
    ("Foreign Key", "Reference")
]

print("   {:<15} {:<15}".format("SQL", "MongoDB"))
print("   {:<15} {:<15}".format("-" * 15, "-" * 15))
for sql, mongo in terminology:
    print("   {:<15} {:<15}".format(sql, mongo))

# MongoDB Document Structure
print("\n7. MongoDB Document Structure:")
print("   MongoDB stores data in BSON format (Binary JSON):")

# Example document
print("\n   Example MongoDB Document:")
example_doc = '''
{
   "_id": ObjectId("612f9b5a7cd94f3a4c7e9b3d"),
   "name": "John Smith",
   "email": "john@example.com",
   "age": 30,
   "address": {
      "street": "123 Main St",
      "city": "New York",
      "state": "NY",
      "zip": "10001"
   },
   "tags": ["developer", "python", "mongodb"],
   "active": true,
   "created_at": ISODate("2023-01-15T08:00:00Z")
}
'''
print(example_doc)

# Key Features of MongoDB Documents
print("\n8. Key Features of MongoDB Documents:")
doc_features = [
    "Documents are self-contained with all their data",
    "Can contain nested documents (embeds)",
    "Can contain arrays of values or documents",
    "Each document can have a different structure (schema-less)",
    "Field values can be any BSON data type (strings, numbers, arrays, documents, etc.)",
    "Every document has a unique '_id' field (automatically generated if not provided)"
]
for feature in doc_features:
    print(f"   - {feature}")

# MongoDB Schema Design Patterns
print("\n9. MongoDB Schema Design Patterns:")
schema_patterns = {
    "Embedding": [
        "Store related data in a single document",
        "Best for 1:1 or 1:few relationships",
        "Reduces need for joins (improves read performance)",
        "May lead to document growth or duplication"
    ],
    "Referencing": [
        "Store references (IDs) between documents",
        "Best for 1:many or many:many relationships",
        "Avoids data duplication",
        "Requires multiple queries to fetch related data"
    ],
    "Hybrid": [
        "Combine embedding and referencing",
        "Embed frequently accessed data",
        "Reference less frequently accessed data",
        "Balance between performance and flexibility"
    ]
}

for pattern, details in schema_patterns.items():
    print(f"\n   {pattern}:")
    for detail in details:
        print(f"   - {detail}")

# Real-world MongoDB Use Cases
print("\n10. Real-world MongoDB Use Cases:")
real_world = [
    "Content management systems",
    "Mobile applications",
    "Real-time analytics",
    "Caching and session management",
    "IoT data storage",
    "Product catalogs",
    "User profiles and preferences",
    "Social media feeds and interactions"
]
for i, case in enumerate(real_world, 1):
    print(f"   {i}. {case}")

# MongoDB and Python
print("\n11. MongoDB and Python:")
python_mongo = [
    "PyMongo - Official MongoDB driver for Python",
    "Motor - Asynchronous Python driver for MongoDB",
    "MongoEngine - ODM (Object-Document Mapper) for MongoDB",
    "Mongoframes - Lightweight ODM for MongoDB",
    "MongoDB with Flask - Flask-PyMongo extension",
    "MongoDB with Django - djongo or Django-MongoDB-Engine"
]
for lib in python_mongo:
    print(f"   - {lib}")