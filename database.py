import mysql.connector

# Step 1: Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",                # your MySQL username
    password="5604",            # your MySQL password
    database="school_db"        # the database you created in Workbench
)

cursor = conn.cursor()

# ! This is for the teachers.
# Create `teachers` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100), -- optional
    password VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL
)
""")

# ! This is to add students in the students table
cursor.execute("""
INSERT IGNORE INTO teachers (id, password, name)
VALUES (%s, %s, %s)
""", (2068, 1112, "Gyanesh"))
conn.commit()

# ! This is for the students
# Create `students` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    class VARCHAR(10) NOT NULL,
    section VARCHAR(10) NOT NULL,
    roll_number INT NOT NULL,
    username VARCHAR(100),  -- optional
    password VARCHAR(100) NOT NULL
)
""")

# ! This is to add students in the students table
cursor.execute("""
INSERT IGNORE INTO students (id, name, class, section, roll_number, username, password)
VALUES (%s, %s, %s, %s, %s, %s, %s)
""", (2927, "Shreya", "10", "A", 1, None, 9999))
conn.commit()

cursor.execute("""
INSERT IGNORE INTO students (id, name, class, section, roll_number, username, password)
VALUES (%s, %s, %s, %s, %s, %s, %s)
""", (5604, "Yugansh", "10", "A", 2, None, 9998))
conn.commit()


# ! This is for the questions.
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

print("Executoin Complete")

# Close the connection
cursor.close()
conn.close()