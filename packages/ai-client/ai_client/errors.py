class AIClientError(Exception):
    """Base error for Internal AI Client failures."""


class AIClientHTTPError(AIClientError):
    def __init__(self, status_code: int, message: str, response_body: str = "") -> None:
        super().__init__(f"LiteLLM request failed with HTTP {status_code}: {message}")
        self.status_code = status_code
        self.response_body = response_body


class AIClientJSONError(AIClientError):
    """Raised when a model response cannot be parsed as JSON."""
