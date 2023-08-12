from abc import ABC, abstractmethod, abstractproperty
from llvmlite.ir import Type

class Variable(ABC):

    basic_type: Type

    @abstractmethod
    def get_value():
        pass

    @abstractmethod
    def copy_variable():
        pass

    @abstractmethod
    def set_value(value):
        pass
