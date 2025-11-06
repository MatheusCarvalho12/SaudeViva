import json
from typing import Optional, Dict
from openai import OpenAI, APIError
from datetime import datetime
from infrastructure.env_loader import get_openai_api_key
from domain.prompts import get_parse_appointment_prompt, get_confirmation_message_prompt


class OpenAIClient:
    
    def __init__(self):
        api_key = get_openai_api_key()
        if not api_key:
            raise ValueError(
                "Chave da OpenAI não encontrada. "
                "Configure OPENAI_API_KEY no arquivo .env"
            )
        self.client = OpenAI(api_key=api_key)
    
    def parse_appointment(self, text: str) -> Optional[Dict]:
        try:
            prompt = get_parse_appointment_prompt(text)

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente que retorna apenas JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            data = json.loads(content)
            
            if not data.get("paciente") or not data.get("data") or not data.get("hora"):
                return None
            
            return data
            
        except (APIError, json.JSONDecodeError) as e:
            print(f"Erro ao interpretar linguagem natural: {e}")
            return None
    
    def generate_confirmation_message(
        self, 
        patient_name: str, 
        date: str, 
        time_: str
    ) -> str:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            date_formatted = date_obj.strftime("%d/%m/%Y")
            
            prompt = get_confirmation_message_prompt(
                patient_name, date_formatted, time_
            )

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente amigável de uma clínica médica."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            message = response.choices[0].message.content.strip()
            message = message.strip('"').strip("'")
            return message
            
        except APIError:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            date_formatted = date_obj.strftime("%d/%m/%Y")
            
            return (
                f"Olá {patient_name}! Sua consulta com o Dr. Carlos (Clínico Geral) "
                f"está confirmada para {date_formatted} às {time_}. "
                f"Por favor, chegue com 10 minutos de antecedência."
            )

