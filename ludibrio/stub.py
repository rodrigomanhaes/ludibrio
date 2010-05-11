#-*- coding:utf-8 -*-

from inspect import getframeinfo
from sys import _getframe as getframe
from _testdouble import _TestDouble

STOPRECORD = False
RECORDING = True

class Stub(_TestDouble):
    """Stubs provides canned answers to calls made during the test.
    """
    __expectation__= [] # [(attribute, args, kargs),]
    __recording__ = RECORDING
    __lastPropertyCalled__ = None

    def __enter__(self):
        self.__expectation__= []
        self.__recording__ = RECORDING
        return self

    def __methodCalled__(self, *args, **kargs):
        property =  self.__lastPropertyCalled__ or getframeinfo(getframe(1))[2]#nome da funcao chamada
        # property == __call__ or alias
        self.__lastPropertyCalled__ = None
        return self.__propertyCalled(property, args, kargs)

    def __propertyCalled(self, property, args=[], kargs={}, retorno=None):
        if self.__recording__:
            self.__newExpectation([property, args, kargs, retorno])
            return self
        else:
            return self._expectationValue(property, args, kargs)

    def __exit__(self, type, value, traceback):
        self.__recording__ = STOPRECORD

    def __setattr__(self, attr, value):
        if attr in dir(Stub):
            object.__setattr__(self, attr, value)
        else:
            self.__propertyCalled('__setattr__', args=[attr, value])

    def __newExpectation(self, attr):
        self.__expectation__.append(attr)

    def __rshift__(self, retorno):
            self.__expectation__[-1][3] = retorno
    __lshift__ = __rshift__

    def _expectationValue(self, attr, args=[], kargs={}):
        for position, (attrEsp, argsEsp, kargsEsp, retorno) in enumerate(self.__expectation__):
            if (attrEsp, argsEsp, kargsEsp) == (attr, args, kargs):
                self.__toTheEnd__(position)
                return retorno
        raise AttributeError("Stub Object received unexpected call")

    def __toTheEnd__(self, position):
        self.__expectation__.append(self.__expectation__.pop(position))

    def __getattr__(self, x):
        self.__lastPropertyCalled__ = x
        return self.__propertyCalled('__getattribute__', (x,), retorno=self)