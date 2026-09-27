class SynchronizationError(Exception):
    def __init__(self, message="Synchronization Failed", details=None):
        super().__init__(message)
        self.details = details or ""

class ApplyChangesError(SynchronizationError):
    """Raised  when applying changes failed"""
    def __init__(message, details="applying changes failed to complete"):
        super().__init__(message, details)
        pass


class RetryAttemptsException(SynchronizationError):
    """Raised when retries attempts over"""
    pass