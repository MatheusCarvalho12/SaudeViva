import json
import os
from typing import List, Dict, Optional


class JsonAppointmentRepository:
    
    def __init__(self, filepath: str = "data/consultas.json"):
        self.filepath = filepath
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def list_all(self) -> List[Dict]:
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save(self, appointment_dict: Dict):
        appointments = self.list_all()
        appointments.append(appointment_dict)
        self._write_all(appointments)
    
    def update(self, appointments: List[Dict]):
        self._write_all(appointments)
    
    def find_by_id(self, appointment_id: str) -> Optional[Dict]:
        appointments = self.list_all()
        for apt in appointments:
            if apt.get("id") == appointment_id:
                return apt
        return None
    
    def _write_all(self, appointments: List[Dict]):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(appointments, f, ensure_ascii=False, indent=2)

