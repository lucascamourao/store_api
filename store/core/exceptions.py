class BaseException(Exception):
    message: str = "Internal Server Error"

    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message


class NotFoundException(BaseException):
    message = "Not Found"


# Create: Map an exception in case an insertion error occurs and capture it in the controller
class DuplicateEntryException(BaseException):
    message = "Duplicate Entry"
