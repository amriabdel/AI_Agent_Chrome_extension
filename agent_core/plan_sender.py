import requests
from agent_utils import log_info, log_error

BRIDGE_PLAN_ENDPOINT = "http://localhost:3001/plan"

# URL of the bridge server that relays plans to the Chrome Extension
async def send_to_bridge(parsed_plan: dict):
    log_info(f"Sending plan to bridge: {parsed_plan}")
    try:
        response = requests.post(BRIDGE_PLAN_ENDPOINT, json=parsed_plan)
        log_info(f"bridge response: {response.status_code}")
        return response.json()
    except Exception as e:
        log_error(f"bridge communication failed: {e}")
        return {"error": str(e)}
