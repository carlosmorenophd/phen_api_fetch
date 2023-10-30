from app.schemas import schemas
from app import models


def get_or_create(trial: schemas.TrialCreate):
    db_entity = models.Trial.filter(models.Trial.name == trial.name).first()
    if db_entity:
        return db_entity
    db_entity = models.Trial(name=trial.name)
    db_entity.save()
    return db_entity


def find_by_name(name: str):
    return models.Trial.filter(models.Trial.name == name).first()
