# In-memory conversation store (toy)
CONVERSATIONS = {}

def handle_message(user_id: str, message: str) -> str:
    """
    Very basic logic for now.
    """

    if user_id not in CONVERSATIONS:
        # New conversation
        CONVERSATIONS[user_id] = {
            "turn": 1
        }
        return (
            "Hi! 👋\n"
            "Thanks for reaching out.\n\n"
            "Can you briefly tell me what connectivity you are looking for?"
        )

    # Existing conversation
    CONVERSATIONS[user_id]["turn"] += 1

    return (
        "Thanks! 👍\n"
        "Our team will review your requirement and get back to you shortly."
    )
