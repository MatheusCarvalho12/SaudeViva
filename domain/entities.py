from dataclasses import dataclass, asdict
import uuid


@dataclass
class Appointment:
    id: str
    patient_name: str
    date: str
    time: str
    duration_minutes: int = 30
    status: str = "marcada"
    
    @staticmethod
    def create(patient_name: str, date: str, time: str, duration_minutes: int = 30) -> "Appointment":
        return Appointment(
            id=str(uuid.uuid4()),
            patient_name=patient_name,
            date=date,
            time=time,
            duration_minutes=duration_minutes,
            status="marcada"
        )
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @staticmethod
    def from_dict(data: dict) -> "Appointment":
        return Appointment(**data)

