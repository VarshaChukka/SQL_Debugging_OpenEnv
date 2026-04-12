from fastapi import FastAPI, HTTPException
from app.env import SQLEnv
from app.models import Action

app = FastAPI()
env = SQLEnv()


#Home
@app.get("/")
def home():
    return {"message": "SQL OpenEnv Running"}


#FIXED: Reset must be POST (not GET)
@app.post("/reset")
def reset(task_id: int = 0):
    try:
        return env.reset(task_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


#Step (already correct)
@app.post("/step")
def step(action: Action):
    return env.step(action)


#Tasks list
@app.get("/tasks")
def tasks():
    return {
        "tasks": [
            {"id": 0, "level": "easy"},
            {"id": 1, "level": "medium"},
            {"id": 2, "level": "hard"}
        ]
    }


#State
@app.get("/state")
def state():
    return env.state()


#Grader
@app.get("/grader")
def grader():
    return {"message": "Grading happens during step execution"}


#Baseline
@app.get("/baseline")
def baseline():
    return {"message": "Run inference.py for baseline evaluation"}
