# Description: This file contains the FastAPI code to create a REST API that will run the task when a POST request is made to the /task endpoint. The task is run by calling the run_task function from the sample module. The task description is passed as a JSON payload in the request body.
from fastapi import FastAPI
from pydantic import BaseModel
import sample


class Task(BaseModel):
    description: str = None


class TaskResponse(BaseModel):
    status: str
    result: str


app = FastAPI()


@app.post("/task")
async def do_task(task: Task):
    print(f"Received task: {task.description}")
    response = await sample.run_task(task.description)
    # if "error" in response:
    #     raise HTTPException(status_code=500, detail=response["error"])
    print(f"Task response: {response}")
    return response


@app.get("/")
async def index():
    print("Index endpoint called")
    response = {"message": "Welcome to the Task Runner API!"}
    return response
