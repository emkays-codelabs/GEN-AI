# 1. Importing Libraries: 

from fastapi import FastAPI
from pydantic import BaseModel  

# 2. Creating FastAPI Instance which will be used to define routes (endpoints) and handle requests.

app = FastAPI()

# 3.Defining a Data Model: 

class AddStudent(BaseModel): # Define a Pydantic model for the request body meaning to validate the data. BaseModel is a base class provided by Pydantic which is used to create data models with type validation. 
    id: int
    name: str
    age: int
    
# 4. Creating an Endpoint to Handle POST Requests:

@app.post("/create_student")
# When a request to this endpoint is made, it expects a JSON payload that matches the AddStudent model.
def create_student(student: AddStudent): # student is an instance of AddStudent model because of which we can access its attributes like id, name, age
    """
    Before calling def create_student(student: AddStudent):, code instantiates AddStudent by passing values to its constructor, such as student = AddStudent(id=123, name="Alice", age=20). The type hint AddStudent indicates the expected class, ensuring the parameter is a pre-created object with populated attributes.
    """
# 5. Response from the Endpoint: 
    return {
        "message": "Student created successfully",
        "student_id": student.id,
        "student_name": student.name,
        "student_age": student.age
    }
    
# The attributes are accessed directly from the student instance that was passed into the function.
    
    

    
    
