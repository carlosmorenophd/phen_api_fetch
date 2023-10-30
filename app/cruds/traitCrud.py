from app import models
from app.schemas import schemas


def get_or_create(trait: schemas.Trait):
    db_entity = models.Trait.filter(
        models.Trait.name == trait.name
    ).first()
    if db_entity:
        return db_entity
    db_entity = models.Trait(
        name=trait.name,
        number=trait.number,
        description=trait.description,
        co_trait_name=trait.co_trait_name,
        variable_name=trait.variable_name,
        co_id=trait.co_id,
    )
    db_entity.save()
    return db_entity


def update(id: int, trait: schemas.Trait):
    db_entity = models.Trait.filter(models.Trait.id == id).first()
    if not db_entity:
        raise ValueError("The trait does not exist")
    db_entity.co_trait_name = trait.co_trait_name
    db_entity.variable_name = trait.variable_name
    db_entity.co_id = trait.co_id
    db_entity.save()
    return db_entity


def find_by_id(id: int):
    try:
        return models.Trait.get_by_id(id)
    except Exception:
        raise ValueError("Trait can not found")


def find_by_number(number: str):
    trait = models.Trait.filter(models.Trait.number == number).first()
    if not trait:
        raise ValueError("The trait does not exist")
    return trait


def find_by_name(name: str):
    trait = models.Trait.filter(models.Trait.name == name).first()
    if not trait:
        raise ValueError("The trait does not exist")
    return trait


def find_by_name_number(name: str, number: str):
    trait = models.Trait.filter(
        models.Trait.name == name,
        models.Trait.number == number,
    ).first()
    if not trait:
        raise ValueError("The trait does not exist")
    return trait
