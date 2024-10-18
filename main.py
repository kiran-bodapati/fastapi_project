from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer


from pydantic import BaseModel
from typing import Union,Annotated

from pymongo import MongoClient


client = MongoClient('mongodb://127.0.0.1:27017')
database = client["my_database"]
collection = database["my_collection"]

# first application running on port 8000
application = FastAPI()
'''Items data'''
items = {"items_list": [{"foo": "hi"}, {"bar": "hello"}, {"baz": "world"}]}
item_id = 5


@application.get("/")
def hello_world():
    return "hello world"


@application.get("/items/{item_id}", tags=["items"])
def get_item(item_id: int):
    # return f"{item_id}"
    return items["items_list"][item_id]


@application.put("/items/{item_id}", tags=["items"])
def put_item(item_id: int):
    print(len(items["items_list"]))
    if len(items["items_list"]) == item_id:
        print(items["items_list"])
        items["items_list"].append({"foobar": "hello_world"})
    return items


@application.get("/list_items", tags=["items"])
def get_all_items():
    return items


@application.post("/items/new_item", tags=["items"])
def post_new_item(new_dict: dict):
    items["items_list"].append(new_dict)
    return items


'''players_data'''
scores = {"player1": 90, "player2": 30}


@application.post("/players/new_palyer", tags=["scores"])
def new_player(new_player: dict):
    # scores[new_player.keys()]=new_player.values()
    # return scores
    scores.update(new_player)
    return scores


@application.delete("/players/{delete_player}", tags=["scores"])
def delete_player(delete_palyer: str):
    # del scores[f"{delete_palyer}"]
    print(scores)
    scores.popitem()
    print(scores)
    return scores


# second application running on port 5000
app = FastAPI()
'''students_data'''
students_info = [
    {
        "name": "kiran",
        "age": 0,
        "gender": "Male",

        "marks": {
            "additionalProp1": 0,
            "additionalProp2": 0,
            "additionalProp3": 0
        }
    },
    {
        "name": "differnet",
        "age": 29,
        "gender": "Male",

        "marks": {
            "subject1": 50,
            "subject2": 60,
            "subject3": 70
        }
    },
    {
        "name": "out_of_box",
        "age": 29,
        "gender": "Male",

        "marks": {
            "subject1": 50,
            "subject2": 60,
            "subject3": 70
        }
    },

]
'''Employees_data'''


class details(BaseModel):
    name: str
    age: int
    gender: str = "Male"
    parents_names: list[Union[str, None]] = None
    marks: dict[str, int]


@app.post("/add_student", tags=["students"], response_model=details)
def add_student(student_details: details):
    students_info.append(student_details)
    students_info.append(1)
    return students_info


@app.get("/get_student/", tags=["students"])
def get_details(q: int | None = None):
    print(students_info)
    if q:
        return students_info[q]
    else:
        return students_info


@app.patch("/change_student_data/{student_id}")
def patch_student_data(student_id: int, q: details):
    students_info[student_id] = q.model_dump(exclude_unset=True)
    return students_info[student_id]


'''Employees_data'''
class Employee(BaseModel):
    employee_id: int
    name: str
    gender: str
    age: int
    salary: int
    phone_number: list
    hikes: dict
    balance_leaves: float


@app.post("/add_employee/", response_model=Employee, tags=["employee"])
def add_new_employee(employee: Employee):
    employee_details = jsonable_encoder(employee)
    database.collection.insert_one(employee_details)
    # database.collection.insert_one(employee.model_dump())
    return employee


@app.get("/get_employee_details/{employee_id}", response_model=Employee, tags=["employee"])
def get_employee_details(employee_id: int):
    result = database.collection.find_one({"employee_id": employee_id})
    print(database.list_collection_names())
    print(database.collection.find())
    return result


@app.delete("/delete_employee/{employee_id}", tags=["employee"])
def delete_employee(employee_id: int):
    result = database.collection.delete_one({"employee_id": employee_id})
    return result
