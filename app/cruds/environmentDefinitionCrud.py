from app import models
from app.schemas import schemas


def get_or_create(
    environment_definition: schemas.EnvironmentDefinitionCreate
):
    db_entity = models.EnvironmentDefinition.select().where(
        models.EnvironmentDefinition.name == environment_definition.name,
        models.EnvironmentDefinition.number == environment_definition.number,
    ).first()
    if db_entity:
        return db_entity
    db_save = models.EnvironmentDefinition(
        name=environment_definition.name,
        number=environment_definition.number,
    )
    db_save.save()
    return db_save
