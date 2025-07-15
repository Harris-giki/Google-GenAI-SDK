from sqlalchemy import create_engine, text

# Create or connect to the SQLite database
engine = create_engine("sqlite:///mydb.sqlite")

# Step 1: Create the 'users' table
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """))
    conn.commit()

# Step 2: Insert some sample data
with engine.connect() as conn:
    conn.execute(text("INSERT INTO users (name, email) VALUES (:name, :email)"),
                 {"name": "Haris", "email": "haris@giki.edu.pk"})
    conn.execute(text("INSERT INTO users (name, email) VALUES (:name, :email)"),
                 {"name": "Sara", "email": "sara@example.com"})
    conn.commit()

print("Database created and sample data inserted.")
