from datetime import datetime


def convert_date_BDY(date_text: str) -> datetime:
    return datetime.strptime(date_text, '%b %d %Y')


def diff_date(date_start: datetime, date_end: datetime) -> int:
    return (date_end - date_start).days


def transform_to_basic_debug(head: str, start_date: datetime,  value: str, debug: bool = False) -> str:
    result = transform_to_basic(head=head, start_date=start_date,  value=value)
    if debug:
        return "{} | {}".format(result, value)
    else:
        return result


def transform_to_basic(head: str, start_date: datetime,  value: str) -> str:
    if value:
        if head.find("(date)") > 0:
            if head == 'EMERGENCE_DATE:(date)':
                return "1"
            else:
                return (diff_date(start_date, convert_date_BDY(
                    value)))
        elif head.find("(Y/N)") > 0:
            if value == "YES":
                return "1"
            else:
                return "0"
        elif head.find("(N/T/S/M/V)") > 0:
            if value[0] == "N":
                return "0"
            elif value[0] == "T":
                return "0.25"
            elif value[0] == "S":
                return "0.50"
            elif value[0] == "M":
                return "0.75"
            elif value[0] == "V":
                return "1"
        elif head.find("(S/N/D)") > 0:
            if value[0] == "S":
                return "0"
            elif value[0] == "N":
                return "0.5"
            elif value[0] == "D":
                return "1"
        elif head.find("(E/N/L)") > 0:
            if value[0] == "E":
                return "0"
            elif value[0] == "N":
                return "0.5"
            elif value[0] == "L":
                return "1"
        else:
            return value

    else:
        return ""
