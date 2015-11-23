# -*- coding: utf-8 -*-

__all__ = ['ArgExt', 'parse_args']


import inspect
import logging

from functools import (
    wraps,
)

from collections import (
    OrderedDict,
)

from flask import (
    request as flask_req,
)

from .exc import (
    ArgError,
)

from .const import (
    ArgErrorCode,
)


logger = logging.getLogger(__name__)


##################
# 参数处理器
##################

class ArgMeta(object):

    __args__ = None
    __defaults__ = None

    def __init__(self, func_name, **kwargs):

        # 请求中有必传参数未找到
        essential_args = set(self.__args__) - set(self.__defaults__)

        if not essential_args.issubset(set(kwargs)):
            raise ArgError(
                ArgErrorCode['ARGUMENT_MISSING_EXC'],
                '{}() required argument not found: {}'.
                format(func_name, list(essential_args - set(kwargs)))
            )

        # 必传参数传值
        for sn, key in enumerate(essential_args):
            setattr(self, key, kwargs[key])

        # 若指定可选参数
        for sn, key in enumerate(self.__defaults__):
            val = kwargs.get(key, None)
            if val:
                setattr(self, key, val)

    @property
    def args(self):
        return [getattr(self, arg) for arg in self.__args__]

    @classmethod
    def _make(cls, argkeys, validators, default_args={}):
        cls.__args__ = argkeys or []
        cls.__defaults__ = default_args.keys() or []

        for key in cls.__args__:
            validator = validators.get(key)
            if not validator:
                setattr(cls, key, default_args.get(key))
                continue

            setattr(cls, key, validator(default_args.get(key)))


##################
# 过滤器封装
##################

parser_factory = lambda name, bases, dct: type(name, bases, dct)


class ArgExt(object):

    def __init__(self, validators={}):
        self._validators = validators

    def __call__(self, func):

        # 获取方法参数列表

        ArgSpec = inspect.getargspec(func)
        argkeys = ArgSpec.args[:]
        defaults = ArgSpec.defaults or []

        default_args = zip(ArgSpec.args[-len(defaults):], defaults[:])
        default_args = OrderedDict(default_args)

        # 创建ArgParser参数分析器

        ArgParser = parser_factory('ArgParser', (ArgMeta,), {})
        ArgParser._make(argkeys, self._validators, default_args)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 载入参数
            self.load_args()
            parser = ArgParser(func.__name__, **self._args_req)
            return func(*parser.args)

        return wrapper

    def load_args(self):
        args = flask_req.get_json(force=False, silent=True, cache=True)
        self._args_req = args or {}

        for key, val in flask_req.values.iteritems():
            self._args_req[key] = val[0] if isinstance(val, list) else val

        self._args_req.update(flask_req.view_args)


parse_args = ArgExt


if __name__ == '__main__':
    import doctest
    doctest.testmod()
