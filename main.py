# Description: This file contains the FastAPI code to create a REST API that will run the task when a POST request is made to the /task endpoint. The task is run by calling the run_task function from the sample module. The task description is passed as a JSON payload in the request body.
import json
from typing import Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import browser_agent
from PIL import ImageFont


class Task(BaseModel):
    description: str = None


class TaskResponse(BaseModel):
    status: str
    result: Any


app = FastAPI()


@app.post("/task", response_model=TaskResponse)
async def do_task(task: Task):
    print(f"Received task: {task.description}")
    try:
        response = await browser_agent.run_task(task.description)
        return TaskResponse(status="success", result=response)
    except OSError as e:
        print(f"OSError: {e}")
        raise HTTPException(
            status_code=500, detail="Resource error occurred while processing the task."
        )
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        raise HTTPException(status_code=500, detail="Error decoding JSON response.")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while processing the task."
        )


@app.get("/")
async def index():
    print("Index endpoint called")
    response = {"message": "Welcome to the Task Runner API!"}
    return response
