Flask-ArgExt
============

Introducation
-------------

**Flask-ArgExt** is designed to make it easier to deal with arguments' types through
requests. Validate and convert the types automatically.

Install
-------

Activate your virtualenv, assume your virtualenvs location is ``/srv/virtualenvs``

.. code:: bash

   $ source /srv/virtualenvs/env/bin/activate

and install the extension with the following commands

.. code:: bash

   $ mkdir ~/workspace && cd ~/workspace

   $ git clone git@github.com:streethacker/flask-argext.git

   $ cd flask_argext && make install



Quick Start
===========

Once installed, the **Flask-ArgExt** is easy to use. Import and wrap the function(the
request handler) with ``parse_args``, a decorator which receives a dictionary with
argument name(e.g. ``user_id``) & its coresponding type(a descriptor, e.g. ``IntField``)
pairs

Example
--------

.. code:: python

   # -*- coding: utf-8 -*-

   from .models import (
        DBSession,
        User,
   )

   from flask_argext import (
        parse_args,
   )

   from flask_argext.fields import (
        ListField,
        DateField,
   )

   @app.route('/api/user')
   @parse_args({
       'user_ids': ListField,
       'created_at': DateField,
    })
   def mget(user_ids, created_at):

        if not user_ids:
            return []

        users = DBSession().query(User).\
            filter(User.user_id.in_(user_ids)).\
            filter(User.created_at >= created_at).\
            all()

        return users

Then checkout to the directory which contains the ``runserver.py`` file, and start the
sever

.. code:: bash

   $ python runserver.py

and now you can test your api using **CURL**

.. code:: bash

   $ curl http://localhost:8080/api/user?user_ids=1,2,3,4&created_at=2015-01-01

As a result, ``user_ids`` would be automatically converted to ``[1, 2, 3, 4]``, and
``created_at`` would be ``datetime.datetime(2015, 1, 1, 0, 0)``

Builtin Fields
--------------

A bundle of data types is supported by default, i.e. these data types can be
imported and used directly. Each type is a descriptor, which contains a
``__get__`` and ``__set__`` method to restrict the operations

Complete Type List
^^^^^^^^^^^^^^^^^^

**1. IntField**

    Argument which specified to ``IntField`` would be converted to ``int`` type,
    raise ``ArgError`` if any unexpected error occurred

**2. FloatField**

    Argument which specified to ``FloatField`` would be converted to ``float`` type,
    raise ``ArgError`` if any unexpected error occurred

**3. StringField**

    Argument which specified to ``StringField`` would be converted to ``str`` type,
    raise ``ArgError`` if any unexpected error occurred

    **Caution:** ``str`` in **Python 2.x** is quite different from ``unicode``

**4. ListField**

    Argument which specified to ``ListField`` would be converted to ``list`` type,
    raise ``ArgError`` if any unexpected error occurred

    **Caution:** ``ListField`` could also accept a callable object as its inside
    elements type, e.g. ``int`` or ``str``, default is ``int``

    **Here is an example**

    .. code:: python
        
        @parse_args({
            'user_ids': ListField(inside_fmt=int),
        })
        def mget(user_ids):
            return User.mget(user_ids)

**5. DateField**

    Argument which specified to ``DateField`` would be converted to ``datetime.datetime``
    type, raise ``ArgError`` if any unexpected error occurred

    **Caution:** Considering compatibility, ``DateField`` actually convert the argument
    to the same type as ``DatetimeField``. However, if you send an argument like
    '2015-09-10 12:34:10', the ``ArgError`` would be raised rigidly

**6. DatetimeField**

    Argument which specified to ``DatetimeField`` would be converted to ``datetime.datetime``
    type, raise ``ArgError`` if any unexpected error occurred


Advanced Usage
==============

You can customize your own data types by inherit the ``BaseField`` class, and implement
your own ``__get__`` and ``__set__`` method

Example
-------

.. code:: python

   # -*- coding: utf-8 -*-

   from flask_argext.fields import (
        BaseField,
   )

   from flask_argext.exc import (
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
                    "{}() invalid argument format: {}".format(self._fmt.__name__, self._val)
                )

        def __get__(self, instance, owner=None):
            try:
                return self._fmt(self._val)
            except ArgFormatError:
                raise ArgError(
                    608,
                    "{}() invalid argument format: {}".format(self._fmt.__name__, self._val)
                )

        def __set__(self, instance, val):
            try:
                self._val = self._fmt(val)
            except ArgFormatError:
                raise ArgError(
                    608,
                    "{}() invalid argument format: {}".format(self._fmt.__name__, self._val)
                )

then you can use your own ``UnicodeField`` the same way as default data types

.. code:: python

   # -*- coding: utf-8 -*-

   from .models import (
        User,
   )

   from flask_argext import (
        parse_args,
   )
   
   @parse_args({
       'username': UnicodeField,
    })
   def get(username):
        return User.get_by_name(username)   # username is already unicode
