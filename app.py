import os
from dotenv import load_dotenv
from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from orchestrator import handle_message
from state_store import get_state

# Load environment variables
load_dotenv()

UPSTASH_REDIS_REST_URL = os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_REST_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")


# we are doing this here 
#Conversation Orchestrator Service
#   ├── REST API (FastAPI)
#   ├── State Store (Redis / DB)
#   ├── LLM Client (later)
#   └── TMF Integrations (later)

# building a conversation Orchestrator service
# the Service is stateless
#   State is stored in :
#    - Redis database

app = FastAPI(title=" Lead Capture Bot L2O")


# ============================================================================
# REQUEST MODELS
# ============================================================================

class MessageRequest(BaseModel):
    """Request model for message endpoint"""
    user_id: str
    message: str


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Lead Capture Bot L2O",
        "version": "1.0.0"
    }

@app.get("/debug/state/{user_id}")
def debug_state(user_id: str):
    """Debug endpoint to view conversation state from Redis"""
    state = get_state(user_id)
    if not state:
        return {"message": "No state found"}
    return state.model_dump()


@app.post("/message")
def send_message(payload: MessageRequest):
    """
    Process incoming message from user.

    Args:
        payload: MessageRequest with user_id and message

    Returns:
        Response dict with reply and conversation state
    """
    return handle_message(payload.user_id, payload.message)


@app.post("/test/message")
def test_message(payload: MessageRequest):
    """
    Test endpoint for message processing (same as /message).

    Args:
        payload: MessageRequest with user_id and message

    Returns:
        Response dict with reply and conversation state
    """
    return handle_message(payload.user_id, payload.message)


@app.get("/conversation/{user_id}")
def get_conversation(user_id: str):
    """
    Retrieve current conversation state for a user from Redis.

    Args:
        user_id: Unique identifier for the user

    Returns:
        Conversation state or error if not found
    """
    state = get_state(user_id)

    if not state:
        return {"error": "Conversation not found", "user_id": user_id}

    return {"user_id": user_id, "state": state.model_dump()}