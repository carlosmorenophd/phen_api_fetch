from app import models
from app.schemas import schemas


def get_or_create(web_file: schemas.WebFileCreate) -> models.WebFile:
    db_entity = models.WebFile.select().where(
        models.WebFile.name == web_file.name
    ).first()
    if db_entity:
        return db_entity
    db_entity = models.WebFile(name=web_file.name)
    db_entity.save()
    return db_entity


def get_by_id(id: int):
    return models.WebFile.get_by_id(id)
