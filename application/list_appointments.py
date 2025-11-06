from typing import List, Dict
from infrastructure.json_repository import JsonAppointmentRepository


class ListAppointments:
    
    def __init__(self, repository: JsonAppointmentRepository):
        self.repository = repository
    
    def execute(self) -> List[Dict]:
        return self.repository.list_all()

