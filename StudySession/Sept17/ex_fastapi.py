from fastapi import FastAPI
from pydantic import BaseModel

# FastAPI() object
app = FastAPI()


class Student(BaseModel):
    name: str
    age: int | None = None
    school: str = "USF"


class Output(BaseModel):
    output: str = "Thank you"
    key: str


students = {}


@app.post("/add_student", response_model=Output)
def add_student(student: Student):
    students[student.name] = student
    # {"lynn" : {"name" :"Lynn", "age":None, "school": "USF"}}
    return {"key": student.name,
            "school": student.school,
            "output": "Bye"}
