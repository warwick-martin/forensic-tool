from datetime import datetime

from pydantic import BaseModel


class ReportData(BaseModel):
    investigator_name: str
    case_number: int
    start_date: datetime
    end_date: datetime
    evidence: str