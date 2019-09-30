from abc import ABCMeta, abstractmethod


class ResourceDriverInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def initialize(self, context):
        pass

    @abstractmethod
    def cleanup(self):
        pass
