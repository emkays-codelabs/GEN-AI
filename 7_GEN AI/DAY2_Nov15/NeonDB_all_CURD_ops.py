'''
4️⃣ CRUD Endpoints Summary
Method	          Endpoint	         Action
POST	        /students	       Create student
GET	            /students/{id}	   Read student
PUT	            /students/{id}	   Update student
DELETE	        /students/{id}	   Delete student
'''
# =========================================================
# 1. Import Required Libraries
# =========================================================
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from dotenv import load_dotenv

# =========================================================
# 2. Load Environment Variables
# =========================================================
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# =========================================================
# 3. Initialize FastAPI App
# =========================================================
app = FastAPI(title="Student Management API")

# =========================================================
# 4. Database Connection Helper
# =========================================================
def get_connection():
    """
    Returns a new database connection.
    Uses RealDictCursor to fetch results as dictionaries.
    """
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

# =========================================================
# 5. Pydantic Models
# =========================================================
class Student(BaseModel):
    """
    Model for creating a new student
    """
    id: int
    name: str
    age: int

class StudentUpdate(BaseModel):
    """
    Model for updating an existing student
    Only name and age can be updated
    """
    name: str
    age: int

# =========================================================
# 6. CREATE: Add New Student
# =========================================================
@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: Student):
    """
    Create a new student record in the database
    """
    query = """
        INSERT INTO student (id, name, age)
        VALUES (%s, %s, %s)
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (student.id, student.name, student.age))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Student created successfully"}
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="Student already exists")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# =========================================================
# 7. READ: Get Student by ID
# =========================================================
@app.get("/students/{student_id}")
def get_student(student_id: int):
    """
    Retrieve a student record by ID
    """
    query = "SELECT * FROM student WHERE id = %s"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, (student_id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# =========================================================
# 8. UPDATE: Update Existing Student
# =========================================================
@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    """
    Update the name and age of a student by ID
    """
    query = """
        UPDATE student
        SET name = %s,
            age = %s
        WHERE id = %s
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, (student.name, student.age, student_id))
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")

    cursor.close()
    conn.close()
    return {"message": "Student updated successfully"}

# =========================================================
# 9. DELETE: Remove Student by ID
# =========================================================
@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int):
    """
    Delete a student record by ID
    """
    query = "DELETE FROM student WHERE id = %s"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, (student_id,))
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")

    cursor.close()
    conn.close()
