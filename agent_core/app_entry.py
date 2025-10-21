from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from agent_runner import parse_task
from plan_sender import send_to_bridge

app = FastAPI()

# Full agent flow: parse task → send to Chrome
@app.post("/task")
async def generate_task(request: Request):
    try:
        data = await request.json()
        task = data.get("task", "")
        result = parse_task(task)
        result = await send_to_bridge(result)
        return JSONResponse(content={"status": "success", "plan": result})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

# In-memory plan store
stored_plan = None

# Generate and store plan (without sending to Chrome)
@app.post("/plan")
async def set_plan(request: Request):
    global stored_plan
    data = await request.json()
    task = data.get("task", "")
    stored_plan = parse_task(task)
    return JSONResponse(content={"status": "success", "plan": stored_plan})

# Retrieve stored plan
@app.get("/plan")
async def get_plan():
    return stored_plan or {}

# Clear stored plan
@app.delete("/plan")
async def delete_plan():
    global stored_plan
    stored_plan = None
    return JSONResponse(content={"status": "deleted"})

# Serve static web_ui
app.mount("/", StaticFiles(directory="../web_ui", html=True))
