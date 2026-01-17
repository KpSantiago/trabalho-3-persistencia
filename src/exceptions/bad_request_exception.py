from starlette import status

from exceptions.business_exception import BusinessException


class BadRequestException(BusinessException):
    def __init__(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        super().__init__(message, status_code)