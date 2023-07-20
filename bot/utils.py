from datetime import datetime, timedelta


def generate_ten_days_of_the_week() -> list[str]:
    """Возвращает 10 дней недели с сегодня в формате 'date day'"""
    week = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
    today: int = datetime.weekday(datetime.today().date())
    ten_days: list = week[today:] + week[:today] + week[today:][0:3]
    return list(map(lambda i: f'{datetime.today().date() + timedelta(days=i[0])} {i[1]}', enumerate(ten_days)))
