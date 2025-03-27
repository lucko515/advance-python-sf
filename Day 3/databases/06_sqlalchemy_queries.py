import os
import time
from datetime import datetime, timedelta
from sqlalchemy import create_engine, func, desc, asc, and_, or_, not_, cast, Integer, text
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, joinedload, subqueryload, contains_eager

# Setup: Create models for demonstration
# We'll reuse models similar to our previous examples
Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    
    employees = relationship("Employee", back_populates="department")
    
    def __repr__(self):
        return f"<Department(id={self.id}, name='{self.name}')>"

class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hire_date = Column(DateTime, default=datetime.utcnow)
    salary = Column(Float, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    
    department = relationship("Department", back_populates="employees")
    addresses = relationship("Address", back_populates="employee")
    
    def __repr__(self):
        return f"<Employee(id={self.id}, name='{self.first_name} {self.last_name}')>"

class Address(Base):
    __tablename__ = 'addresses'
    
    id = Column(Integer, primary_key=True)
    street = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(String(10), nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    
    employee = relationship("Employee", back_populates="addresses")
    
    def __repr__(self):
        return f"<Address(id={self.id}, city='{self.city}', employee_id={self.employee_id})>"

# Create data directory if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# Set up the database
db_path = os.path.abspath("data/sqlalchemy_queries.db")
engine = create_engine(f"sqlite:///{db_path}", echo=False)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Generate some sample data for our queries
def create_sample_data():
    # Check if data already exists
    if session.query(Employee).count() > 0:
        print("Sample data already exists, skipping creation.")
        return
    
    # Departments
    departments = [
        Department(name="Engineering"),
        Department(name="Marketing"),
        Department(name="Sales"),
        Department(name="Human Resources"),
        Department(name="Customer Support")
    ]
    session.add_all(departments)
    session.commit()
    
    # Employees
    employees_data = [
        # Engineering
        {"first_name": "Alice", "last_name": "Smith", "email": "alice@example.com", 
         "hire_date": datetime.utcnow() - timedelta(days=500), "salary": 90000, "department_id": 1},
        {"first_name": "Bob", "last_name": "Johnson", "email": "bob@example.com", 
         "hire_date": datetime.utcnow() - timedelta(days=300), "salary": 85000, "department_id": 1},
        {"first_name": "Charlie", "last_name": "Williams", "email": "charlie@example.com", 
         "hire_date": datetime.utcnow() - timedelta(days=100), "salary": 80000, "department_id": 1},
        
        # Marketing
        {"first_name": "Diana", "last_name": "Jones", "email": "diana@example.com", 
         "hire_date": datetime.utcnow() - timedelta(days=450), "salary": 75000, "department_id": 2},
        {"first_name": "Edward", "last_name": "Brown", "email": "edward@example.com", 
         "hire_date": datetime.utcnow() - timedelta(days=250), "salary": 70000, "department_id": 2},
        
        # Sales
        {"first_name": "Fiona", "last_name": "Miller", "email": "fiona@example.com", 
         "hire_date": datetime.utcnow() - timedelta(days=400), "salary": 82000, "department_id": 3},
        {"first_name": "George", "last_name": "Wilson", "email": "george@example.com", 
         "hire_date": datetime.utcnow() - timedelta(days=350), "salary": 80000, "department_id": 3},
        {"first_name": "Hannah", "last_name": "Moore", "email": "hannah@example.com", 
         "hire_date": datetime.utcnow() - timedelta(days=320), "salary": 78000, "department_id": 3},
        
        # HR
        {"first_name": "Ian", "last_name": "Taylor", "email": "ian@example.com", 
         "hire_date": datetime.utcnow() - timedelta(days=200), "salary": 72000, "department_id": 4},
        
        # Customer Support
        {"first_name": "Julia", "last_name": "Anderson", "email": "julia@example.com", 
         "hire_date": datetime.utcnow() - timedelta(days=150), "salary": 65000, "department_id": 5},
        {"first_name": "Kevin", "last_name": "Thomas", "email": "kevin@example.com", 
         "hire_date": datetime.utcnow() - timedelta(days=120), "salary": 62000, "department_id": 5}
    ]
    
    employees = []
    for emp_data in employees_data:
        emp = Employee(**emp_data)
        employees.append(emp)
        session.add(emp)
    
    session.commit()
    
    # Addresses
    addresses = [
        # Alice has two addresses
        Address(street="123 Main St", city="San Francisco", state="CA", zip_code="94102", employee_id=1),
        Address(street="456 Market St", city="San Francisco", state="CA", zip_code="94103", employee_id=1),
        
        # Bob has one address
        Address(street="789 Mission St", city="San Francisco", state="CA", zip_code="94105", employee_id=2),
        
        # Others have one address each
        Address(street="101 Broadway", city="New York", state="NY", zip_code="10001", employee_id=3),
        Address(street="202 5th Ave", city="New York", state="NY", zip_code="10002", employee_id=4),
        Address(street="303 Madison Ave", city="New York", state="NY", zip_code="10003", employee_id=5),
        Address(street="404 Pine St", city="Seattle", state="WA", zip_code="98101", employee_id=6),
        Address(street="505 Olive Way", city="Seattle", state="WA", zip_code="98102", employee_id=7),
        Address(street="606 University St", city="Seattle", state="WA", zip_code="98103", employee_id=8),
        Address(street="707 Park Ave", city="Chicago", state="IL", zip_code="60601", employee_id=9),
        Address(street="808 Michigan Ave", city="Chicago", state="IL", zip_code="60602", employee_id=10),
        Address(street="909 State St", city="Chicago", state="IL", zip_code="60603", employee_id=11)
    ]
    
    session.add_all(addresses)
    session.commit()
    
    print(f"Created {len(departments)} departments, {len(employees)} employees, and {len(addresses)} addresses.")

# Create sample data
create_sample_data()

# Basic Queries
print("\n1. Basic Queries:")

print("\n   1.1 Simple SELECT query:")
employees = session.query(Employee).all()
print(f"   - Found {len(employees)} employees")
for emp in employees[:3]:  # Show first 3
    print(f"      {emp.first_name} {emp.last_name}")
print("      ...")

print("\n   1.2 SELECT with specific columns:")
results = session.query(Employee.first_name, Employee.last_name, Employee.salary).all()
print("   - Selected specific columns for all employees:")
for first_name, last_name, salary in results[:3]:  # Show first 3
    print(f"      {first_name} {last_name}: ${salary:,.2f}")
print("      ...")

# Filtering Queries
print("\n2. Filtering Queries:")

print("\n   2.1 Basic WHERE clause with equality:")
engineering_employees = session.query(Employee).filter(Employee.department_id == 1).all()
print(f"   - Found {len(engineering_employees)} employees in Engineering:")
for emp in engineering_employees:
    print(f"      {emp.first_name} {emp.last_name}")

print("\n   2.2 Multiple filter conditions with AND:")
highly_paid_engineers = session.query(Employee).filter(
    and_(Employee.department_id == 1, Employee.salary > 80000)
).all()
print(f"   - Found {len(highly_paid_engineers)} highly paid engineers:")
for emp in highly_paid_engineers:
    print(f"      {emp.first_name} {emp.last_name}: ${emp.salary:,.2f}")

print("\n   2.3 OR conditions:")
support_or_hr = session.query(Employee).filter(
    or_(Employee.department_id == 4, Employee.department_id == 5)
).all()
print(f"   - Found {len(support_or_hr)} employees in HR or Customer Support:")
for emp in support_or_hr:
    print(f"      {emp.first_name} {emp.last_name} (Dept ID: {emp.department_id})")

print("\n   2.4 NOT conditions:")
not_sales = session.query(Employee).filter(
    Employee.department_id != 3
).all()
print(f"   - Found {len(not_sales)} employees not in Sales (first 3):")
for emp in not_sales[:3]:
    print(f"      {emp.first_name} {emp.last_name} (Dept ID: {emp.department_id})")
print("      ...")

print("\n   2.5 IN clause:")
specific_departments = session.query(Employee).filter(
    Employee.department_id.in_([1, 3])  # Engineering and Sales
).all()
print(f"   - Found {len(specific_departments)} employees in Engineering or Sales (first 3):")
for emp in specific_departments[:3]:
    print(f"      {emp.first_name} {emp.last_name} (Dept ID: {emp.department_id})")
print("      ...")

print("\n   2.6 LIKE clause for pattern matching:")
j_employees = session.query(Employee).filter(
    Employee.first_name.like('J%')  # Names starting with J
).all()
print(f"   - Found {len(j_employees)} employees with names starting with 'J':")
for emp in j_employees:
    print(f"      {emp.first_name} {emp.last_name}")

# Sorting Results
print("\n3. Sorting Results:")

print("\n   3.1 ORDER BY (ascending):")
employees_by_salary_asc = session.query(Employee).order_by(Employee.salary).all()
print("   - Employees ordered by salary (ascending, first 3):")
for emp in employees_by_salary_asc[:3]:
    print(f"      {emp.first_name} {emp.last_name}: ${emp.salary:,.2f}")
print("      ...")

print("\n   3.2 ORDER BY (descending):")
employees_by_salary_desc = session.query(Employee).order_by(desc(Employee.salary)).all()
print("   - Employees ordered by salary (descending, first 3):")
for emp in employees_by_salary_desc[:3]:
    print(f"      {emp.first_name} {emp.last_name}: ${emp.salary:,.2f}")
print("      ...")

print("\n   3.3 Multiple ORDER BY criteria:")
employees_by_dept_salary = session.query(Employee).order_by(
    Employee.department_id, desc(Employee.salary)
).all()
print("   - Employees ordered by department, then by salary (descending, first 3):")
for emp in employees_by_dept_salary[:3]:
    print(f"      Dept {emp.department_id}: {emp.first_name} {emp.last_name} - ${emp.salary:,.2f}")
print("      ...")

# Limiting Results
print("\n4. Limiting Results:")

print("\n   4.1 LIMIT clause:")
top_3_salaries = session.query(Employee).order_by(desc(Employee.salary)).limit(3).all()
print("   - Top 3 highest paid employees:")
for emp in top_3_salaries:
    print(f"      {emp.first_name} {emp.last_name}: ${emp.salary:,.2f}")

print("\n   4.2 LIMIT with OFFSET (for pagination):")
page_2 = session.query(Employee).order_by(Employee.id).offset(5).limit(5).all()
print("   - Page 2 (records 6-10) when paginating by 5 records:")
for emp in page_2:
    print(f"      {emp.id}: {emp.first_name} {emp.last_name}")

# Aggregation Queries
print("\n5. Aggregation Queries:")

print("\n   5.1 COUNT:")
employee_count = session.query(func.count(Employee.id)).scalar()
print(f"   - Total employee count: {employee_count}")

print("\n   5.2 AVG, MIN, MAX:")
salary_stats = session.query(
    func.avg(Employee.salary).label('avg_salary'),
    func.min(Employee.salary).label('min_salary'),
    func.max(Employee.salary).label('max_salary')
).first()

print(f"   - Salary statistics:")
print(f"      Average: ${salary_stats.avg_salary:,.2f}")
print(f"      Minimum: ${salary_stats.min_salary:,.2f}")
print(f"      Maximum: ${salary_stats.max_salary:,.2f}")

print("\n   5.3 GROUP BY:")
dept_counts = session.query(
    Employee.department_id,
    func.count(Employee.id).label('emp_count')
).group_by(Employee.department_id).all()

print("   - Employee count by department:")
for dept_id, count in dept_counts:
    dept = session.query(Department).get(dept_id)
    print(f"      {dept.name}: {count} employees")

print("\n   5.4 GROUP BY with HAVING:")
large_depts = session.query(
    Employee.department_id,
    func.count(Employee.id).label('emp_count')
).group_by(Employee.department_id).having(
    func.count(Employee.id) > 2
).all()

print("   - Departments with more than 2 employees:")
for dept_id, count in large_depts:
    dept = session.query(Department).get(dept_id)
    print(f"      {dept.name}: {count} employees")

# Joining Tables
print("\n6. Joining Tables:")

print("\n   6.1 Inner Join:")
employees_with_dept = session.query(
    Employee, Department
).join(
    Department, Employee.department_id == Department.id
).all()

print("   - Employees with their departments (first 3):")
for emp, dept in employees_with_dept[:3]:
    print(f"      {emp.first_name} {emp.last_name} works in {dept.name}")
print("      ...")

print("\n   6.2 Left Outer Join (includes employees without departments):")
# For demonstration purposes - in our sample data, all employees have departments
employees_left_join = session.query(
    Employee, Department
).outerjoin(
    Department, Employee.department_id == Department.id
).all()

print("   - All employees with departments (first 3, including those without):")
for emp, dept in employees_left_join[:3]:
    dept_name = dept.name if dept else "No Department"
    print(f"      {emp.first_name} {emp.last_name} works in {dept_name}")
print("      ...")

print("\n   6.3 Multiple Joins:")
employee_dept_address = session.query(
    Employee.first_name,
    Employee.last_name,
    Department.name.label('department'),
    Address.city,
    Address.state
).join(
    Department, Employee.department_id == Department.id
).join(
    Address, Employee.id == Address.employee_id
).all()

print("   - Employees with department and address (first 3):")
for first_name, last_name, dept, city, state in employee_dept_address[:3]:
    print(f"      {first_name} {last_name} works in {dept} and lives in {city}, {state}")
print("      ...")

# Subqueries
print("\n7. Subqueries:")

print("\n   7.1 Subquery in WHERE clause:")
# Find employees who earn more than the average salary
avg_salary = session.query(func.avg(Employee.salary)).scalar()
high_earners = session.query(Employee).filter(
    Employee.salary > avg_salary
).all()

print(f"   - Employees earning more than the average salary (${avg_salary:,.2f}):")
for emp in high_earners:
    print(f"      {emp.first_name} {emp.last_name}: ${emp.salary:,.2f}")

print("\n   7.2 Correlated Subquery:")
# Find employees who earn more than the average salary in their department
employees_above_dept_avg = session.query(Employee).filter(
    Employee.salary > session.query(
        func.avg(Employee.salary)
    ).filter(
        Employee.department_id == Employee.department_id
    ).scalar_subquery()
).all()

print("   - Employees earning more than their department average:")
for emp in employees_above_dept_avg:
    dept_avg = session.query(
        func.avg(Employee.salary)
    ).filter(
        Employee.department_id == emp.department_id
    ).scalar()
    print(f"      {emp.first_name} {emp.last_name}: ${emp.salary:,.2f} (dept avg: ${dept_avg:,.2f})")

# Loading Relationships
print("\n8. Loading Relationships:")

print("\n   8.1 Lazy Loading (default):")
# Demonstrate the N+1 problem
start_time = time.time()
departments = session.query(Department).all()
employee_count = 0
for dept in departments:
    # This triggers a separate query for each department
    employees = dept.employees
    employee_count += len(employees)
end_time = time.time()

print(f"   - Lazy loading: Retrieved {len(departments)} departments with a total of {employee_count} employees")
print(f"   - Time taken: {(end_time - start_time):.4f} seconds")

print("\n   8.2 Eager Loading with joinedload:")
# Solve the N+1 problem with eager loading
start_time = time.time()
departments = session.query(Department).options(joinedload(Department.employees)).all()
employee_count = 0
for dept in departments:
    # No additional queries here - data was loaded in the original query
    employees = dept.employees
    employee_count += len(employees)
end_time = time.time()

print(f"   - Eager loading (joinedload): Retrieved {len(departments)} departments with a total of {employee_count} employees")
print(f"   - Time taken: {(end_time - start_time):.4f} seconds")

print("\n   8.3 Eager Loading with subqueryload:")
# Alternative eager loading strategy
start_time = time.time()
departments = session.query(Department).options(subqueryload(Department.employees)).all()
employee_count = 0
for dept in departments:
    employees = dept.employees
    employee_count += len(employees)
end_time = time.time()

print(f"   - Eager loading (subqueryload): Retrieved {len(departments)} departments with a total of {employee_count} employees")
print(f"   - Time taken: {(end_time - start_time):.4f} seconds")

# Raw SQL
print("\n9. Working with Raw SQL:")

print("\n   9.1 Executing a Raw SQL Query:")
result = session.execute(
    text("SELECT e.first_name, e.last_name, d.name as department FROM employees e JOIN departments d ON e.department_id = d.id")
)
print("   - Results from raw SQL query (first 3):")
for row in list(result)[:3]:
    print(f"      {row.first_name} {row.last_name} - {row.department}")
print("      ...")

print("\n   9.2 Mapping Raw SQL Results to ORM Objects:")
result = session.execute(
    text("SELECT * FROM employees WHERE salary > :min_salary ORDER BY salary DESC"),
    {"min_salary": 80000}
)
# Convert result proxy to ORM objects
high_salary_employees = [Employee(**dict(row)) for row in result]
print(f"   - Mapped {len(high_salary_employees)} high-salary employees from raw SQL to ORM objects:")
for emp in high_salary_employees:
    print(f"      {emp.first_name} {emp.last_name}: ${emp.salary:,.2f}")

# Clean up
session.close()
print("\n10. Session closed")