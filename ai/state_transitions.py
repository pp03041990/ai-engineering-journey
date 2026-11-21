ALLOWED_TRANSITIONS = {
    "NEW": {"IN_PROGRESS"},
    "IN_PROGRESS": {"COMPLETED", "FAILED"},
    "COMPLETED": set(),
    "FAILED": set(),
}

def transition_state(state, new_status: str):
    allowed = ALLOWED_TRANSITIONS[state.status]

    if new_status not in allowed:
        raise ValueError(
            f"Invalid transition: {state.status} -> {new_status}"
        )

    state.status = new_status