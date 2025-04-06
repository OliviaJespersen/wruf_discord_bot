class CustomError(Exception):
    """Base class for all custom exceptions."""
    pass

class UserInputError(CustomError):
    """Raised when user input is invalid."""
    pass
