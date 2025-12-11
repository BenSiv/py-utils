from typing import Any

def is_empty(source: Any) -> bool:
    """Checks if a source is empty."""
    if source is None:
        return True
    if isinstance(source, (str, list, dict, tuple)):
        return len(source) == 0
    return False
