from app import models
from app.schemas import schemas


def get_or_create(
    field_collection_environment: schemas.FieldCollectionEnvironmentCreate
):
    db_entity = find_by_field(
        environment_definition_id=field_collection_environment.environment_definition_id,
        field_collection_id=field_collection_environment.field_collection_id,
        unit_id=field_collection_environment.unit_id,
        value_data=field_collection_environment.value_data,
    ).first()
    if db_entity:
        return db_entity
    db_field_collection = models.FieldCollection.get_by_id(
        field_collection_environment.field_collection_id
    )
    if not db_field_collection:
        raise ValueError("Field collection is not valid")
    db_environment_definition = models.EnvironmentDefinition.get_by_id(
        field_collection_environment.environment_definition_id
    )
    if not db_environment_definition:
        raise ValueError("Environment definition is not valid")
    db_unit = models.Unit.get_by_id(
        field_collection_environment.unit_id
    )
    if not db_unit:
        raise ValueError("Unit is not valid")
    db_entity = models.FieldCollectionEnvironment(
        value_data=field_collection_environment.value_data,
        unit=db_unit,
        field_collection=db_field_collection,
        environment_definition=db_environment_definition
    )
    db_entity.save()
    return db_entity


def find_by_field(
    environment_definition_id: int,
    field_collection_id: int,
    unit_id: int,
    value_data: int,
):
    return models.FieldCollectionEnvironment.select().join(
        models.FieldCollection
    ).switch(
        models.FieldCollectionEnvironment
    ).join(
        models.EnvironmentDefinition
    ).switch(
        models.FieldCollectionEnvironment
    ).join(
        models.Unit
    ).where(
        models.FieldCollection.id == field_collection_id,
        models.EnvironmentDefinition.id == environment_definition_id,
        models.Unit.id == unit_id,
        models.FieldCollectionEnvironment.value_data == value_data,
    )
