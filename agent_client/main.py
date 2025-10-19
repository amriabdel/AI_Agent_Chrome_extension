from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from agent import parse_task
from chrome_bridge import send_to_chrome
from utils import log_info, log_error

app = FastAPI()

class TaskRequest(BaseModel):
    task: str

@app.post("/task")
async def generate_task(request: Request):
    try:
        data = await request.json()
        task = data.get("task", "")
        result = parse_task(task)
        result = await send_to_chrome(result)
        return JSONResponse(content={"status": "success", "plan": result})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
    
stored_plan = None

@app.post("/plan")
async def set_plan(request: Request):
    global stored_plan
    data = await request.json()
    task = data.get("task", "")
    stored_plan = parse_task(task)
    return JSONResponse(content={"status": "success", "plan": stored_plan})

@app.get("/plan")
async def get_plan():
    return stored_plan or {}

@app.delete("/plan")
async def delete_plan():
    global stored_plan
    stored_plan = None
    return JSONResponse(content={"status": "deleted"})

from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="../frontend", html=True))
