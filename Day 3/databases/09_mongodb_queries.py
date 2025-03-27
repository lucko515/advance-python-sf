import os
import pprint
import datetime
from bson.objectid import ObjectId
from bson.son import SON  # Used for ordered dictionaries in aggregation

try:
    import pymongo
    from pymongo import MongoClient, ASCENDING, DESCENDING
    from pymongo.errors import ConnectionFailure, OperationFailure
    print("\nPyMongo imported successfully!")
except ImportError:
    print("\nPyMongo is not installed. Please install it using:")
    print("pip install pymongo")
    print("\nFor this lesson, we'll continue as if PyMongo is installed.")

# Create a pretty printer for better document display
pp = pprint.PrettyPrinter(indent=2)

# Try to connect to MongoDB
try:
    # Connect to a local MongoDB instance or MongoDB Atlas
    # For this example, we're using a local connection
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
    client.admin.command('ping')  # Test the connection
    connected = True
    print("Successfully connected to MongoDB!")
except (ConnectionFailure, OperationFailure) as e:
    connected = False
    print(f"Could not connect to MongoDB. Error: {e}")
    print("For the purpose of this lesson, we'll continue as if connected.")

# Setup: Create a database and collection for our examples
db_name = "advanced_queries_demo"
db = client[db_name] if connected else None

# Create a products collection for our examples
products_collection_name = "products"
products = db[products_collection_name] if connected else None

# Sample data for our examples
sample_products = [
    {
        "name": "Laptop Pro",
        "price": 1499.99,
        "category": "Electronics",
        "subcategory": "Computers",
        "brand": "TechMaster",
        "in_stock": True,
        "stock_count": 45,
        "tags": ["laptop", "high-performance", "professional"],
        "specs": {
            "processor": "Intel i9",
            "ram": "32GB",
            "storage": "1TB SSD",
            "display": "15.6 inch 4K"
        },
        "reviews": [
            {"user": "user123", "rating": 5, "comment": "Great laptop for development work!"},
            {"user": "user456", "rating": 4, "comment": "Fast but runs hot sometimes."}
        ],
        "warehouse_locations": [
            {"city": "San Francisco", "quantity": 20},
            {"city": "New York", "quantity": 15},
            {"city": "Chicago", "quantity": 10}
        ],
        "release_date": datetime.datetime(2023, 1, 15),
        "sale_history": [100, 120, 80, 95, 110]
    },
    {
        "name": "Smartphone X",
        "price": 899.99,
        "category": "Electronics",
        "subcategory": "Phones",
        "brand": "MobileTech",
        "in_stock": True,
        "stock_count": 120,
        "tags": ["smartphone", "5G", "high-resolution"],
        "specs": {
            "processor": "Snapdragon 8",
            "ram": "12GB",
            "storage": "256GB",
            "display": "6.7 inch OLED"
        },
        "reviews": [
            {"user": "user789", "rating": 5, "comment": "Best phone I've ever had!"},
            {"user": "user101", "rating": 5, "comment": "Amazing camera quality."},
            {"user": "user202", "rating": 3, "comment": "Good phone but expensive."}
        ],
        "warehouse_locations": [
            {"city": "San Francisco", "quantity": 40},
            {"city": "New York", "quantity": 50},
            {"city": "Chicago", "quantity": 30}
        ],
        "release_date": datetime.datetime(2023, 2, 20),
        "sale_history": [150, 180, 200, 190, 210]
    },
    {
        "name": "Wireless Earbuds",
        "price": 129.99,
        "category": "Electronics",
        "subcategory": "Audio",
        "brand": "SoundWave",
        "in_stock": True,
        "stock_count": 200,
        "tags": ["wireless", "earbuds", "bluetooth"],
        "specs": {
            "battery_life": "8 hours",
            "charging_case": "24 hours additional",
            "water_resistant": True
        },
        "reviews": [
            {"user": "user303", "rating": 4, "comment": "Great sound quality!"},
            {"user": "user404", "rating": 2, "comment": "Battery doesn't last as advertised."}
        ],
        "warehouse_locations": [
            {"city": "San Francisco", "quantity": 75},
            {"city": "New York", "quantity": 75},
            {"city": "Chicago", "quantity": 50}
        ],
        "release_date": datetime.datetime(2022, 11, 10),
        "sale_history": [80, 95, 120, 110, 130]
    },
    {
        "name": "Coffee Maker Deluxe",
        "price": 149.99,
        "category": "Home",
        "subcategory": "Kitchen",
        "brand": "HomeStyle",
        "in_stock": True,
        "stock_count": 30,
        "tags": ["coffee", "kitchen", "appliance"],
        "specs": {
            "capacity": "12 cups",
            "programmable": True,
            "auto_shutoff": True
        },
        "reviews": [
            {"user": "user505", "rating": 5, "comment": "Makes the perfect cup every time!"},
            {"user": "user606", "rating": 4, "comment": "Easy to use and clean."}
        ],
        "warehouse_locations": [
            {"city": "San Francisco", "quantity": 10},
            {"city": "New York", "quantity": 10},
            {"city": "Chicago", "quantity": 10}
        ],
        "release_date": datetime.datetime(2022, 9, 5),
        "sale_history": [20, 25, 30, 35, 40]
    },
    {
        "name": "Running Shoes Pro",
        "price": 129.99,
        "category": "Clothing",
        "subcategory": "Footwear",
        "brand": "SportMax",
        "in_stock": True,
        "stock_count": 8,
        "tags": ["shoes", "running", "athletic"],
        "specs": {
            "size_range": "7-13",
            "color_options": ["Black", "White", "Red", "Blue"],
            "cushioning": "High Impact"
        },
        "reviews": [
            {"user": "user707", "rating": 5, "comment": "Very comfortable for long runs!"},
            {"user": "user808", "rating": 4, "comment": "Good quality but runs small."}
        ],
        "warehouse_locations": [
            {"city": "San Francisco", "quantity": 3},
            {"city": "New York", "quantity": 3},
            {"city": "Chicago", "quantity": 2}
        ],
        "release_date": datetime.datetime(2023, 3, 15),
        "sale_history": [15, 18, 20, 22, 25]
    },
    {
        "name": "Smart Watch",
        "price": 249.99,
        "category": "Electronics",
        "subcategory": "Wearables",
        "brand": "TechMaster",
        "in_stock": True,
        "stock_count": 60,
        "tags": ["watch", "smart", "fitness"],
        "specs": {
            "display": "AMOLED",
            "battery_life": "5 days",
            "water_resistant": True,
            "heart_rate_monitor": True
        },
        "reviews": [
            {"user": "user909", "rating": 5, "comment": "Tracks all my fitness activities perfectly!"},
            {"user": "user111", "rating": 3, "comment": "Battery life is shorter than advertised."}
        ],
        "warehouse_locations": [
            {"city": "San Francisco", "quantity": 25},
            {"city": "New York", "quantity": 20},
            {"city": "Chicago", "quantity": 15}
        ],
        "release_date": datetime.datetime(2022, 10, 12),
        "sale_history": [50, 60, 75, 80, 90]
    },
    {
        "name": "4K Smart TV",
        "price": 799.99,
        "category": "Electronics",
        "subcategory": "TVs",
        "brand": "ViewTech",
        "in_stock": True,
        "stock_count": 15,
        "tags": ["tv", "4k", "smart"],
        "specs": {
            "size": "55 inch",
            "resolution": "4K Ultra HD",
            "smart_platform": "Android TV",
            "refresh_rate": "120Hz"
        },
        "reviews": [
            {"user": "user121", "rating": 5, "comment": "Picture quality is amazing!"},
            {"user": "user131", "rating": 4, "comment": "Good TV, but the interface is a bit sluggish."}
        ],
        "warehouse_locations": [
            {"city": "San Francisco", "quantity": 5},
            {"city": "New York", "quantity": 5},
            {"city": "Chicago", "quantity": 5}
        ],
        "release_date": datetime.datetime(2022, 8, 20),
        "sale_history": [10, 12, 15, 18, 20]
    }
]

# Set up the sample data
if connected:
    # Drop the collection if it exists to start fresh
    if products_collection_name in db.list_collection_names():
        db.drop_collection(products_collection_name)
    
    # Insert sample data
    result = products.insert_many(sample_products)
    print(f"Inserted {len(result.inserted_ids)} sample products")

# 1. Complex Query Operators
print("\n1. Complex Query Operators:")

# Example complex query operators
print("\n   1.1 Comparison Operators:")
comparison_operators = [
    ("$eq", "Equals"),
    ("$ne", "Not equals"),
    ("$gt", "Greater than"),
    ("$gte", "Greater than or equal to"),
    ("$lt", "Less than"),
    ("$lte", "Less than or equal to"),
    ("$in", "In array"),
    ("$nin", "Not in array")
]
for op, desc in comparison_operators:
    print(f"   - {op}: {desc}")

# Example: Products in a price range
if connected:
    mid_range_products = products.find({
        "price": {
            "$gte": 100,
            "$lte": 500
        }
    })
    print("\n   Products in price range $100-$500:")
    for product in mid_range_products:
        print(f"   - {product['name']}: ${product['price']}")

print("\n   1.2 Logical Operators:")
logical_operators = [
    ("$and", "Logical AND"),
    ("$or", "Logical OR"),
    ("$not", "Logical NOT"),
    ("$nor", "Logical NOR")
]
for op, desc in logical_operators:
    print(f"   - {op}: {desc}")

# Example: Electronics products with high stock
if connected:
    high_stock_electronics = products.find({
        "$and": [
            {"category": "Electronics"},
            {"stock_count": {"$gt": 50}}
        ]
    })
    print("\n   Electronics with stock > 50:")
    for product in high_stock_electronics:
        print(f"   - {product['name']}: {product['stock_count']} in stock")

print("\n   1.3 Element Operators:")
element_operators = [
    ("$exists", "Field exists"),
    ("$type", "Field is of specified type")
]
for op, desc in element_operators:
    print(f"   - {op}: {desc}")

# Example: Products with water resistance specified
if connected:
    water_resistant_products = products.find({
        "specs.water_resistant": {"$exists": True}
    })
    print("\n   Products with water resistance spec:")
    for product in water_resistant_products:
        print(f"   - {product['name']}: Water resistant: {product['specs']['water_resistant']}")

print("\n   1.4 Evaluation Operators:")
evaluation_operators = [
    ("$regex", "Regular expression match"),
    ("$text", "Text search"),
    ("$expr", "Aggregation expressions")
]
for op, desc in evaluation_operators:
    print(f"   - {op}: {desc}")

# Example: Products with "Pro" in the name
if connected:
    pro_products = products.find({
        "name": {"$regex": "Pro", "$options": "i"}  # 'i' for case-insensitive
    })
    print("\n   Products with 'Pro' in the name:")
    for product in pro_products:
        print(f"   - {product['name']}")

# 2. Querying Nested Documents and Arrays
print("\n2. Querying Nested Documents and Arrays:")

print("\n   2.1 Querying Nested Documents:")
if connected:
    # Find products with specific processor
    intel_products = products.find({
        "specs.processor": "Intel i9"
    })
    print("\n   Products with Intel i9 processor:")
    for product in intel_products:
        print(f"   - {product['name']}: {product['specs']['processor']}")

print("\n   2.2 Array Query Operators:")
array_operators = [
    ("$all", "Array contains all specified elements"),
    ("$elemMatch", "Element in array matches all conditions"),
    ("$size", "Array is of specified size")
]
for op, desc in array_operators:
    print(f"   - {op}: {desc}")

# Example: Products with specific tags
if connected:
    wireless_products = products.find({
        "tags": {"$all": ["wireless"]}
    })
    print("\n   Products with 'wireless' tag:")
    for product in wireless_products:
        print(f"   - {product['name']}: Tags: {', '.join(product['tags'])}")

print("\n   2.3 Querying Arrays of Objects:")
if connected:
    # Find products with high ratings
    high_rated_products = products.find({
        "reviews": {
            "$elemMatch": {
                "rating": 5
            }
        }
    })
    print("\n   Products with 5-star reviews:")
    for product in high_rated_products:
        print(f"   - {product['name']}")
        for review in product['reviews']:
            if review['rating'] == 5:
                print(f"      - \"{review['comment']}\" ({review['rating']} stars)")

# 3. Aggregation Framework
print("\n3. MongoDB Aggregation Framework:")
print("   The aggregation framework allows for data processing in stages:")

aggregation_stages = [
    ("$match", "Filters documents (like find)"),
    ("$group", "Groups documents by a key"),
    ("$sort", "Sorts documents"),
    ("$project", "Reshapes documents (includes/excludes fields)"),
    ("$limit", "Limits number of documents"),
    ("$skip", "Skips documents"),
    ("$unwind", "Deconstructs array field"),
    ("$lookup", "Performs a left outer join to another collection")
]

print("\n   3.1 Basic Aggregation Example:")
if connected:
    # Average price by category
    pipeline = [
        {"$group": {
            "_id": "$category",
            "avgPrice": {"$avg": "$price"},
            "count": {"$sum": 1}
        }},
        {"$sort": {"avgPrice": -1}}
    ]
    
    category_avg_prices = products.aggregate(pipeline)
    print("\n   Average prices by category:")
    for result in category_avg_prices:
        print(f"   - {result['_id']}: ${result['avgPrice']:.2f} (from {result['count']} products)")

print("\n   3.2 Using $match and $project:")
if connected:
    # Find and reshape electronics products
    pipeline = [
        {"$match": {"category": "Electronics"}},
        {"$project": {
            "_id": 0,
            "product": "$name",
            "brand": 1,
            "price": 1,
            "inStock": "$stock_count"
        }}
    ]
    
    electronics = products.aggregate(pipeline)
    print("\n   Electronics products (reshaped):")
    for product in electronics:
        pp.pprint(product)

print("\n   3.3 Using $unwind:")
if connected:
    # Unwind the reviews array
    pipeline = [
        {"$match": {"name": "Smartphone X"}},
        {"$unwind": "$reviews"},
        {"$project": {
            "_id": 0,
            "product": "$name",
            "reviewer": "$reviews.user",
            "rating": "$reviews.rating",
            "comment": "$reviews.comment"
        }}
    ]
    
    reviews = products.aggregate(pipeline)
    print("\n   Smartphone X reviews (unwound):")
    for review in reviews:
        pp.pprint(review)

print("\n   3.4 Complex Aggregation Example:")
if connected:
    # Get products with average review rating
    pipeline = [
        {"$match": {"reviews": {"$exists": True, "$ne": []}}},
        {"$unwind": "$reviews"},
        {"$group": {
            "_id": {
                "product_id": "$_id",
                "name": "$name",
                "category": "$category"
            },
            "avgRating": {"$avg": "$reviews.rating"},
            "numReviews": {"$sum": 1}
        }},
        {"$match": {"avgRating": {"$gte": 4}}},
        {"$sort": {"avgRating": -1}}
    ]
    
    product_ratings = products.aggregate(pipeline)
    print("\n   Products with average rating ≥ 4:")
    for result in product_ratings:
        print(f"   - {result['_id']['name']} ({result['_id']['category']}): "
              f"{result['avgRating']:.1f} stars ({result['numReviews']} reviews)")

# 4. Indexing for Query Optimization
print("\n4. Indexing for Query Optimization:")

index_types = [
    ("Single Field", "Index on one field - db.collection.createIndex({'field': 1})"),
    ("Compound", "Index on multiple fields - db.collection.createIndex({'field1': 1, 'field2': -1})"),
    ("Multikey", "Index on array field - db.collection.createIndex({'array_field': 1})"),
    ("Text", "Index for text search - db.collection.createIndex({'field': 'text'})"),
    ("Geospatial", "Index for geospatial queries - db.collection.createIndex({'field': '2dsphere'})")
]

# Create some indexes
if connected:
    # Create a price index
    products.create_index([("price", ASCENDING)])
    print("\n   Created index on price field")
    
    # Create a compound index
    products.create_index([("category", ASCENDING), ("subcategory", ASCENDING)])
    print("   Created compound index on category and subcategory")
    
    # Create a text index for searching
    products.create_index([("name", "text"), ("tags", "text")])
    print("   Created text index on name and tags")
    
    # Show all indexes
    print("\n   Collection indexes:")
    for index in products.list_indexes():
        print(f"   - {index['name']}: {index['key']}")

# 5. Text Search
print("\n5. Text Search:")
if connected:
    # Perform a text search
    search_results = products.find({"$text": {"$search": "wireless bluetooth"}})
    print("\n   Text search for 'wireless bluetooth':")
    for product in search_results:
        print(f"   - {product['name']}: {', '.join(product['tags'])}")
    
    # Search with score
    scored_results = products.find(
        {"$text": {"$search": "smart"}},
        {"score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})])
    
    print("\n   Text search for 'smart' with relevance score:")
    for product in scored_results:
        print(f"   - {product['name']} (Score: {product['score']:.2f})")

# 6. Working with Large Result Sets
print("\n6. Working with Large Result Sets:")

pagination_example = '''
# Pagination example
page_size = 10
page_num = 2
skip_count = page_size * (page_num - 1)

results = collection.find().skip(skip_count).limit(page_size)
'''
print(pagination_example)

cursor_methods = [
    ("limit(n)", "Limits results to n documents"),
    ("skip(n)", "Skips the first n documents"),
    ("sort(spec)", "Sorts results by the given spec"),
    ("count_documents(filter)", "Returns the count of matching documents"),
    ("distinct(field)", "Returns array of distinct values for the field")
]
print("\n   Cursor Methods:")
for method, desc in cursor_methods:
    print(f"   - {method}: {desc}")

# 7. Query Performance Analysis
print("\n7. Query Performance Analysis:")
if connected:
    # Example of using explain
    explanation = products.find({"category": "Electronics"}).explain()
    
    # Just show a simplified version for teaching purposes
    print("\n   Query execution plan (simplified):")
    if "executionStats" in explanation:
        stats = explanation["executionStats"]
        print(f"   - Execution time: {stats.get('executionTimeMillis')} ms")
        print(f"   - Documents examined: {stats.get('totalDocsExamined')}")
        print(f"   - Results returned: {stats.get('nReturned')}")
    else:
        print("   - Query planner used: " + explanation.get("queryPlanner", {}).get("winningPlan", {}).get("stage", "Unknown"))

# 8. Performance Best Practices
print("\n8. Performance Best Practices:")
best_practices = [
    "Create indexes for frequently queried fields",
    "Use covered queries where possible (queries satisfied by indexes)",
    "Avoid querying for unnecessary fields",
    "Use projections to limit returned fields",
    "Be aware of index size and memory usage",
    "Monitor slow queries and optimize them",
    "Properly structure documents to avoid deep nesting",
    "Consider data access patterns when designing the schema"
]

# Clean up
if connected:
    # Uncomment to drop the collection when finished
    # db.drop_collection(products_collection_name)
    
    # Close the connection
    client.close()
    print("\n   MongoDB connection closed")