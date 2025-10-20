# Chrome AI Agent 

A modular automation system that connects a web interface, a Python LLM agent, and a Chrome Extension to execute natural language tasks directly in your browser.

---

## 💡 What This Project Does

This project lets you type a natural language request (like “ search for AI videos in youtube” or “search for unread emails older than 3 months”) into a **web interface**. Behind the scenes, it:

1. **Receives your request** via a simple web page
2. **Sends it to a Python LLM agent** to generate a step-by-step plan
3. **Passes the plan to a bridge server**, which holds the plan temporarily
4. **A Chrome Extension polls the bridge**, receives the plan, and executes it in your browser using DOM automation

---

## 🧩 Architecture Overview

🖥️ **Web UI**
A minimal frontend interface where users type their task or request.
⚙️ **Agent Server (localhost:8000)**
A FastAPI backend powered by an LLM. It receives the user’s input, generates a structured plan, and dispatches it to the bridge.
🔗 **Bridge Server (localhost:3001)**
A lightweight FastAPI service that stores the latest plan and exposes it via HTTP. Acts as a relay between the agent and the Chrome Extension.
🧩 **Chrome Extension**
Polls the Bridge Server for new plans, then executes them directly in the active webpage. Designed to be modular and browser-agnostic.

---

## 🛠️ Setup Instructions

### 1. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
 ```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add Your API Key
Please create your own .env file in the project root and define your LLM API key:
```bash
LLM_API_KEY= your_own_key_here
```
The environment variable is used in the following file:
```bash
agent_core/agent_runner.py
```
This project uses a language model (LLM) to generate structured plans from natural language input. By default, it integrates with Mistral.
If you're using a different LLM provider (e.g., OpenAI, Anthropic), you can redefine the client logic in agent_runner.py to match your provider’s SDK or HTTP interface. The architecture is modular and easy to adapt.
### 4. Load the Chrome Extension

1. Open Google Chrome
2. Go to chrome://extensions
3. Enable Developer Mode
4. Click “Load unpacked”
5. Select the chrome_extension/ folder from this project

### 4. Run the Servers
In your terminal, split into two panes or tabs:
**Terminal 1 — Start the Agent Server (LLM)**
```bash
cd agent_core
python -m uvicorn app_entry:app --reload --port 8000
```
**Terminal 2 — Start the Bridge Server**
```bash
cd api_bridge
python -m uvicorn bridge:app --reload --port 3001 
```

### 5. Use the Web Interface
Open your browser and go to:
```bash
http://localhost:8000
```
✅ Make sure Google Chrome is open and the Chrome Extension is active. Then, type your request in the input field provided.