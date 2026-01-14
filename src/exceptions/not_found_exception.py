from starlette import status

from exceptions.business_exception import BusinessException


class NotFoundException(BusinessException):
    def __int__(self, message):
        super().__init__(self.message, status.HTTP_404_NOT_FOUND)