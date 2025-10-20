from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Enable CORS so the Chrome Extension can access this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to your extension ID
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for the latest plan
stored_plan = None  

# Receive a plan from the agent
@app.post("/plan")
async def receive_plan(request: Request):
    global stored_plan
    stored_plan = await request.json()
    print("Received plan:", stored_plan)
    return JSONResponse(content={"status": "success"})

# Serve the stored plan to the Chrome Extension
@app.get("/plan")
def send_plan():
    return stored_plan or {"status": "no plan yet"}

# Clear the stored plan
@app.delete("/plan")
def clear_plan():
    global stored_plan
    stored_plan = None
    print("🧹 Cleared plan")
    return JSONResponse(content={"status": "deleted"})
