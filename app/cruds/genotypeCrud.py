from app import models
from app.schemas import schemas


def find_by_id(id: int):
    try:
        return models.Genotype.get_by_id(id)
    except Exception:
        raise ValueError("Genotype can not found")


def create(genotype: schemas.Genotype):
    db_entity = models.Genotype.filter(
        models.Genotype.c_id == genotype.c_id
    ).filter(
        models.Genotype.s_id == genotype.s_id
    ).first()
    if db_entity:
        return db_entity
    db_entity = models.Genotype(
        c_id=genotype.c_id,
        s_id=genotype.s_id,
        cross_name=genotype.cross_name,
        history_name=genotype.history_name,
    )
    db_entity.save()
    return db_entity


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
