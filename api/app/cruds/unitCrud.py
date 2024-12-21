from schemas import schemas
import models


def get_or_create(unit: schemas.Unit) -> models.Unit:
    db_entity = models.Unit.select().where(
        models.Unit.name == unit.name
    ).first()
    if db_entity:
        return db_entity
    db_save = models.Unit(
        name=unit.name
    )
    db_save.save()
    return db_save

def find_by_id(id: int) -> models.Unit:
    return models.Unit.get_by_id(id)
