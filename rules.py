# rules.py
# Business rules for lead qualification

from models import Lead

MANDATORY_FIELDS = ["intent", "plan_type", "urgency"]
CONFIDENCE_THRESHOLD = 0.6

QUESTION_TEMPLATES = {
    "intent": "What kind of connectivity are you looking for?",
    "plan_type": "Are you looking for 5G, Fiber, or Dedicated Internet?",
    "urgency": "When do you need this connection? (Immediately / Soon / Later)",
    "company_name": "May I know your company name?"
}


def get_missing_fields(lead: Lead):
    """Identify which mandatory fields are missing or have low confidence"""
    missing = []
    for field in MANDATORY_FIELDS:
        value = getattr(lead, field)
        confidence = lead.confidence.get(field, 0.0)

        if value is None or confidence < CONFIDENCE_THRESHOLD:
            missing.append(field)
    return missing
