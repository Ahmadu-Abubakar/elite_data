class BaseProviderException(Exception):
    """Base exception for all provider activities."""
    def __init__(self, message="A provider error occurred.", details=None):
        super().__init__(message)
        self.details = details or {}


# --- Network & Connection Exceptions ---

class ProviderNetworkError(BaseProviderException):
    """Raised when the server cannot be reached (Timeout, DNS, Connection drop)."""
    pass


class ProviderHTTPError(BaseProviderException):
    """Raised when the provider returns a bad HTTP status code (4xx or 5xx)."""
    def __init__(self, message, status_code, response_body=None):
        super().__init__(message, details={"status_code": status_code, "body": response_body})
        self.status_code = status_code
        self.response_body = response_body


# --- Data & Parsing Exceptions ---

class ProviderDataValidationError(BaseProviderException):
    """Raised when the API returns invalid data format or missing required keys."""
    pass


class ProviderAuthenticationError(BaseProviderException):
    """Raised specifically for 401 Unauthorized or 403 Forbidden issues."""
    pass


# --- Business Logic Exceptions ---

class ProviderTransactionFailed(BaseProviderException):
    """Raised when a data/airtime purchase explicitly fails on the supplier end."""
    pass


class ProviderEmptyResponse(BaseProviderException):
    """Raised when the provider returns an empty successful response (e.g., no products found)."""
    pass

class ProviderDataValidationError(BaseProviderException):
    """Raised when Supplier change their language"""
    pass
