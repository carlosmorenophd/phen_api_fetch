import models
from schemas import schemas


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

def find_ids() -> list :
    """Get list of ids from trait

    Returns:
        list: List of ids from trait
    """
    return [trait.id for trait in models.Trait.select(models.Trait.id).order_by(models.Trait.id)]