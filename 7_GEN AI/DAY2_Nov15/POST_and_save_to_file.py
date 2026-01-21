# 1️⃣ Import Libraries
from fastapi import FastAPI
from pydantic import BaseModel

# 2️⃣ Create FastAPI Instance
# This instance will be used to define API endpoints and handle HTTP requests
app = FastAPI()

# 3️⃣ Define Data Model
# Pydantic model validates incoming data types automatically
class AddStudent(BaseModel):
    id: int       # Student ID
    name: str     # Student Name
    age: int      # Student Age

# 4️⃣ Function to Save Student Data to File
def save_student_to_file(new_student: dict):
    """
    Appends student information to 'students.txt'.
    
    Args:
        new_student (dict): Dictionary containing student data
    """
    with open("students.txt", "a") as file:
        file.write(
            f"ID: {new_student['id']}, Name: {new_student['name']}, Age: {new_student['age']}\n"
        )

# 5️⃣ Endpoint to Handle POST Requests
@app.post("/create_student")
def create_student(student: AddStudent):
    """
    Adds a new student.
    
    Steps:
        1. Convert Pydantic object to dictionary
        2. Save student details to a file
        3. Return a success message with student data
    """
    # Convert Pydantic object to dictionary (Pydantic v2)
    student_details = student.model_dump()

    # Save student details to file
    save_student_to_file(student_details)

    # Return success message with student data
    return {
        "message": "Student created successfully",
        "student": student_details
    }

