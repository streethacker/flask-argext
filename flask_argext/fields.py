# -*- coding: utf-8 -*-

import logging

from datetime import (
    datetime
)

from abc import (
    ABCMeta,
    abstractmethod,
)

from .exc import (
    ArgFormatError,
    ArgError,
)

from .const import (
    ArgErrorCode,
)


logger = logging.getLogger(__name__)


##################
# 类型定义
##################

class BaseField(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __get__(self, instance, owner=None):
        raise NotImplementedError

    @abstractmethod
    def __set__(self, instance, val):
        raise NotImplementedError


class IntField(BaseField):

    '''
    IntField
    ========

    Doctest
    --------

    >>> class IntegerModel(object):
    ...     field = IntField()
    ...
    >>> m = IntegerModel()
    >>> m.field = '1001'
    >>> isinstance(m.field, int)
    True
    '''

    __format__ = int

    def __init__(self, val=None, fmt=None):
        self._fmt = fmt if callable(fmt) else self.__format__

        try:
            self._val = self._fmt(val) if val is not None else val
        except ArgFormatError:
            raise ArgError(
                ArgErrorCode['ARGUMENT_FORMAT_EXC'],
                "{}() invalid argument format: {}".
                format(self._fmt.__name__, self._val)
            )

    def __get__(self, instance, owner=None):
        try:
            return self._fmt(self._val)
        except ArgFormatError:
            raise ArgError(
                ArgErrorCode['ARGUMENT_FORMAT_EXC'],
                "{}() invalid argument format: {}".
                format(self._fmt.__name__, self._val)
            )

    def __set__(self, instance, val):
        try:
            self._val = self._fmt(val)
        except ArgFormatError:
            raise ArgError(
                ArgErrorCode['ARGUMENT_FORMAT_EXC'],
                "{}() invalid argument format: {}".
                format(self._fmt.__name__, self._val)
            )


class FloatField(BaseField):

    __format__ = float

    def __init__(self, val=None, fmt=None):
        self._fmt = fmt if callable(fmt) else self.__format__

        try:
            self._val = self._fmt(val) if val is not None else val
        except ArgFormatError:
            raise ArgError(
                ArgErrorCode['ARGUMENT_FORMAT_EXC'],
                "{}() invalid argument format: {}".
                format(self._fmt.__name__, self._val)
            )

    def __get__(self, instance, owner=None):
        try:
            return self._fmt(self._val)
        except ArgFormatError:
            raise ArgError(
                ArgErrorCode['ARGUMENT_FORMAT_EXC'],
                "{}() invalid argument format: {}".
                format(self._fmt.__name__, self._val)
            )

    def __set__(self, instance, val):
        try:
            self._val = self._fmt(val)
        except ArgFormatError:
            raise ArgError(
                ArgErrorCode['ARGUMENT_FORMAT_EXC'],
                "{}() invalid argument format: {}".
                format(self._fmt.__name__, self._val)
            )


class StringField(BaseField):

    '''
    StringField
    ===========

    Doctest
    -------

    >>> class StringModel(object):
    ...     field = StringField()
    ...
    >>> m = StringModel()
    >>> m.field = 1000
    >>> isinstance(m.field, str)
    True
    '''

    __format__ = str

    def __init__(self, val=None, fmt=None):
        self._fmt = fmt if callable(fmt) else self.__format__

        try:
            self._val = self._fmt(val) if val is not None else val
        except ArgFormatError:
            raise ArgError(
                ArgErrorCode['ARGUMENT_FORMAT_EXC'],
                "{}() invalid argument format: {}".
                format(self._fmt.__name__, self._val)
            )

    def __get__(self, instance, owner=None):
        try:
            return self._fmt(self._val)
        except ArgFormatError:
            raise ArgError(
                ArgErrorCode['ARGUMENT_FORMAT_EXC'],
                "{}() invalid argument format: {}".
                format(self._fmt.__name__, self._val)
            )

    def __set__(self, instance, val):
        try:
            self._val = self._fmt(val)
        except ArgFormatError:
            raise ArgError(
                ArgErrorCode['ARGUMENT_FORMAT_EXC'],
                "{}() invalid argument format: {}".
                format(self._fmt.__name__, self._val)
            )


class ListField(BaseField):

    '''
    ListField
    =========

    Doctest
    -------

    >>> class ListModel(object):
    ...     field = ListField()
    ...
    >>> m = ListModel()
    >>> m.field = '1,2,3'
    >>> isinstance(m.field, list)
    True
    '''

    __format__ = lambda self, val: val.strip().split(',')

    def __init__(self, val=None, fmt=None, inside_fmt=int):
        self._fmt = fmt if callable(fmt) else self.__format__
        self._val = val
        self._inside_fmt = inside_fmt if callable(inside_fmt) else None

    def __get__(self, instance, owner=None):

        try:
            return_val = \
                self._val if isinstance(self._val, list) else self._fmt(self._val)  # noqa
            if self._inside_fmt:
                return_val = [self._inside_fmt(item) for item in return_val]
            return return_val
        except ArgFormatError:
            raise ArgError(
                ArgErrorCode['ARGUMENT_FORMAT_EXC'],
                "{}() invalid argument format: {}".
                format(self._fmt.__name__, self._val)
            )

    def __set__(self, instance, val):

        try:
            self._val = val if isinstance(val, list) else self._fmt(val)
            if self._inside_fmt:
                self._val = [self._inside_fmt(item) for item in self._val]
        except ArgFormatError:
            raise ArgError(
                ArgErrorCode['ARGUMENT_FORMAT_EXC'],
                "{}() invalid argument format: {}".
                format(self._fmt.__name__, self._val)
            )


class DateField(BaseField):

    '''
    DateField
    =========

    Doctest
    -------

    >>> class DateModel(object):
    ...     field = DateField()
    ...
    >>> m = DateModel()
    >>> m.field = '2015-11-17'
    >>> isinstance(m.field, datetime)
    True
    >>> m.field.strftime('%Y-%m-%d') == '2015-11-17'
    True
    '''

    __format__ = lambda self, val: datetime.strptime(val, '%Y-%m-%d')

    def __init__(self, val=None, fmt=None):
        self._fmt = fmt if callable(fmt) else self.__format__

        try:
            self._val = self._fmt(val) if val is not None else val
        except ArgFormatError:
            raise ArgError(
                ArgErrorCode['ARGUMENT_FORMAT_EXC'],
                "{}() invalid argument format: {}".
                format(self._fmt.__name__, self._val)
            )

    def __get__(self, instance, owner=None):
        try:
            return_val = self._fmt(self._val) \
                if not isinstance(self._val, datetime) else self._val
            return return_val
        except ArgFormatError:
            raise ArgError(
                ArgErrorCode['ARGUMENT_FORMAT_EXC'],
                "{}() invalid argument format: {}".
                format(self._fmt.__name__, self._val)
            )

    def __set__(self, instance, val):
        try:
            self._val = self._fmt(val)
        except ArgFormatError:
            raise ArgError(
                ArgErrorCode['ARGUMENT_FORMAT_EXC'],
                "{}() invalid argument format: {}".
                format(self._fmt.__name__, self._val)
            )


class DatetimeField(DateField):

    '''
    DatetimeField
    =============

    Doctest
    -------

    >>> class DatetimeModel(object):
    ...     field = DatetimeField()
    ...
    >>> m = DatetimeModel()
    >>> m.field = '2015-11-17 18:00:20'
    >>> isinstance(m.field, datetime)
    True
    >>> m.field.strftime('%Y-%m-%d %H:%M:%S') == '2015-11-17 18:00:20'
    True
    '''

    __format__ = lambda self, val: datetime.strptime(val, '%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
