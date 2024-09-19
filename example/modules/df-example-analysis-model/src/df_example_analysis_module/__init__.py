import json
from datetime import datetime
from typing import List, Any

from df_modules import AnalysisModule
from pydantic import BaseModel
from gpxpy import gpx


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

class Analysis(AnalysisModule):
    @staticmethod
    def version() -> str:
        """Return the version of the module."""
        return "0.1.0"

    @staticmethod
    def input_data_structures() -> List[str]:
        """Return the data structures that this module can read."""
        return ["csv"]

    @staticmethod
    def output_data_structures() -> List[str]:
        """Return the data structures produced by this module."""
        return ["GPX"]

    @staticmethod
    def analyze(data: CSVIngestYuneec) -> Any:
        """Analyze data and return the resulting data structure."""
        doc = gpx.GPX()
        track = gpx.GPXTrack()
        doc.tracks.append(track)
        segment = gpx.GPXTrackSegment()
        track.segments.append(segment)

        for entry in data.entries:
            time = datetime.strptime(entry.timestamp, "%Y%m%d %H:%M:%S:%f")
            segment.points.append(gpx.GPXTrackPoint(latitude=entry.latitude, longitude=entry.longitude, elevation=entry.altitude, time=time, speed=entry.speed, comment=json.dumps(
                {'accuracy': entry.accuracy, 'angle': entry.angle}
            )))

        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(doc.to_xml())

        return doc.to_xml()
