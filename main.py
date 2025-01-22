# Description: This file contains the FastAPI code to create a REST API that will run the task when a POST request is made to the /task endpoint. The task is run by calling the run_task function from the sample module. The task description is passed as a JSON payload in the request body.
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sample
import logging
from logger_config import configure_logging

class Task(BaseModel):
    description: str = None

# Configure logging
logger = configure_logging()

app=FastAPI()

@app.post("/task")
async def do_task(task: Task):
    try:
        logger.info(f"Received task: {task.description}")
        response = await sample.run_task(task.description)
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        logger.info(f"Task response: {response}")
        return response
    except HTTPException as e:
        logger.error(f"HTTP error processing task: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Error processing task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def index():
    logger.info("Index endpoint called")
    response = {"message": "Welcome to the Task Runner API!"}
    return response
