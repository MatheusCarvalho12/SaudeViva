from datetime import datetime

def get_parse_appointment_prompt(text: str) -> str:
    today_str = datetime.now().strftime('%Y-%m-%d')
    current_year = datetime.now().year
    
    return f"""Você é um assistente que extrai informações de agendamento de consultas.
A data de hoje é {today_str}. Se o ano não for especificado no texto do usuário, presuma que é o ano corrente ({current_year}). Se a data mencionada já passou no ano corrente, use o próximo ano.
Analise o texto do usuário e retorne APENAS um JSON com os seguintes campos:
- paciente: nome do paciente
- data: data no formato YYYY-MM-DD
- hora: horário no formato HH:MM

Se não conseguir extrair alguma informação, retorne null para aquele campo.

Texto do usuário: "{text}"

Retorne APENAS o JSON, sem explicações."""


def get_confirmation_message_prompt(patient_name: str, date_formatted: str, time_: str) -> str:
    return f"""Gere uma mensagem de confirmação cordial e profissional para um agendamento de consulta.

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
