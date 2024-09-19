from abc import ABCMeta, abstractmethod
from typing import List, Any

class AnalysisModule(metaclass=ABCMeta):
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
    def output_data_structures() -> List[str]:
        """Return the data structures produced by this module."""
        pass

    @staticmethod
    @abstractmethod
    def analyze(data: Any) -> Any:
        """Analyze data and return the resulting data structure."""
        pass



