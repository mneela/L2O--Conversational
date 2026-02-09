# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Lead Capture Bot conversation orchestrator service built with FastAPI. The service follows a stateless design where conversation state is managed separately from the request-handling layer.

## Architecture

The codebase follows a two-layer architecture:

- **[app.py](app.py)**: FastAPI application entry point. Defines the REST API server but currently lacks endpoint definitions.
- **[orchestrator.py](orchestrator.py)**: Message handling logic. Contains `handle_message()` function that manages conversation state and generates responses.

### State Management

**Current Implementation**: In-memory storage using the `CONVERSATIONS` dictionary in [orchestrator.py](orchestrator.py). This is a toy implementation for development.

**Planned Implementation**: Redis-based persistent storage. Upstash Redis credentials are loaded from environment variables in [app.py](app.py).

### Planned Components (Not Yet Implemented)

According to comments in [app.py](app.py:10-14):
- LLM Client integration
- TMF (TeleManagement Forum) integrations

## Environment Configuration

Configuration is managed via environment variables in a [.env](.env) file:

- `UPSTASH_REDIS_REST_URL`: Redis instance URL
- `UPSTASH_REDIS_REST_TOKEN`: Redis authentication token

**Setup**: Copy [.env.example](.env.example) to `.env` and update with your credentials. The `.env` file is gitignored to prevent credential leakage.

## Running the Application

1. Install dependencies: `pip install -r requirements.txt`
2. Ensure [.env](.env) file exists with required credentials
3. Add API endpoints to [app.py](app.py) that call `handle_message()` from the orchestrator
4. Run with: `uvicorn app:app --reload`

## Key Implementation Details

- **Conversation Flow**: The orchestrator tracks conversation turns per user_id. First message returns a greeting, subsequent messages return an acknowledgment.
- **User Identification**: Conversations are keyed by `user_id` string.
- **Stateless Service**: The FastAPI service itself maintains no state; all conversation history goes through the orchestrator's state store.

