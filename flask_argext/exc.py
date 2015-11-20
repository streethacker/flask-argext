# -*- coding: utf-8 -*-

__all__ = ['ArgError']


from httplib import (
    OK,
)


ArgFormatError = (
    TypeError,
    ValueError,
)


class ArgError(Exception):
    status_code = OK

    def __init__(self, error_code, error_msg, status_code=None):
        super(ArgError, self).__init__(error_msg)
        self.error_code = error_code
        self.error_msg = error_msg

        if status_code is not None:
            self.status_code = status_code
