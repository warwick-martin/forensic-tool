from typing import List, Any
import csv

from df_modules.ingest import IngestModule
from pydantic import BaseModel

class CSVIngestEntryYuneec(BaseModel):
    timestamp: str
    longitude: float
    latitude: float
    altitude: float
    accuracy: float
    speed: float
    angle: float

class CSVIngestYuneec(BaseModel):
    entries: List[CSVIngestEntryYuneec]

class Ingest(IngestModule):
    @staticmethod
    def version() -> str:
        """Return the version of the module."""
        return "0.1.0"

    @staticmethod
    def file_types() -> List[str]:
        """Return a list of supported file types."""
        return ["csv"]

    @staticmethod
    def output_data_structures() -> List[str]:
        """Return the data structures produced by this module."""
        return ["csv"]

    @staticmethod
    def ingest(file_path: str) -> CSVIngestYuneec:
        """Ingest a file and return the data structure."""
        with open(file_path, newline='') as csv_file:
            contents = csv.reader(csv_file)
            next(contents)
            entries: List[CSVIngestEntryYuneec] = []
            for row in contents:
                entry = CSVIngestEntryYuneec(
                    timestamp=row[0],
                    longitude=float(row[1]),
                    latitude=float(row[2]),
                    altitude=float(row[3]),
                    accuracy=float(row[4]),
                    speed=float(row[5]),
                    angle=float(row[6]),
                )
                entries.append(entry)
            data: CSVIngestYuneec = CSVIngestYuneec(
                entries=entries
            )
        return data
