import os
import pprint
import datetime
from bson.objectid import ObjectId

try:
    # Check if PyMongo is installed
    import pymongo
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, OperationFailure
    
    print("\nPyMongo installed and imported successfully!")
    print(f"PyMongo version: {pymongo.__version__}")
except ImportError:
    print("\nPyMongo is not installed. Please install it using:")
    print("pip install pymongo")
    print("\nFor this lesson, we'll continue as if PyMongo is installed.")

# Create a pretty printer for better document display
pp = pprint.PrettyPrinter(indent=2)

# 1. Connecting to MongoDB
print("\n1. Connecting to MongoDB:")
print("   PyMongo provides several ways to connect to MongoDB:")

# Connection strings examples
print("\n   Connection string examples:")
connection_examples = [
    ("Local MongoDB", "mongodb://localhost:27017/"),
    ("MongoDB with authentication", "mongodb://username:password@localhost:27017/"),
    ("MongoDB Atlas", "mongodb+srv://username:password@cluster0.mongodb.net/")
]
for desc, conn_string in connection_examples:
    print(f"   - {desc}: {conn_string}")

# For the lesson, we'll use a try-except block to handle potential connection failures
try:
    # Try to connect to a local MongoDB instance
    # Note: In a real environment, you might connect to MongoDB Atlas or another MongoDB server
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
    
    # Check if the connection is valid by issuing a command to the server
    client.admin.command('ping')
    
    connected = True
    print("\n   Successfully connected to MongoDB!")

except (ConnectionFailure, OperationFailure) as e:
    connected = False
    print(f"\n   Could not connect to MongoDB. Error: {e}")
    print("   For the purpose of this lesson, we'll continue as if connected.")

# 2. Understanding PyMongo's Structure
print("\n2. PyMongo's Client-Database-Collection Structure:")
print("   PyMongo follows MongoDB's organizational hierarchy:")
hierarchy = [
    ("MongoClient", "Connection to a MongoDB instance"),
    ("Database", "A database within MongoDB (client.database_name)"),
    ("Collection", "A collection within a database (db.collection_name)"),
    ("Document", "A record in a collection (stored as BSON/dict)")
]
for item, desc in hierarchy:
    print(f"   - {item}: {desc}")

# 3. Creating/Accessing Databases and Collections
print("\n3. Creating/Accessing Databases and Collections:")
print("   In MongoDB, databases and collections are created lazily (on first use)")

# Access a database
db_name = "pymongo_demo"
db = client[db_name] if connected else None
print(f"   - Accessed database: {db_name}")

# Access a collection
collection_name = "users"
users = db[collection_name] if connected else None
print(f"   - Accessed collection: {collection_name}")

print("\n   Note: The database and collection aren't actually created until you insert data")

# 4. CRUD Operations: Create (Insert)
print("\n4. CRUD Operations: Create (Insert)")

# Example documents
sample_users = [
    {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "address": {
            "street": "123 Main St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94107"
        },
        "interests": ["Python", "MongoDB", "Data Science"],
        "active": True,
        "created_at": datetime.datetime.utcnow()
    },
    {
        "name": "Jane Smith",
        "email": "jane@example.com",
        "age": 28,
        "address": {
            "street": "456 Market St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94103"
        },
        "interests": ["Web Development", "UX Design"],
        "active": True,
        "created_at": datetime.datetime.utcnow()
    },
    {
        "name": "Bob Johnson",
        "email": "bob@example.com",
        "age": 35,
        "address": {
            "street": "789 Mission St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94105"
        },
        "interests": ["MongoDB", "DevOps", "Cloud Computing"],
        "active": False,
        "created_at": datetime.datetime.utcnow()
    }
]

print("\n   4.1 Inserting a single document:")
if connected:
    # Check if the collection is empty before inserting
    if users.count_documents({}) == 0:
        user_1_id = users.insert_one(sample_users[0]).inserted_id
        print(f"   - Inserted user with ID: {user_1_id}")
    else:
        print("   - Collection already has data, skipping insert")
else:
    print("   - Example: users.insert_one(document)")
    print("   - Returns an InsertOneResult object with inserted_id attribute")

print("\n   4.2 Inserting multiple documents:")
if connected:
    # Check count again to avoid duplicate inserts in repeated runs
    if users.count_documents({}) < 2:
        result = users.insert_many(sample_users[1:])
        print(f"   - Inserted {len(result.inserted_ids)} documents")
        print(f"   - IDs: {result.inserted_ids}")
    else:
        print("   - Collection already has multiple documents, skipping insert")
else:
    print("   - Example: users.insert_many([doc1, doc2, ...])")
    print("   - Returns an InsertManyResult object with inserted_ids attribute")

# 5. CRUD Operations: Read (Query)
print("\n5. CRUD Operations: Read (Query)")

if connected:
    # Get total document count
    total_docs = users.count_documents({})
    print(f"   Collection contains {total_docs} documents")

print("\n   5.1 Finding a single document:")
if connected:
    user = users.find_one({"name": "John Doe"})
    if user:
        print("   - Found user:")
        pp.pprint(user)
    else:
        print("   - User not found")
else:
    print("   - Example: users.find_one({'field': 'value'})")
    print("   - Returns the first matching document or None")

print("\n   5.2 Finding multiple documents:")
if connected:
    cursor = users.find({"active": True})
    print("   - Active users:")
    for doc in cursor:
        print(f"     - {doc['name']} ({doc['email']})")
else:
    print("   - Example: users.find({'field': 'value'})")
    print("   - Returns a cursor that can be iterated")

print("\n   5.3 Querying with filters:")
print("   MongoDB supports various query operators:")
query_operators = [
    ("Equality", "{'field': 'value'}"),
    ("Less than", "{'field': {'$lt': value}}"),
    ("Greater than", "{'field': {'$gt': value}}"),
    ("In list", "{'field': {'$in': [value1, value2]}}"),
    ("AND", "{'field1': value1, 'field2': value2}"),
    ("OR", "{'$or': [{'field1': value1}, {'field2': value2}]}")
]
for op, example in query_operators:
    print(f"   - {op}: {example}")

if connected:
    # Example: Find users over 30
    older_users = users.find({"age": {"$gt": 30}})
    print("\n   - Users over 30:")
    for user in older_users:
        print(f"     - {user['name']} (Age: {user['age']})")
    
    # Example: Find users with specific interest
    mongo_users = users.find({"interests": "MongoDB"})
    print("\n   - Users interested in MongoDB:")
    for user in mongo_users:
        print(f"     - {user['name']} (Interests: {', '.join(user['interests'])})")

print("\n   5.4 Projections (selecting specific fields):")
if connected:
    # Only return name and email fields
    projection = users.find({}, {"name": 1, "email": 1, "_id": 0})
    print("   - Name and email only:")
    for p in projection:
        print(f"     - {p['name']}: {p['email']}")
else:
    print("   - Example: users.find({}, {'name': 1, 'email': 1, '_id': 0})")
    print("   - 1 includes the field, 0 excludes it")

# 6. CRUD Operations: Update
print("\n6. CRUD Operations: Update")

print("\n   6.1 Updating a single document:")
if connected:
    # Update John's age
    result = users.update_one(
        {"name": "John Doe"},
        {"$set": {"age": 31, "updated_at": datetime.datetime.utcnow()}}
    )
    print(f"   - Matched {result.matched_count} document(s)")
    print(f"   - Modified {result.modified_count} document(s)")
    
    # Show the updated document
    updated_user = users.find_one({"name": "John Doe"})
    if updated_user:
        print("   - Updated user:")
        print(f"     - Name: {updated_user['name']}")
        print(f"     - Age: {updated_user['age']}")
else:
    print("   - Example: users.update_one({'field': 'value'}, {'$set': {'field': new_value}})")
    print("   - Returns UpdateResult object with matched_count and modified_count")

print("\n   6.2 Update operators:")
update_operators = [
    ("$set", "Sets field values"),
    ("$inc", "Increments field values"),
    ("$push", "Adds elements to arrays"),
    ("$pull", "Removes elements from arrays"),
    ("$unset", "Removes fields")
]
for op, desc in update_operators:
    print(f"   - {op}: {desc}")

print("\n   6.3 Updating multiple documents:")
if connected:
    # Add a new field to all active users
    result = users.update_many(
        {"active": True},
        {"$set": {"account_type": "Standard"}}
    )
    print(f"   - Matched {result.matched_count} document(s)")
    print(f"   - Modified {result.modified_count} document(s)")
else:
    print("   - Example: users.update_many({'field': 'value'}, {'$set': {'field': new_value}})")
    print("   - Updates all documents that match the filter")

# 7. CRUD Operations: Delete
print("\n7. CRUD Operations: Delete")

print("\n   7.1 Deleting a single document:")
if connected:
    # First, insert a temporary document
    temp_doc = {
        "name": "Temporary User",
        "email": "temp@example.com",
        "to_be_deleted": True
    }
    temp_id = users.insert_one(temp_doc).inserted_id
    
    # Then delete it
    result = users.delete_one({"_id": temp_id})
    print(f"   - Deleted {result.deleted_count} document(s)")
else:
    print("   - Example: users.delete_one({'field': 'value'})")
    print("   - Returns DeleteResult object with deleted_count")

print("\n   7.2 Deleting multiple documents:")
if connected:
    # Insert some temporary documents
    temp_docs = [
        {"name": "Temp 1", "to_be_deleted": True},
        {"name": "Temp 2", "to_be_deleted": True}
    ]
    users.insert_many(temp_docs)
    
    # Delete them
    result = users.delete_many({"to_be_deleted": True})
    print(f"   - Deleted {result.deleted_count} document(s)")
else:
    print("   - Example: users.delete_many({'field': 'value'})")
    print("   - Deletes all documents that match the filter")

# 8. Working with ObjectIDs
print("\n8. Working with ObjectIDs:")
print("   MongoDB uses ObjectIDs as the default _id field")

# Create a new ObjectID
new_id = ObjectId()
print(f"   - New ObjectID: {new_id}")
print(f"   - Creation time: {new_id.generation_time}")

print("\n   Querying by ObjectID:")
print("   - Convert string to ObjectID: ObjectId('5f50a1d....')")
print("   - Example: users.find_one({'_id': ObjectId('5f50a1d....')})")

# 9. Error Handling
print("\n9. Error Handling in PyMongo:")
error_types = [
    ("ConnectionFailure", "Failed to connect to MongoDB server"),
    ("OperationFailure", "Operation failed (e.g., authentication, permissions)"),
    ("WriteError", "Write operation failed"),
    ("DuplicateKeyError", "Tried to insert a document with a duplicate key")
]
print("   Common PyMongo exceptions:")
for exc, desc in error_types:
    print(f"   - {exc}: {desc}")

print("\n   Example error handling:")
code_example = '''
try:
    result = users.insert_one({"_id": "duplicate", "name": "Test"})
except pymongo.errors.DuplicateKeyError:
    print("A document with that _id already exists")
'''
print(code_example)

# 10. Performance Tips
print("\n10. Performance Tips for PyMongo:")
tips = [
    "Use indexes for frequently queried fields",
    "Limit the number of documents returned with limit()",
    "Use projections to return only needed fields",
    "Consider using bulk operations for multiple writes",
    "Be mindful of document size (16MB maximum)",
    "Use appropriate connection pooling settings",
    "Monitor query performance with explain()"
]
for i, tip in enumerate(tips, 1):
    print(f"   {i}. {tip}")

# Clean up
if connected:
    # Drop the collection if you want to clean up
    # Uncomment the next line to drop the collection
    # db.drop_collection(collection_name)
    
    # Close the connection
    client.close()
    print("\n   MongoDB connection closed")