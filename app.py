import os
from dotenv import load_dotenv
from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from orchestrator import handle_message

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

