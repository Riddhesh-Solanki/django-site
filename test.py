import mysql.connector
from mysql.connector import Error

# ── 1. Connect ──────────────────────────────────────────────
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,           # default MySQL port
            user="root",         # your MySQL username
            password="ROOT",         # your MySQL password (XAMPP default is empty)
            database="testdb"    # database you created above
        )
        if conn.is_connected():
            print("✅ Connected to MySQL on localhost")
            return conn
    except Error as e:
        print(f"❌ Connection failed: {e}")
        return None


# ── 2. Create Table ─────────────────────────────────────────
def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id    INT AUTO_INCREMENT PRIMARY KEY,
            name  VARCHAR(100) NOT NULL,
            age   INT,
            email VARCHAR(100)
        )
    """)
    print("✅ Table 'students' ready.")


# ── 3. Insert Data ──────────────────────────────────────────
def insert_data(cursor, conn):
    students = [
        ("Rahul Sharma",  21, "rahul@example.com"),
        ("Priya Patel",   22, "priya@example.com"),
        ("Arjun Mehta",   20, "arjun@example.com"),
    ]
    sql = "INSERT INTO students (name, age, email) VALUES (%s, %s, %s)"
    cursor.executemany(sql, students)
    conn.commit()
    print(f"✅ {cursor.rowcount} rows inserted.")


# ── 4. Read Data ────────────────────────────────────────────
def read_data(cursor):
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    print("\n📋 Students Table:")
    print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Email'}")
    print("-" * 55)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<5} {row[3]}")


# ── 5. Update Data ──────────────────────────────────────────
def update_data(cursor, conn):
    sql = "UPDATE students SET age = %s WHERE name = %s"
    cursor.execute(sql, (25, "Rahul Sharma"))
    conn.commit()
    print(f"\n✅ Updated {cursor.rowcount} row(s).")


# ── 6. Delete Data ──────────────────────────────────────────
def delete_data(cursor, conn):
    sql = "DELETE FROM students WHERE name = %s"
    cursor.execute(sql, ("Arjun Mehta",))
    conn.commit()
    print(f"✅ Deleted {cursor.rowcount} row(s).")


# ── 7. Main ─────────────────────────────────────────────────
def main():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()

    create_table(cursor)
    insert_data(cursor, conn)
    read_data(cursor)
    update_data(cursor, conn)
    print("\n📋 After Update:")
    read_data(cursor)
    delete_data(cursor, conn)
    print("\n📋 After Delete:")
    read_data(cursor)

    cursor.close()
    conn.close()
    print("\n🔒 Connection closed.")


if __name__ == "__main__":
    main()