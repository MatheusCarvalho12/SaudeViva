from typing import Tuple, Optional
from domain.entities import Appointment
from application.schedule_appointment import ScheduleAppointment
from infrastructure.openai_client import OpenAIClient


class ScheduleFromNatural:
    
    def __init__(
        self, 
        schedule_use_case: ScheduleAppointment,
        openai_client: OpenAIClient
    ):
        self.schedule_use_case = schedule_use_case
        self.openai_client = openai_client
    
    def execute(self, natural_text: str) -> Tuple[Optional[Appointment], Optional[str]]:
        parsed = self.openai_client.parse_appointment(natural_text)
        
        if not parsed:
            return None, (
                "Não consegui entender o pedido. "
                "Por favor, informe o nome do paciente, data e horário."
            )
        
        patient_name = parsed.get("paciente")
        date = parsed.get("data")
        time = parsed.get("hora")
        
        if not patient_name or not date or not time:
            return None, (
                "Não consegui extrair todas as informações necessárias. "
                "Por favor, informe o nome do paciente, data e horário."
            )
        
        return self.schedule_use_case.execute(patient_name, date, time)

