from starlette import status

from exceptions.business_exception import BusinessException


class BadRequestException(BusinessException):
    def __int__(self, message):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)