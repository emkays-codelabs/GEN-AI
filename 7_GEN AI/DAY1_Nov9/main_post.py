from fastapi import FastAPI # Meaning "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints."

from pydantic import BaseModel

app =FastAPI() # Create an instance of the FastAPI class

students = {1: "mk", 2: "vk", 3: "ck"}

@app.post("/add_student_by_post") # post method 
def add_student_by_post():    
    students['new_student_id'] = "new_name"  
    return students

#------------------------------------------------------------------------------------------------------------

# To test use postman or insomnia or httpie or curl
# http POST http://
# uvicorn main_post:app --reload
# Example using httpie
# http POST http://localhost:8000/add_student_by_post
# Example to add new data by passing dictionary in post method

students = {1: "mk", 2: "vk", 3: "ck"}
from pydantic import BaseModel

class Student(BaseModel): # Define a Pydantic model for the request body meaning to validate the data. BaseModel is a base class provided by Pydantic which is used to create data models with type validation.
    
    id: int
    name: str

@app.post("/add_student_by_post_with_dict")
def add_student_by_post_with_dict(new_student: Student): # new_student is an instance of Student model
    students[new_student.id] = new_student.name
    return students

# To test use postman --click select POST method, insert url and select Body -> Raw -> JSON    
# http POST http://localhost:8000/add_student_by_post_with_dict id=4 name="new_student_name"

'''
POST JSON
  { "id": 4, "name": "ak" }
       |
       v
FastAPI reads request body
       |
       v
Parses JSON → FastAPI reads request body in JSON format and converts it to a Python dictionary.
       |
       v
Creates Pydantic model
  new_student = Student(id=4, name="ak")
       |
       v
Passed into your function:
def add_student_by_post_with_dict(new_student: Student)
       |
       v
Use new_student.id and new_student.name
'''