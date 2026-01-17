from starlette import status


class BusinessException(Exception):
    def __init__(self, message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message,
        self.status_code = status_code
