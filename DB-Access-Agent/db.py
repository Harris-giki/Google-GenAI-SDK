from sqlalchemy import create_engine, text # importing components for database operations

# the text component/function allows wrting raw SQL queries safely in text form for the database

engine = create_engine("sqlite:///mydb.sqlite") # creating a connection with the database

def get_user_by_id(user_id: int):
    with engine.connect() as conn: # connecting with the database during interaction, also automatically closes it
        result = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id}) 
        # above is the parametrized binding for safe information injection in SQL queries using python, used instead of F-string literals
        # .excecute sends the Sql query to the database engine without returning the actual row to be fetched here
        # it returns an result object saved in result which basically points to where the data is placed in our DB
        row = result.fetchone()
        #fetching the row we are pointing to
        if row:
            return dict(row._mapping)  #Convert SQLAlchemy Row to dict safely
        else:
            return "User not found."
# this is how a dictionary look like

# {
#   "id": 1,
#   "name": "Haris",
#   "email": "haris@giki.edu.pk"
# }


def update_user_email(user_id: int, new_email: str):
    with engine.connect() as conn:
        conn.execute(text("UPDATE users SET email = :email WHERE id = :id"), {"email": new_email, "id": user_id})
        conn.commit()
        return "Email updated successfully"


# .connect, .execute, .commit etc are given by the create_engine component
# provided by sqlalchemy's python library.