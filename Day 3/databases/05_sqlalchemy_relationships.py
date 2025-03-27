import os
from datetime import datetime
from sqlalchemy import create_engine, ForeignKey, Table, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref

# Create a database directory if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# Create SQLAlchemy engine and base
db_path = os.path.abspath("data/sqlalchemy_relationships.db")
engine = create_engine(f"sqlite:///{db_path}", echo=False)
Base = declarative_base()

# 1. Introduction to Database Relationships
print("\n1. Database Relationship Types:")
relationship_types = {
    "One-to-Many (1:N)": "One record in table A can be referenced by many records in table B",
    "Many-to-One (N:1)": "Many records in table A can reference one record in table B",
    "One-to-One (1:1)": "One record in table A references exactly one record in table B",
    "Many-to-Many (N:M)": "Many records in table A can reference many records in table B (requires junction table)"
}

# 2. One-to-Many Relationship Example
print("\n2. One-to-Many (1:N) Relationship:")
print("   Example: Department -> Employees (one department has many employees)")

# Define the models for one-to-many relationship
class Department(Base):
    __tablename__ = 'departments'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    location = Column(String(100))
    
    # The 'employees' relationship attribute will be created below
    
    def __repr__(self):
        return f"<Department(id={self.id}, name='{self.name}')>"

class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    # Foreign key to link to the department
    department_id = Column(Integer, ForeignKey('departments.id'))
    hire_date = Column(DateTime, default=datetime.utcnow)
    salary = Column(Float)
    
    # Relationship - the many side of one-to-many
    # Using back_populates to create a bidirectional relationship
    department = relationship("Department", back_populates="employees")
    
    def __repr__(self):
        return f"<Employee(id={self.id}, name='{self.name}', department_id={self.department_id})>"

# Create the relationship attribute on Department
Department.employees = relationship("Employee", back_populates="department", 
                                 cascade="all, delete-orphan")

print("\n   Department model represents the 'one' side:")
print("   - One department can have many employees")
print("   - 'employees' is a collection attribute on Department instances")
print("   - No foreign key on Department")

print("\n   Employee model represents the 'many' side:")
print("   - Many employees belong to one department")
print("   - 'department_id' is a foreign key column to departments.id")
print("   - 'department' is a reference attribute on Employee instances")

# 3. Many-to-Many Relationship Example
print("\n3. Many-to-Many (N:M) Relationship:")
print("   Example: Students <-> Courses (students take many courses, courses have many students)")

# Association table for many-to-many relationship
enrollment = Table(
    'enrollments', 
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True),
    Column('enrollment_date', DateTime, default=datetime.utcnow),
    Column('grade', String(2))
)

# Define the models for many-to-many relationship
class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    
    # Many-to-many relationship - students can be in many courses
    # secondary specifies the association table
    courses = relationship("Course", secondary=enrollment, back_populates="students")
    
    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}')>"

class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Many-to-many relationship - courses can have many students
    students = relationship("Student", secondary=enrollment, back_populates="courses")
    
    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.title}')>"

print("\n   Association Table (enrollments):")
print("   - Junction table linking students and courses")
print("   - Contains student_id and course_id foreign keys")
print("   - Can include additional attributes about the relationship")
print("      - enrollment_date, grade, etc.")

print("\n   Student model has a 'courses' relationship:")
print("   - Many students can enroll in many courses")
print("   - 'secondary' parameter specifies the association table")

print("\n   Course model has a 'students' relationship:")
print("   - Many courses can have many students")
print("   - 'secondary' parameter specifies the association table")

# 4. One-to-One Relationship Example
print("\n4. One-to-One (1:1) Relationship:")
print("   Example: User -> Profile (one user has exactly one profile)")

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # One-to-one relationship with Profile
    # uselist=False means it's a scalar (not a list)
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class Profile(Base):
    __tablename__ = 'profiles'
    
    id = Column(Integer, primary_key=True)
    # One-to-one foreign key with unique constraint
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    full_name = Column(String(100))
    bio = Column(Text)
    birth_date = Column(DateTime)
    
    # One-to-one relationship with User
    user = relationship("User", back_populates="profile")
    
    def __repr__(self):
        return f"<Profile(id={self.id}, user_id={self.user_id}, full_name='{self.full_name}')>"

print("\n   User model has a 'profile' attribute:")
print("   - uselist=False makes it a one-to-one (not a collection)")
print("   - Each user has exactly one profile")

print("\n   Profile model has:")
print("   - user_id foreign key with unique constraint")
print("   - user attribute for the associated User instance")

# 5. Self-Referential Relationship Example
print("\n5. Self-Referential Relationship:")
print("   Example: Employees with Managers (employees can manage other employees)")

class Manager(Base):
    __tablename__ = 'managers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    title = Column(String(100))
    
    # Self-referential relationship - managers can have many subordinates
    manager_id = Column(Integer, ForeignKey('managers.id'))
    
    # Relationship attribute referring to the same class
    subordinates = relationship("Manager", 
                              backref=backref("manager", remote_side=[id]),
                              cascade="all, delete")
    
    def __repr__(self):
        return f"<Manager(id={self.id}, name='{self.name}', manager_id={self.manager_id})>"

print("\n   Manager model with self-referential relationship:")
print("   - manager_id is a foreign key to the same table")
print("   - 'subordinates' attribute is a collection of managed employees")
print("   - 'manager' attribute (via backref) points to the manager")
print("   - remote_side=[id] indicates the 'many' side of the relationship")

# 6. Creating all tables
Base.metadata.create_all(engine)
print("\n6. Created all database tables with relationships")

# 7. Using relationships - Adding sample data
print("\n7. Working with Relationships - Sample Data:")

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# One-to-Many: Department and Employees
print("\n   7.1 One-to-Many Example:")

# Creating departments
engineering = Department(name="Engineering", location="Building A")
marketing = Department(name="Marketing", location="Building B")
hr = Department(name="Human Resources", location="Building B")

# Creating employees and associating with departments
# Method 1: Set department attribute 
alice = Employee(name="Alice Smith", salary=85000.0)
alice.department = engineering  # This sets the department_id automatically

# Method 2: Add to department's employees collection
bob = Employee(name="Bob Johnson", salary=72000.0)
engineering.employees.append(bob)  # This sets the department_id automatically

# Method 3: Set department_id directly
charlie = Employee(name="Charlie Williams", department_id=1, salary=92000.0)

# More employees
dave = Employee(name="Dave Brown", department=marketing, salary=68000.0)
emma = Employee(name="Emma Davis", department=marketing, salary=74000.0)
frank = Employee(name="Frank Miller", department=hr, salary=65000.0)

session.add_all([engineering, marketing, hr])
session.add_all([alice, bob, charlie, dave, emma, frank])
session.commit()

# Query to show the relationships
eng_dept = session.query(Department).filter_by(name="Engineering").first()
print(f"   Department: {eng_dept.name}")
print("   Employees:")
for emp in eng_dept.employees:
    print(f"      - {emp.name} (${emp.salary:,.2f})")

print("\n   Employee: {0}".format(alice.name))
print(f"   Works in: {alice.department.name} department")

# Many-to-Many: Students and Courses
print("\n   7.2 Many-to-Many Example:")

# Creating students
john = Student(name="John Anderson", email="john@example.com")
sarah = Student(name="Sarah Wilson", email="sarah@example.com")
michael = Student(name="Michael Taylor", email="michael@example.com")

# Creating courses
python = Course(title="Advanced Python", description="In-depth Python programming")
data_science = Course(title="Data Science", description="Introduction to data analysis")
web_dev = Course(title="Web Development", description="Building web applications")

# Enrolling students in courses
# Method 1: Add course to student's courses
john.courses.append(python)
john.courses.append(data_science)

# Method 2: Add student to course's students
data_science.students.append(sarah)
web_dev.students.append(sarah)

# Method 3: Add multiple courses to a student
michael.courses = [python, web_dev]

session.add_all([john, sarah, michael, python, data_science, web_dev])
session.commit()

# Update enrollment grades
enrollments = session.execute(enrollment.select()).fetchall()
for i, (student_id, course_id, enroll_date, grade) in enumerate(enrollments):
    # Set some sample grades
    session.execute(
        enrollment.update().where(
            (enrollment.c.student_id == student_id) & 
            (enrollment.c.course_id == course_id)
        ).values(grade=["A", "B+", "A-", "B", "C+"][i % 5])
    )
session.commit()

# Query to show the relationships
python_course = session.query(Course).filter_by(title="Advanced Python").first()
print(f"   Course: {python_course.title}")
print("   Students enrolled:")
for student in python_course.students:
    # Get enrollment details
    enrollment_details = session.execute(
        enrollment.select().where(
            (enrollment.c.student_id == student.id) & 
            (enrollment.c.course_id == python_course.id)
        )
    ).fetchone()
    grade = enrollment_details.grade if enrollment_details.grade else "N/A"
    print(f"      - {student.name} (Grade: {grade})")

print("\n   Student: {0}".format(john.name))
print("   Enrolled in courses:")
for course in john.courses:
    # Get enrollment details
    enrollment_details = session.execute(
        enrollment.select().where(
            (enrollment.c.student_id == john.id) & 
            (enrollment.c.course_id == course.id)
        )
    ).fetchone()
    grade = enrollment_details.grade if enrollment_details.grade else "N/A"
    print(f"      - {course.title} (Grade: {grade})")

# One-to-One: User and Profile
print("\n   7.3 One-to-One Example:")

# Creating users with profiles
user1 = User(username="jsmith", email="jsmith@example.com")
profile1 = Profile(full_name="John Smith", bio="Software developer")
user1.profile = profile1  # Assign profile to user

user2 = User(username="mwilson", email="mwilson@example.com")
# Create profile directly on the user instance
user2.profile = Profile(full_name="Mary Wilson", bio="Data scientist")

session.add_all([user1, user2])
session.commit()

# Query to show the relationship
user = session.query(User).filter_by(username="jsmith").first()
print(f"   User: {user.username}")
print(f"   Profile: {user.profile.full_name}")
print(f"   Bio: {user.profile.bio}")

# Starting from profile
profile = session.query(Profile).filter_by(full_name="Mary Wilson").first()
print(f"\n   Profile: {profile.full_name}")
print(f"   User: {profile.user.username}")
print(f"   Email: {profile.user.email}")

# Self-Referential: Managers and Subordinates
print("\n   7.4 Self-Referential Example:")

# Creating a management hierarchy
ceo = Manager(name="Jane Smith", title="CEO")
cto = Manager(name="Bob Johnson", title="CTO")
cfo = Manager(name="Alice Brown", title="CFO")

# CTO and CFO report to CEO
cto.manager = ceo
cfo.manager = ceo

# Creating subordinates for CTO
dev_manager = Manager(name="Dave Wilson", title="Development Manager", manager=cto)
qa_manager = Manager(name="Sarah Miller", title="QA Manager", manager=cto)

# Creating subordinates for Development Manager
dev1 = Manager(name="Chris Davis", title="Senior Developer", manager=dev_manager)
dev2 = Manager(name="Emily White", title="Developer", manager=dev_manager)

session.add_all([ceo, cto, cfo, dev_manager, qa_manager, dev1, dev2])
session.commit()

# Query to show the hierarchy
top_manager = session.query(Manager).filter_by(name="Jane Smith").first()
print(f"   Top Manager: {top_manager.name} ({top_manager.title})")
print("   Direct Reports:")
for subordinate in top_manager.subordinates:
    print(f"      - {subordinate.name} ({subordinate.title})")
    if subordinate.subordinates:
        print(f"        Subordinates of {subordinate.name}:")
        for sub_subordinate in subordinate.subordinates:
            print(f"          - {sub_subordinate.name} ({sub_subordinate.title})")
            if sub_subordinate.subordinates:
                print(f"            Subordinates of {sub_subordinate.name}:")
                for sub_sub_subordinate in sub_subordinate.subordinates:
                    print(f"              - {sub_sub_subordinate.name} ({sub_sub_subordinate.title})")

# Starting from a lower-level manager
dev = session.query(Manager).filter_by(name="Chris Davis").first()
print(f"\n   Employee: {dev.name} ({dev.title})")
print(f"   Reports to: {dev.manager.name} ({dev.manager.title})")
print(f"   Manager's manager: {dev.manager.manager.name} ({dev.manager.manager.title})")

# Clean up
session.close()
print("\n8. Session closed")