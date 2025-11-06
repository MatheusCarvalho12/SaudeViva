from datetime import datetime, timedelta


CLINIC_OPEN_HOUR = 8
CLINIC_CLOSE_HOUR = 18
DEFAULT_DURATION_MINUTES = 30


def is_weekday(date_str: str) -> bool:
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.weekday() < 5
    except ValueError:
        return False


def is_within_working_hours(date_str: str, time_str: str) -> bool:
    if not is_weekday(date_str):
        return False
    
    try:
        time_obj = datetime.strptime(time_str, "%H:%M")
        hour = time_obj.hour
        minute = time_obj.minute
        
        if hour < CLINIC_OPEN_HOUR:
            return False
        if hour >= CLINIC_CLOSE_HOUR:
            return False
        
        if hour == CLINIC_CLOSE_HOUR - 1 and minute > 30:
            return False
        
        return True
    except ValueError:
        return False


def has_conflict(new_date: str, new_time: str, existing_appointments: list) -> bool:
    try:
        new_datetime_str = f"{new_date} {new_time}"
        new_start = datetime.strptime(new_datetime_str, "%Y-%m-%d %H:%M")
        new_end = new_start + timedelta(minutes=DEFAULT_DURATION_MINUTES)
        
        for apt in existing_appointments:
            if apt.get("status") == "cancelada":
                continue
            
            if apt.get("date") != new_date:
                continue
            
            existing_datetime_str = f"{apt['date']} {apt['time']}"
            existing_start = datetime.strptime(existing_datetime_str, "%Y-%m-%d %H:%M")
            existing_duration = apt.get("duration_minutes", DEFAULT_DURATION_MINUTES)
            existing_end = existing_start + timedelta(minutes=existing_duration)
            
            if (new_start < existing_end and new_end > existing_start):
                return True
        
        return False
    except (ValueError, KeyError):
        return True

