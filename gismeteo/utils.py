from datetime import date


# deprecated
def ten_weekdays_with_today() -> list[str]:
    """Возвращает 10 дней недели от сегодняшнего дня"""
    days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
    today = date.today().weekday()
    days_starting_today: list[str] = days[today:] + days[:today]
    ten_days_with_today = days_starting_today + days_starting_today[:3]
    return ten_days_with_today
