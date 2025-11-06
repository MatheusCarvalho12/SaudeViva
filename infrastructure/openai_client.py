import json
from typing import Optional, Dict
from openai import OpenAI
from infrastructure.env_loader import get_openai_api_key


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
            prompt = f"""Você é um assistente que extrai informações de agendamento de consultas.
Analise o texto do usuário e retorne APENAS um JSON com os seguintes campos:
- paciente: nome do paciente
- data: data no formato YYYY-MM-DD (se for "amanhã", "hoje", etc., calcule a data)
- hora: horário no formato HH:MM

Se não conseguir extrair alguma informação, retorne null para aquele campo.

Texto do usuário: "{text}"

Retorne APENAS o JSON, sem explicações."""

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
            
        except Exception as e:
            print(f"Erro ao interpretar linguagem natural: {e}")
            return None
    
    def generate_confirmation_message(
        self, 
        patient_name: str, 
        date: str, 
        time_: str
    ) -> str:
        try:
            from datetime import datetime
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            date_formatted = date_obj.strftime("%d/%m/%Y")
            
            prompt = f"""Gere uma mensagem de confirmação cordial e profissional para um agendamento de consulta.

Informações:
- Paciente: {patient_name}
- Data: {date_formatted}
- Horário: {time_}
- Médico: Dr. Carlos
- Especialidade: Clínico Geral

A mensagem deve:
- Ser amigável e profissional
- Mencionar o nome do paciente
- Incluir data e horário
- Mencionar o Dr. Carlos
- Pedir para chegar com 10 minutos de antecedência
- Ser breve (2-3 frases)

Retorne APENAS a mensagem, sem aspas ou formatação extra."""

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
            
        except Exception as e:
            from datetime import datetime
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            date_formatted = date_obj.strftime("%d/%m/%Y")
            
            return (
                f"Olá {patient_name}! Sua consulta com o Dr. Carlos (Clínico Geral) "
                f"está confirmada para {date_formatted} às {time_}. "
                f"Por favor, chegue com 10 minutos de antecedência."
            )

