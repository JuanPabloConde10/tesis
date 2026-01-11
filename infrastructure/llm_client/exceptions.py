class LLMClientError(Exception):
    """Base exception for LLM client errors."""
    status_code: int = 500


class LLMQuotaExceededError(LLMClientError):
    """Raised when a provider returns a quota / rate-limit error (HTTP 429)."""
    status_code = 429
class MissingAPIKeyError(RuntimeError):
    pass

__all__ = ["MissingAPIKeyError"]
