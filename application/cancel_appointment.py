from typing import Optional
from infrastructure.json_repository import JsonAppointmentRepository


class CancelAppointment:
    
    def __init__(self, repository: JsonAppointmentRepository):
        self.repository = repository
    
    def execute(self, appointment_id: str) -> Optional[str]:
        appointments = self.repository.list_all()
        found = False
        
        for apt in appointments:
            if apt.get("id") == appointment_id:
                if apt.get("status") == "cancelada":
                    return "Esta consulta já está cancelada."
                apt["status"] = "cancelada"
                found = True
                break
        
        if not found:
            return "Consulta não encontrada."
        
        self.repository.update(appointments)
        return None

