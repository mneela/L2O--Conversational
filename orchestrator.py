from state_store import get_state, save_state
from models import Lead, ConversationState
from rules import get_missing_fields, QUESTION_TEMPLATES
from llm_extractor import call_llm

def handle_message(user_id: str, message: str):
    # 1️. Load state
    state = get_state(user_id)

    if not state:
        state = ConversationState(
            user_id=user_id,
            lead=Lead(),
            turn_count=0
        )

    state.turn_count += 1

    # 2️. Call LLM extractor
    extracted = call_llm(message)
    print(f"\n{'='*60}")
    print(f"DEBUG: User message: {message}")
    print(f"DEBUG: Extracted data: {extracted}")

    # 3️. Merge extraction into lead (confidence-aware)
    for field, value in extracted.items():
        if field == "confidence":
            print(f"\nDEBUG: Processing confidence field...")
            for k, v in value.items():
                old_conf = state.lead.confidence.get(k, 0)
                if v > old_conf:
                    print(f"  - Updating {k}: {old_conf} -> {v}")
                    state.lead.confidence[k] = v
                else:
                    print(f"  - Keeping {k}: {old_conf} (new: {v})")
        else:
            if value is not None:
                print(f"DEBUG: Setting {field} = {value}")
                setattr(state.lead, field, value)

    print(f"\nDEBUG: Final lead state:")
    print(f"  - intent: {state.lead.intent} (conf: {state.lead.confidence.get('intent', 0.0)})")
    print(f"  - plan_type: {state.lead.plan_type} (conf: {state.lead.confidence.get('plan_type', 0.0)})")
    print(f"  - urgency: {state.lead.urgency} (conf: {state.lead.confidence.get('urgency', 0.0)})")
    print(f"  - status: {state.lead.status}")

    # 4️. Decide next action
    missing = get_missing_fields(state.lead)
    print(f"\nDEBUG: Missing fields: {missing}")

    if not missing:
        state.lead.status = "QUALIFIED"
        print(f"\nDEBUG: ✓ Lead QUALIFIED!")
        save_state(state)   #  SAVE STATE
        print(f"{'='*60}\n")
        return {
            "reply": "Thanks! Our team will contact you shortly.",
            "state": state.model_dump()
        }

    next_field = missing[0]
    state.last_question = next_field
    print(f"\nDEBUG: ✗ Lead INCOMPLETE - asking for: {next_field}")
    print(f"{'='*60}\n")

    save_state(state)       # SAVE STATE

    return {
        "reply": QUESTION_TEMPLATES[next_field],
        "state": state.model_dump()
    }
