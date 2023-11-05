from datetime import datetime


def convert_date_BDY(date_text: str) -> datetime:
    return datetime.strptime(date_text, '%b %d %Y')


def diff_date(date_start: datetime, date_end: datetime) -> int:
    return (date_end - date_start).days
