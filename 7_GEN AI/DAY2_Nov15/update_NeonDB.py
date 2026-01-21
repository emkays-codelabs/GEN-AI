
from fastapi import FastAPI
from pydantic import BaseModel  
import psycopg2
from psycopg2.extras import RealDictCursor as real_dict_cursor 

app = FastAPI()

db_url = "postgresql://neondb_owner:npg_jFZ8tTRsiu1X@ep-withered-shadow-ahyotlry-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def get_connection():
    try:
        conn = psycopg2.connect(db_url, cursor_factory=real_dict_cursor) 
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)

class AddStudent(BaseModel): 
    id: int
    name: str
    age: int

@app.post("/update_studentdata_in_neondb") # Decorator to define a POST endpoint at the specified URL path


def store_studentdata_in_neondb(student: AddStudent):
    try:
        conn = get_connection()  
        cursor = conn.cursor() 
        
        update_query = "UPDATE student SET name = %s,age = %s WHERE id = %s"

        cursor.execute(update_query, ( student.name, student.age,student.id))      
        conn.commit()  # Commit the transaction
        cursor.close()
        conn.close()
        return {
            "message": "Student created and stored in database successfully",
            "student_id": student.id,
            "student_name": student.name,
            "student_age": student.age
        }
    except Exception as e:
        return {"error": str(e)}


