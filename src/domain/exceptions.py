"""Domain-specific exceptions for the Core Web Vitals application."""


class DomainException(Exception):
    """Base exception for domain layer errors."""
    pass


class InvalidURLException(DomainException):
    """Raised when a URL is invalid or malformed."""
    pass


class InvalidDeviceException(DomainException):
    """Raised when device type is not valid."""
    pass


class RepositoryException(DomainException):
    """Base exception for repository operations."""
    pass


class DatabaseConnectionException(RepositoryException):
    """Raised when database connection fails."""
    pass


class DuplicateRecordException(RepositoryException):
    """Raised when attempting to insert a duplicate record."""
    pass
