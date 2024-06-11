from abc import ABCMeta, abstractmethod
from typing import Any


class GenericUseCaseInterface(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError("This suppose to be an abstract function !")

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        raise NotImplementedError("This suppose to be an abstract function !")
