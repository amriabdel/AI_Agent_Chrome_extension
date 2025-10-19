from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Allow Chrome Extension to access this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to your extension ID
    allow_methods=["*"],
    allow_headers=["*"],
)

latest_plan = None  

@app.post("/plan")
async def receive_plan(request: Request):
    global latest_plan
    latest_plan = await request.json()
    print("📦 Received plan:", latest_plan)
    return JSONResponse(content={"status": "success"})

@app.get("/plan")
def send_plan():
    return latest_plan or {"status": "no plan yet"}


@app.delete("/plan")
def clear_plan():
    global latest_plan
    latest_plan = None
    print("🧹 Cleared plan")
    return JSONResponse(content={"status": "deleted"})
