import models
from schemas import schemas


def find_by_id(id: int):
    try:
        return models.Genotype.get_by_id(id)
    except Exception:
        raise ValueError("Genotype can not found")


def find_by_ids(c_id: int, s_id: int):
    genotype = models.Genotype.filter(
        models.Genotype.s_id == s_id
    ).filter(
        models.Genotype.c_id == c_id
    ).first()
    if not genotype:
        raise ValueError(
            "The genotype does not exist {}-{}".format(c_id, s_id))
    return genotype


def find_ids() -> list:
    """Get all id from genotype entity
    Returns:
        list: list of id sorter less to more
    """
    return [genotype.id for genotype in models.Genotype.select(models.Genotype.id).order_by(models.Genotype.id)]
