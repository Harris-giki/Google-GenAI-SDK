from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///mydb.sqlite")

def get_user_by_id(user_id: int):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
        row = result.fetchone()
        if row:
            return dict(row._mapping)  #Convert SQLAlchemy Row to dict safely
        else:
            return "User not found."

def update_user_email(user_id: int, new_email: str):
    with engine.connect() as conn:
        conn.execute(text("UPDATE users SET email = :email WHERE id = :id"), {"email": new_email, "id": user_id})
        conn.commit()
        return "Email updated successfully"
