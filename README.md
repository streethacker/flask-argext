## Flask-ArgExt ##

### Installation ###
--------------------

Activate your virtualenv, and install the extension with the following commands:

> mkdir ~/workspace && cd ~/workspace

> git clone git@github.com:streethacker/flask\_argext.git

> cd flask\_argext && make install


### Usage ###
--------------

Once installed, the __Flask-ArgExt__ is easy to use. Simply wrapped the function with
`parse_args` decorator, and specify type of arguments one by one.

#### Example ####
------------------

```
from .model import (
    User,
)

from flask_argext import (
    parse_args,
    ArgError,
    IntField,
)


@app.route('/api/user')
@parse_args({
    'user_id': IntField,
})
def get(user_id):
    # user_id is already an integer
    return User.get(user_id)
```


### Advanced Usage ###
----------------------

Until now, the following data types are supported:

* IntField

* FloatField

* StringField

* ListField

* DateField

* DatetimeField

Any one can customize their own data types by inherit the `BaseField` class, and
implement their own `__get__` and `__set__` method.

#### Example ####
-----------------

```
from flask_argext import (
    BaseField,
    ArgFormatError,
    ArgError,
)


class UnicodeField(BaseField):

    __format__ = unicode

    def __init__(self, val=None, fmt=None):
        self._fmt = fmt if callable(fmt) else self.__format__

        try:
            self._val = self._fmt(val) if val is not None else val
        except ArgFormatError:
            raise ArgError(
                608,
                "{}() invalid argument format: {}".
                format(self._fmt.__name__, self._val)
            )

    def __get__(self, instance, owner=None):
        try:
            return self._fmt(self._val)
        except ArgFormatError:
            raise ArgError(
                608,
                "{}() invalid argument format: {}".
                format(self._fmt.__name__, self._val)
            )

    def __set__(self, instance, val):
        try:
            self._val = self._fmt(val)
        except ArgFormatError:
            raise ArgError(
                608,
                "{}() invalid argument format: {}".
                format(self._fmt.__name__, self._val)
            )

```

then you can use your own `UnicodeField` as default data types:

```
@parse_args({
    'name': UnicodeField,
})
def get(name):
    # name is already unicode string
    return User.get_by_name(name)
```
