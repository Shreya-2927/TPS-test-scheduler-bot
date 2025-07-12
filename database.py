import mysql.connector

# Step 1: Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",                # your MySQL username
    password="5604",   # your MySQL password
    database="school_db"        # the database you created in Workbench
)

cursor = conn.cursor()

# Create `teachers` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL
)
""")

# Create `students` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    class VARCHAR(10) NOT NULL,
    section VARCHAR(10) NOT NULL,
    roll_number INT NOT NULL,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
)
""")

# Create `questions` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    class VARCHAR(10) NOT NULL,
    section VARCHAR(10) NOT NULL,
    question TEXT NOT NULL,
    option1 VARCHAR(255) NOT NULL,
    option2 VARCHAR(255) NOT NULL,
    option3 VARCHAR(255) NOT NULL,
    option4 VARCHAR(255) NOT NULL,
    answer VARCHAR(255) NOT NULL,
    created_by VARCHAR(100) NOT NULL,
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

print("Tables created successfully.")

# Close the connection
cursor.close()
conn.close()