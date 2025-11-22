class NoteMissingException(Exception):
    """Exception raised when a note cannot be found by its slug."""

    def __init__(self, message):
        super().__init__(message)


class DuplicateSlugDetected(Exception):
    pass
