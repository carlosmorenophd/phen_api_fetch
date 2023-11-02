import models
from schemas import schemas


def find_by_id(id: int):
    try:
        return models.Location.get_by_id(id)
    except Exception:
        raise ValueError("Location can not found")


def find_by_country_number(number: int, country: str):
    return models.Location.select().where(
        models.Location.number == validate_country_number(
            country=country, number=number),
        models.Location.country == validate_country(country=country),
    ).first()


def create(location: schemas.LocationCreate):
    db_entity = models.Location.filter(
        models.Location.number == validate_country_number(
            country=location.country, number=location.number)
    ).first()
    print("Find {}".format(db_entity))
    if db_entity:
        return db_entity
    db_entity = models.Location(
        number=validate_country_number(
            country=location.country, number=location.number),
        country=validate_country(country=location.country),
        institute_name=location.institute_name,
        cooperator=location.cooperator,
        latitude=location.latitude,
        latitude_degrees=location.latitude_degrees,
        latitude_minutes=location.latitude_minutes,
        longitude=location.longitude,
        longitude_degrees=location.longitude_degrees,
        longitude_minutes=location.longitude_minutes,
        altitude=location.altitude,
    )
    print("Create {}".format(db_entity))
    db_entity.save()
    print("Created {}".format(db_entity))
    return db_entity


def find_by_number(number: int):
    return models.Location.filter(models.Location.number == number).first()


def validate_country(country: str) -> str:
    if rule_to_country(country=country):
        return "None_country"
    else:
        return country


def validate_country_number(country: str, number: int) -> str:
    if rule_to_country(country=country):
        return 2147483647
    else:
        return number

def rule_to_country(country: str) -> bool:
    if country == "" or country == "nan" or country == None or country=="Null":
        return True
    return False