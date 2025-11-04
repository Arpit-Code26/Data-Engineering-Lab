import psycopg2
from psycopg2 import sql

# ---!! IMPORTANT !! ---
# 1. UPDATE this with your own PostgreSQL credentials
DB_CONFIG = {
    'dbname': 'exp66',
    'user': 'postgres',
    'password': 'myretailpass', # e.g., 'admin'
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error: Unable to connect to the database. {e}")
        return None

def initialize_database():
    """Creates the necessary tables if they don't already exist."""
    
    # Combined SQL commands to create tables
    commands = """
        CREATE TABLE IF NOT EXISTS departments (
            dept_id SERIAL PRIMARY KEY,
            dept_name VARCHAR(100) UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS roles (
            role_id SERIAL PRIMARY KEY,
            role_title VARCHAR(100) NOT NULL,
            dept_id INTEGER NOT NULL,
            FOREIGN KEY (dept_id) REFERENCES departments (dept_id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS employees (
            emp_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            role_id INTEGER, 
            FOREIGN KEY (role_id) REFERENCES roles (role_id) ON DELETE SET NULL
        );
        """
    
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: return
        cur = conn.cursor()
        cur.execute(commands) # Execute all commands at once
        conn.commit()
        cur.close()
        print("Database tables initialized successfully.")
    except psycopg2.Error as e:
        print(f"Error initializing database: {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()

# --- Main Application Logic ---
if __name__ == "__main__":
    
    # 2. Run this to create the tables
    initialize_database()
    
    while True:
        print("\n===== Employee Management System =====")
        print("1. Add Department")
        print("2. Add Role")
        print("3. Add Employee")
        print("4. View All Employees")
        print("5. View All Departments")
        print("6. View All Roles")
        print("7. Delete Employee")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ")
        conn = None # Initialize conn
        
        try:
            conn = get_db_connection()
            if conn is None and choice != '8':
                print("Database connection failed. Check config.")
                continue

            cur = conn.cursor()

            if choice == '1': # Create Department
                name = input("Enter department name: ")
                cur.execute("INSERT INTO departments (dept_name) VALUES (%s)", (name,))
                conn.commit()
                print(f"Added department: {name}")

            elif choice == '2': # Create Role
                title = input("Enter role title: ")
                dept_id = input("Enter department ID: ")
                cur.execute("INSERT INTO roles (role_title, dept_id) VALUES (%s, %s)", (title, int(dept_id)))
                conn.commit()
                print(f"Added role: {title}")

            elif choice == '3': # Create Employee
                first = input("Enter first name: ")
                last = input("Enter last name: ")
                email = input("Enter email: ")
                role_id = input("Enter role ID: ")
                cur.execute(
                    "INSERT INTO employees (first_name, last_name, email, role_id) VALUES (%s, %s, %s, %s)",
                    (first, last, email, int(role_id))
                )
                conn.commit()
                print(f"Added employee: {first} {last}")

            elif choice == '4': # Read Employees
                cur.execute("""
                    SELECT e.emp_id, e.first_name, e.last_name, r.role_title, d.dept_name
                    FROM employees e
                    LEFT JOIN roles r ON e.role_id = r.role_id
                    LEFT JOIN departments d ON r.dept_id = d.dept_id
                """)
                employees = cur.fetchall()
                print("\n--- All Employees ---")
                if not employees: print("No employees found.")
                for emp in employees:
                    print(f"ID: {emp[0]}, Name: {emp[1]} {emp[2]}, Role: {emp[3] or 'N/A'}, Dept: {emp[4] or 'N/A'}")
            
            elif choice == '5': # Read Departments
                cur.execute("SELECT * FROM departments")
                depts = cur.fetchall()
                print("\n--- All Departments ---")
                if not depts: print("No departments found.")
                for dept in depts:
                    print(f"ID: {dept[0]}, Name: {dept[1]}")

            elif choice == '6': # Read Roles
                cur.execute("SELECT r.role_id, r.role_title, d.dept_name FROM roles r JOIN departments d ON r.dept_id = d.dept_id")
                roles = cur.fetchall()
                print("\n--- All Roles ---")
                if not roles: print("No roles found.")
                for role in roles:
                    print(f"ID: {role[0]}, Title: {role[1]}, Dept: {role[2]}")

            elif choice == '7': # Delete Employee
                emp_id = input("Enter Employee ID to delete: ")
                cur.execute("DELETE FROM employees WHERE emp_id = %s", (int(emp_id),))
                conn.commit()
                print(f"Deleted employee ID {emp_id}")

            elif choice == '8':
                print("Exiting.")
                if conn: conn.close() # Close connection on exit
                break

            else:
                print("Invalid choice.")

        except (psycopg2.Error, ValueError) as e:
            print(f"An error occurred: {e}")
            if conn: conn.rollback() # Roll back any failed transaction
        
        finally:
            # Close cursor and connection
            if cur: cur.close()
            if conn: conn.close()