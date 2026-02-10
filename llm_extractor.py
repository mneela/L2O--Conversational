import json

SYSTEM_PROMPT = """
You are an enterprise telecom lead extraction assistant.

Extract structured lead information from the user's message.

Rules:
- Return ONLY valid JSON
- Do NOT guess
- Use null if unknown
- Confidence values must be between 0.0 and 1.0
"""

USER_PROMPT_TEMPLATE = """
User message:
"{message}"

Extract:
- company_name
- intent
- plan_type (5G | Fiber | Dedicated Internet | MPLS)
- urgency (Immediate | Short-term | Long-term)

Respond in this JSON format:
{{
  "company_name": null,
  "intent": null,
  "plan_type": null,
  "urgency": null,
  "confidence": {{
    "company_name": 0.0,
    "intent": 0.0,
    "plan_type": 0.0,
    "urgency": 0.0
  }}
}}
"""
def call_llm(message: str) -> dict:
    """
    TEMPORARY mock. Replace with real LLM call later.
    """
    text = message.lower()

    result = {
        "company_name": None,
        "intent": None,
        "plan_type": None,
        "urgency": None,
        "confidence": {
            "company_name": 0.0,
            "intent": 0.0,
            "plan_type": 0.0,
            "urgency": 0.0
        }
    }

    if "factory" in text or "office" in text or "bank" in text:
        result["intent"] = "Business connectivity"
        result["confidence"]["intent"] = 0.8

    if "dedicated" in text:
        result["plan_type"] = "Dedicated Internet"
        result["confidence"]["plan_type"] = 0.9

    if "urgent" in text or "immediately" in text:
        result["urgency"] = "Immediate"
        result["confidence"]["urgency"] = 0.9

    return result
