'''
4️⃣ CRUD Endpoints Summary
Method	          Endpoint	         Action
POST	        /students	       Create student
GET	            /students/{id}	   Read student
PUT	            /students/{id}	   Update student
DELETE	        /students/{id}	   Delete student
'''

# =========================================================
# 1. Importing Libraries:
# =========================================================
from fastapi import FastAPI
from pydantic import BaseModel

# =========================================================
# 2. Creating FastAPI Instance which will be used to define
#    routes (endpoints) and handle requests.
# =========================================================
app = FastAPI()

# =========================================================
# 3. Connecting to NeonDB. This is the connection string got from NeonDB
# =========================================================
db_url = (
    "postgresql://neondb_owner:npg_jFZ8tTRsiu1X"
    "@ep-withered-shadow-ahyotlry-pooler.c-3.us-east-1.aws.neon.tech/neondb"
    "?sslmode=require&channel_binding=require"
)

# =========================================================
# 4. Importing psycopg2 to connect to PostgreSQL.
#    pip install psycopg2-binary
# =========================================================
import psycopg2
from psycopg2.extras import RealDictCursor as real_dict_cursor
# import RealDictCursor class from psycopg2.extras module.
# real_dict_cursor is an alias for RealDictCursor which allows fetching rows as dictionaries.

# =========================================================
# 5. Check connection to NeonDB
# =========================================================
def get_connection():
    try:
        conn = psycopg2.connect(db_url, cursor_factory=real_dict_cursor)
        # conn is the connection object used to interact with the database.
        # cursor_factory is an optional parameter that allows you to specify a custom cursor class for the connection.
        # cursor_factory=real_dict_cursor to get results as dictionaries
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)

# =========================================================
# 5. Defining a Data Model:
# =========================================================
class Student(BaseModel):
    # Define a Pydantic model for the request body meaning to validate the data.
    # BaseModel is a base class provided by Pydantic which is used to create data models with type validation.
    id: int
    name: str
    age: int

# =========================================================
# 6. Define a POST endpoint at the specified URL path
# =========================================================
@app.post("/student_insert")
# Decorator to define a POST endpoint at the specified URL path

# =========================================================
# 7. Store student data in NeonDB
# =========================================================
def store_studentdata_in_neondb(Addstudent: Student):
    try:
        conn = get_connection()
        # conn is the connection object - connection string is opened

        cursor = conn.cursor()
        # meaning to create a cursor object using the connection.
        # A cursor is used to execute SQL queries and fetch results from the database.
        # cursor() method creates a new cursor object.

        sql_query = ("INSERT INTO student (id, name, age) VALUES (%s, %s, %s)")
        # SQL query to insert a new student record into the students table.
        # The %s placeholders will be replaced with actual values.
        # insert_query is a string variable that holds the SQL query.

        cursor.execute(sql_query, (Addstudent.id, Addstudent.name, Addstudent.age)) 
        # Execute the SQL query using the cursor object.
        
        conn.commit()
        # Commit the transaction

        cursor.close()
        conn.close()

        return {
            "message": "Student created and stored in database successfully",
            "student_id": Addstudent.id,
            "student_name": Addstudent.name,
            "student_age": Addstudent.age   
        }

    except Exception as e:
        return {"error": str(e)}

