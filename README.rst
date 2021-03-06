.. image:: http://ludibriar.appspot.com/logo.png

Author
------

    * Gustavo Rezende <nsigustavo@gmail.com>

Contributors
------------

    * Diego Pinheiro <me@dmpinheiro.net>
    * Hugo Lopes <hltbra@gmail.com>
    * Rodrigo Manhães <rmanhaes@gmail.com>



Development
-----------

Ludibrio's development may be viewed and followed on github::

    http://github.com/nsigustavo/ludibrio

Retrieve the source code using 'git'::

    git clone git://github.com/nsigustavo/ludibrio.git

Install package in 'development mode' and run tests with doctestcommand::

    $ sudo easy_install doctestcommand
    $ git clone git://github.com/nsigustavo/ludibrio.git
    $ cd ludibrio
    $ sudo python setup.py develop
    $ cd ludibrio
    $ doctest


In a nutshell
=============


Install
-------

Install package with easy_install or pip::

    $ sudo easy_install ludibrio


Mock
----

Mocks are objects pre-programmed with expectations which form a specification of the calls they are expected to receive.

A Mocker or Stub instance uses the 'with' statement to record and replay expectations::

    >>> from ludibrio import Mock

    >>> with Mock() as MySQLdb:
    ...     con = MySQLdb.connect('servidor', ' usuario', 'senha')
    ...     con.select_db('banco de dados') >> None
    ...     cursor = con.cursor()
    ...     cursor.execute('ALGUM SQL') >> None
    ...     cursor.fetchall() >> [1,2,3,4,5]

    >>> con = MySQLdb.connect('servidor', ' usuario', 'senha')
    >>> con.select_db('banco de dados')
    >>> cursor = con.cursor()
    >>> cursor.execute('ALGUM SQL')
    >>> cursor.fetchall()
    [1, 2, 3, 4, 5]
    
    >>> MySQLdb.validate() #passed


Stub
----

Stubs provide pre-defined answers to method calls made during a test::

    >>> from ludibrio import Stub

    >>> with Stub() as x:
    ...     x.anything() >> 'response'

    >>> x.anything()
    'response'


Trivial mocking or stubing for any external module
--------------------------------------------------

Ludibrio also offers a replace mode, which basically means if a "from ... import ..." statement is defined into a 'with' scope, the replay mechanism will return a mock object to replace the original object in namespace of the whole Python interpreter (including any modules, etc). There's a simple example below to illustrate how use it::

    >>> from ludibrio import Stub

    >>> with Stub() as time:
    ...     from time import time
    ...     time() >> 171

    >>> from time import time

    >>> time()
    171



Proxy
-----

Two Ludibrio's powerful features that aren't found in other mocking systems is the ability of proxying existing objects, or patching a real instance or class.

When an object is proxied, Ludibrio create a Test Double object holding a reference to the real object, allowing expressions passthrough to it(mocked or not, and by default or on request)::

    >>> from os.path import splitext

    >>> with Stub(proxy=splitext) as splitext:
    ...     splitext('ludibrio/stubed.py') >> ('/temp/temp','.temp')

    >>> splitext('mock.py')
    ('mock', '.py')

    >>> splitext('ludibrio/stubed.py')
    ('/temp/temp', '.temp')



