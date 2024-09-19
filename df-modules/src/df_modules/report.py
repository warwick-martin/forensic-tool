from abc import ABCMeta, abstractmethod
from typing import List, Any

class ReportModule(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def version() -> str:
        """Return the version of the module."""
        pass

    @staticmethod
    @abstractmethod
    def input_data_structures() -> List[str]:
        """Return the data structures that this module can read."""
        pass

    @staticmethod
    @abstractmethod
    def report(data: Any) -> str:
        """Generate a report from the data and return it as a string."""
        pass
