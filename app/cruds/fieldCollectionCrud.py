from app import models
from app.schemas import schemas


def get_or_create(
    field_collection: schemas.FieldCollectionCreate
):
    db_location = models.Location.get_by_id(
        field_collection.location_id
    )
    if not db_location:
        raise ValueError("Location is not valid")
    db_trial = models.Trial.get_by_id(
        field_collection.trial_id
    )
    if not db_trial:
        raise ValueError("Trial is not valid")
    db_web = models.WebFile.get_by_id(
        field_collection.web_file_id
    )
    if not db_web:
        raise ValueError("Web file is not valid")
    return get_or_create_object(
        field_collection=models.FieldCollection(
            agricultural_cycle=field_collection.agricultural_cycle,
            description=field_collection.description,
            location=db_location,
            occurrence=field_collection.occurrence,
            trial=db_trial,
            web_file=db_web,
        )
    )


def get_or_create_object(field_collection: models.FieldCollection):
    db_entity = find_by_raw(
        occurrence=field_collection.occurrence,
        description=field_collection.description,
        agricultural_cycle=field_collection.agricultural_cycle,
        web_file=field_collection.web_file,
        trial=field_collection.trial,
        location=field_collection.location,
    ).first()
    if db_entity:
        return db_entity
    field_collection.save()
    return field_collection


def get_by_raw(
    occurrence: int,
    description: str,
    agricultural_cycle: str,
    web_file: models.WebFile,
    trial: models.Trial,
    location: models.Location,
):
    db_entity = find_by_raw(
        occurrence=occurrence,
        description=description,
        agricultural_cycle=agricultural_cycle,
        web_file=web_file,
        trial=trial,
        location=location,
    )
    if not db_entity:
        raise ValueError(
            "Can't found field collection {}, {}, {}, {}, {}, {}".format(
                occurrence,
                agricultural_cycle,
                web_file.id,
                description,
                trial.id,
                location.id,
            ))
    return db_entity.first()


def find_by_raw(
    occurrence: int,
    description: str,
    agricultural_cycle: str,
    web_file: models.WebFile,
    trial: models.Trial,
    location: models.Location,
):
    return models.FieldCollection.select().join(
        models.WebFile
    ).switch(
        models.FieldCollection
    ).join(
        models.Trial
    ).switch(
        models.FieldCollection
    ).join(
        models.Location
    ).where(
        models.FieldCollection.occurrence == occurrence,
        models.FieldCollection.agricultural_cycle == agricultural_cycle,
        models.FieldCollection.description == description,
        models.WebFile.id == web_file.id,
        models.Trial.id == trial.id,
        models.Location.id == location.id,
    )


def find_by_raw_optional(
    occurrence: int = 0,
    description: str = "",
    agricultural_cycle: str = "",
    genotype_ids: list[int] = []
):
    result = models.FieldCollection.select().distinct().join(
        models.WebFile
    ).switch(
        models.FieldCollection
    ).join(
        models.Trial
    ).switch(
        models.FieldCollection
    ).join(
        models.Location
    ).switch(
        models.FieldCollection
    ).join(
        models.RawCollection
    ).join(
        models.Genotype
    )
    if occurrence != 0:
        result = result.where(models.FieldCollection.occurrence == occurrence,
                     )
    if description != "":
        result = result.where(models.FieldCollection.description == description,
        )
    if agricultural_cycle != "":
        result = result.where(models.FieldCollection.description == description,)
    if len(genotype_ids) != 0:
        result = result.where(models.Genotype.id << genotype_ids,)

    return result