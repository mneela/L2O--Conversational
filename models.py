# models.py
# Data models for lead capture

from typing import Optional, Dict
from pydantic import BaseModel


class Lead(BaseModel):
    """Lead information extracted from conversation"""
    company_name: Optional[str] = None
    intent: Optional[str] = None
    plan_type: Optional[str] = None   # 5G | Fiber | Dedicated Internet | MPLS
    urgency: Optional[str] = None     # Immediate | Short-term | Long-term

    confidence: Dict[str, float] = {}
    status: str = "INCOMPLETE"         # INCOMPLETE | QUALIFIED


class ConversationState(BaseModel):
    """Complete conversation state for a user"""
    user_id: str
    lead: Lead

    last_question: Optional[str] = None
    turn_count: int = 0
