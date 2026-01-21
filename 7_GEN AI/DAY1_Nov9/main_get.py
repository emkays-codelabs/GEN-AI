from fastapi import FastAPI # Meaning "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints."
from pydantic import BaseModel # import BaseModel class from pydantic module meaning "pydantic is a library for validating data in Python".

app =FastAPI() # Create an instance of the FastAPI class

#===============================================================================

@app.get("/") # Decorator to define a GET endpoint at the root URL
def test():
    return {"message": "Hello World"} # why curly braces? Because FastAPI automatically converts the dictionary to a JSON format.
    
@app.get("/mk")
def test1():
    return "my name is mahesh"
    
# Make changes to the code, always have to re-run api.
# To avoid re-run everytine use uvicorn main:app --reload 

@app.get("/mk/ssas/ass/assSSAS")
def test2():
    return "my name is mahesh KUMAR"
    
#===============================================================================
   
students = {1: "mk", 2: "vk", 3: "ck"}

@app.get("/students") 
def get_students():
    return {
    "count": len(students),
    "students": students
}

    
@app.get("/student_search/{student_id}") # 
def student_search(student_id: int):
    return students.get(student_id, "student not found") # dictionary.get(keyname, value) 
    
@app.get("/student_detail/{student_id}") # {} to parameterize the student_id
def get_student_detail(student_id: int):
    return {"student id": student_id, "name": students[student_id]}

@app.get("/add_student/{student_id}/{name}")
def add_student(student_id: int, name: str):
    students[student_id] = name
    return students
