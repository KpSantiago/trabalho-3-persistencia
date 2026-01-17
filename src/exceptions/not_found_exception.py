from starlette import status

from exceptions.business_exception import BusinessException


class NotFoundException(BusinessException):
    def __init__(self, message, status_code = status.HTTP_404_NOT_FOUND):
        super().__init__(message, status_code)