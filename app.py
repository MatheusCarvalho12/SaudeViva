import sys
from datetime import datetime
from openai import APIError

from infrastructure.env_loader import load_environment
from infrastructure.json_repository import JsonAppointmentRepository
from infrastructure.openai_client import OpenAIClient
from application.schedule_appointment import ScheduleAppointment
from application.list_appointments import ListAppointments
from application.cancel_appointment import CancelAppointment
from application.schedule_from_natural import ScheduleFromNatural


def clear_screen():
    print("\n" * 2)


def print_header():
    print("=" * 60)
    print("    CLÍNICA SAUDEVIVA - SISTEMA DE AGENDAMENTO")
    print("    Dr. Carlos - Clínico Geral")
    print("=" * 60)
    print()


def print_menu():
    print("\n--- MENU PRINCIPAL ---")
    print("1. Agendar consulta")
    print("2. Listar consultas")
    print("3. Cancelar consulta")
    print("4. Agendar por linguagem natural")
    print("5. Sair")
    print()


def format_date(date_str: str) -> str:
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d/%m/%Y")
    except ValueError:
        return date_str


def handle_schedule_appointment(
    schedule_uc: ScheduleAppointment,
    openai_client: OpenAIClient
):
    print("\n--- AGENDAR CONSULTA ---")
    
    patient_name = input("Nome do paciente: ").strip()
    if not patient_name:
        print("❌ Nome do paciente é obrigatório.")
        return
    
    date = input("Data (YYYY-MM-DD): ").strip()
    time = input("Horário (HH:MM): ").strip()
    
    appointment, error = schedule_uc.execute(patient_name, date, time)
    
    if error:
        print(f"\n❌ Erro: {error}")
        return
    
    print("\n✅ Consulta agendada com sucesso!")
    print(f"   ID: {appointment.id}")
    
    print("\n📩 Gerando mensagem de confirmação...")
    try:
        message = openai_client.generate_confirmation_message(
            appointment.patient_name,
            appointment.date,
            appointment.time
        )
        print(f"\n{message}")
    except APIError as e:
        print(f"\n⚠️  Não foi possível gerar a mensagem de confirmação: {e}")
        print(f"Consulta agendada para {format_date(date)} às {time}.")


def handle_list_appointments(list_uc: ListAppointments):
    print("\n--- CONSULTAS AGENDADAS ---")
    
    appointments = list_uc.execute()
    
    if not appointments:
        print("\nNenhuma consulta agendada.")
        return
    
    active = [a for a in appointments if a.get("status") == "marcada"]
    cancelled = [a for a in appointments if a.get("status") == "cancelada"]
    
    if active:
        print("\n📅 CONSULTAS ATIVAS:")
        for apt in active:
            print(f"\n  • Paciente: {apt['patient_name']}")
            print(f"    Data: {format_date(apt['date'])} às {apt['time']}")
            print(f"    Duração: {apt.get('duration_minutes', 30)} minutos")
            print(f"    ID: {apt['id']}")
    
    if cancelled:
        print("\n❌ CONSULTAS CANCELADAS:")
        for apt in cancelled:
            print(f"\n  • Paciente: {apt['patient_name']}")
            print(f"    Data: {format_date(apt['date'])} às {apt['time']}")
            print(f"    ID: {apt['id']}")
    
    print(f"\n📊 Total: {len(active)} ativas, {len(cancelled)} canceladas")


def handle_cancel_appointment(cancel_uc: CancelAppointment, list_uc: ListAppointments):
    print("\n--- CANCELAR CONSULTA ---")
    
    appointments = list_uc.execute()
    active = [a for a in appointments if a.get("status") == "marcada"]
    
    if not active:
        print("\nNenhuma consulta ativa para cancelar.")
        return
    
    print("\nConsultas ativas:")
    for i, apt in enumerate(active, 1):
        print(f"\n{i}. Paciente: {apt['patient_name']}")
        print(f"   Data: {format_date(apt['date'])} às {apt['time']}")
        print(f"   ID: {apt['id']}")
    
    print()
    choice = input("Digite o ID da consulta a cancelar (ou 'voltar'): ").strip()
    
    if choice.lower() == 'voltar':
        return
    
    error = cancel_uc.execute(choice)
    
    if error:
        print(f"\n❌ Erro: {error}")
    else:
        print("\n✅ Consulta cancelada com sucesso!")


def handle_schedule_from_natural(
    schedule_natural_uc: ScheduleFromNatural,
    openai_client: OpenAIClient
):
    print("\n--- AGENDAR POR LINGUAGEM NATURAL ---")
    print("Exemplos:")
    print('  - "Quero marcar consulta para João amanhã às 10h"')
    print('  - "Agendar Maria para sexta-feira às 14:30"')
    print('  - "Consulta para Pedro no dia 2025-11-08 às 9h"')
    print()
    
    text = input("Digite seu pedido: ").strip()
    
    if not text:
        print("❌ Pedido vazio.")
        return
    
    print("\n🤖 Interpretando seu pedido...")
    
    appointment, error = schedule_natural_uc.execute(text)
    
    if error:
        print(f"\n❌ Erro: {error}")
        return
    
    print("\n✅ Consulta agendada com sucesso!")
    print(f"   Paciente: {appointment.patient_name}")
    print(f"   Data: {format_date(appointment.date)}")
    print(f"   Horário: {appointment.time}")
    print(f"   ID: {appointment.id}")
    
    print("\n📩 Gerando mensagem de confirmação...")
    try:
        message = openai_client.generate_confirmation_message(
            appointment.patient_name,
            appointment.date,
            appointment.time
        )
        print(f"\n{message}")
    except APIError as e:
        print(f"\n⚠️  Não foi possível gerar a mensagem de confirmação: {e}")


def main():
    load_environment()
    
    try:
        repository = JsonAppointmentRepository("data/consultas.json")
        openai_client = OpenAIClient()
    except ValueError as e:
        print(f"❌ Erro de configuração: {e}")
        print("\nVerifique se o arquivo .env existe e contém OPENAI_API_KEY.")
        sys.exit(1)
    
    schedule_uc = ScheduleAppointment(repository)
    list_uc = ListAppointments(repository)
    cancel_uc = CancelAppointment(repository)
    schedule_natural_uc = ScheduleFromNatural(schedule_uc, openai_client)
    
    print_header()
    
    while True:
        print_menu()
        choice = input("Escolha uma opção: ").strip()
        
        if choice == "1":
            handle_schedule_appointment(schedule_uc, openai_client)
        elif choice == "2":
            handle_list_appointments(list_uc)
        elif choice == "3":
            handle_cancel_appointment(cancel_uc, list_uc)
        elif choice == "4":
            handle_schedule_from_natural(schedule_natural_uc, openai_client)
        elif choice == "5":
            print("\n👋 Até logo!")
            break
        else:
            print("\n❌ Opção inválida. Tente novamente.")
        
        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()

