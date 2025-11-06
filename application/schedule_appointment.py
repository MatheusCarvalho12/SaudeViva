from typing import Tuple, Optional
from domain.entities import Appointment
from domain.rules import is_within_working_hours, has_conflict
from infrastructure.json_repository import JsonAppointmentRepository


class ScheduleAppointment:
    
    def __init__(self, repository: JsonAppointmentRepository):
        self.repository = repository
    
    def execute(
        self, 
        patient_name: str, 
        date: str, 
        time: str
    ) -> Tuple[Optional[Appointment], Optional[str]]:
        if not patient_name or not patient_name.strip():
            return None, "Nome do paciente é obrigatório."
        
        if not is_within_working_hours(date, time):
            return None, (
                "Horário inválido. A clínica funciona de segunda a sexta, "
                "das 08:00 às 18:00. Consultas devem terminar até às 18:00."
            )
        
        existing = self.repository.list_all()
        if has_conflict(date, time, existing):
            return None, "Já existe uma consulta agendada neste horário."
        
        appointment = Appointment.create(
            patient_name=patient_name.strip(),
            date=date,
            time=time
        )
        
        self.repository.save(appointment.to_dict())
        
        return appointment, None

