from abc import ABCMeta, abstractmethod
from typing import List, Any

class IngestModule(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def version() -> str:
        """Return the version of the module."""
        pass

    @staticmethod
    @abstractmethod
    def file_types() -> List[str]:
        """Return a list of supported file types."""
        pass

    @staticmethod
    @abstractmethod
    def output_data_structures() -> List[str]:
        """Return the data structures produced by this module."""
        pass

    @staticmethod
    @abstractmethod
    def ingest(file_path: str) -> Any:
        """Ingest a file and return the data structure."""
        pass