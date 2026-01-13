import os
from typing import Optional

DEFAULT_LOCAL_BASE_URL = "http://localhost:1234/v1"

def get_env_key(*names: str) -> Optional[str]:
    """Return the first non-empty environment variable from names."""
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


__all__ = ["get_env_key"]
