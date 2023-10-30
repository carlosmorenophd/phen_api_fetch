from app import models
from app.schemas import schemas, customs

# TODO: Convertir en dinamica para poder seleccionar con una lista de traits
# TODO: soportar la unidad dentro de los traits

query_raw_all = "SELECT raj.id, raj.occurrence, raj.`cycle`, raj.gen_number, raj.repetition, raj.sub_block, raj.plot, raj.genotype_id, raj.location_id, \
g.cross_name, l.country , l.description , l.institute_name , \
raj.value_1,'t/ha' as u_1,  raj.value_2, 'g' as u_2, raj.value_3,'cm' as u_3, raj.value_5, '1-5' as u_5, raj.value_6, 'dias' as u_6, raj.value_12, 'dias' as u_12, raj.value_14, 'doble digito' as u_14 \
FROM raw_all_join raj \
LEFT JOIN genotype g ON g.id =raj.genotype_id \
LEFT JOIN location l ON l.id = raj.location_id "


query_basic_select = "SELECT raj.id, raj.occurrence, raj.`cycle`, \
    raj.gen_number, raj.repetition, raj.sub_block, raj.plot, \
    raj.genotype_id, raj.location_id, g.cross_name, l.country, \
    l.description , l.institute_name "
query_basic_from = " FROM raw_all_join raj \
LEFT JOIN genotype g ON g.id =raj.genotype_id \
LEFT JOIN location l ON l.id = raj.location_id "


def get_raw_all_join_by_id(id: int):
    """To delete

    Args:
        id (int): _description_

    Returns:
        any: return
    """
    cursor = models.db.execute_sql(
        "{}WHERE raj.id = {}; ".format(query_raw_all, id))
    return cursor


def get_raw_join_by_cycle_genotype_id(cycle: str, genotype_id: int):
    """To delete

    Args:
        cycle (str): _description_
        genotype_id (int): _description_

    Returns:
        _type_: _description_
    """
    cursor = models.db.execute_sql(
        "{} WHERE raj.`cycle` = {} and raj.genotype_id = {} ; "
        .format(query_raw_all, cycle, str(genotype_id)))
    return cursor


def get_raw_by_id_with_trait(id: int, trait_ids: list[int]):
    cursor = models.db.execute_sql(
        "{} {} {} WHERE raj.id = {}; ".format(
            query_basic_select,
            get_attributes_from_query(trait_ids),
            query_basic_from,
            id
        )
    )
    return cursor


def get_raw_by_cycle_genotype_id_with_trait(
    trait_ids: list[int],
    cycle: str,
    genotype_id: int
):

    cursor = models.db.execute_sql(
        "{} {} {} WHERE raj.`cycle` = {} and raj.genotype_id = {} ; "
        .format(
            query_basic_select,
            get_attributes_from_query(trait_ids),
            query_basic_from,
            cycle,
            str(genotype_id)
        )
    )
    return cursor


def get_attributes_from_query(trait_ids: list[int]) -> str:
    attribute_query = ""
    for id in trait_ids:
        attribute_query = attribute_query + ", raj.value_{}".format(str(id))
    return attribute_query


def get_list_trait(trait_ids: list[int]):
    result = models.Trait.select().where(models.Trait.id.in_(trait_ids))
    return result


def create(raw_collection: schemas.RawCollectionCreate):
    trait = models.Trait.filter(
        models.Trait.id == raw_collection.trait_id).first()
    if not trait:
        raise ValueError("The Trait is not valid")
    genotype = models.Genotype.filter(
        models.Genotype.id == raw_collection.genotype_id
    ).first()
    if not genotype:
        raise ValueError("The Genotype is not valid")
    unit = models.Unit.filter(models.Unit.id == raw_collection.unit_id).first()
    if not unit:
        raise ValueError("The Unit is not valid")

    field_collection = models.FieldCollection.filter(
        models.FieldCollection.id == raw_collection.field_collection_id
    ).first()
    if not field_collection:
        raise ValueError(
            "The field_collection is not valid id -> {}".format(
                raw_collection.field_collection_id
            ))
    db_entity = models.RawCollection.filter(
        models.RawCollection.hash_raw == raw_collection.hash_raw
    ).first()
    if db_entity:
        return db_entity
    db_entity = models.RawCollection(
        field_collection=field_collection,
        gen_number=raw_collection.gen_number,
        repetition=raw_collection.repetition,
        sub_block=raw_collection.sub_block,
        plot=raw_collection.plot,
        value_data=raw_collection.value_data,
        trait=trait,
        genotype=genotype,
        unit=unit,
        hash_raw=raw_collection.hash_raw,
    )
    db_entity.save()
    return db_entity


def search(id: int, raw_collection: customs.RawCollectionFilter):
    query = models.RawCollection.select()
    if raw_collection.occurrence != 0:
        query = query.where(
            models.RawCollection.occurrence == raw_collection.occurrence)
    if raw_collection.cycle != "":
        query = query.where(models.RawCollection.cycle == raw_collection.cycle)
    if raw_collection.gen_number != 0:
        query = query.where(models.RawCollection.gen_number ==
                            raw_collection.gen_number)
    if raw_collection.repetition != 0:
        query = query.where(models.RawCollection.repetition ==
                            raw_collection.repetition)
    if raw_collection.sub_block != 0:
        query = query.where(models.RawCollection.sub_block ==
                            raw_collection.sub_block)
    if raw_collection.plot != 0:
        query = query.where(models.RawCollection.plot == raw_collection.plot)
    if raw_collection.value_data != "":
        query = query.where(models.RawCollection.value_data ==
                            raw_collection.value_data)
    if raw_collection.trial_id != 0:
        query = query.where(models.RawCollection.trial_id ==
                            raw_collection.trial_id)
    if raw_collection.trait_id != 0:
        query = query.where(models.RawCollection.trait_id ==
                            raw_collection.trait_id)
    if raw_collection.genotype_id != 0:
        query = query.where(models.RawCollection.genotype_id ==
                            raw_collection.genotype_id)
    if raw_collection.location_id != 0:
        query = query.where(models.RawCollection.location_id ==
                            raw_collection.location_id)
    if raw_collection.unit_id != 0:
        query = query.where(models.RawCollection.unit_id ==
                            raw_collection.unit_id)
    return query.execute()


def list_query_ids(
    target: customs.EntityTarget
) -> list[customs.ResponseTarget]:
    if target == customs.EntityTarget.genotype:
        return list(
            map(
                lambda id: customs.ResponseTarget(
                    id=id.id, name=id.cross_name),
                models.Genotype.select(
                    models.Genotype.id,
                    models.Genotype.cross_name
                ).order_by(models.Genotype.id).execute()))
    elif target == customs.EntityTarget.location:
        return list(
            map(
                lambda id: customs.ResponseTarget(
                    id=id.id,
                    name=id.description
                ), models.Location.select(
                    models.Location.id,
                    models.Location.country
                ).order_by(models.Location.id).execute()))
    elif target == customs.EntityTarget.trait:
        return list(
            map(lambda id: customs.ResponseTarget(
                id=id.id,
                name=id.name
            ), models.Trait.select(
                models.Trait.id,
                models.Trait.name
            ).order_by(models.Trait.id).execute()))
    elif target == customs.EntityTarget.repetition:
        return list(
            map(lambda id: customs.ResponseTarget(
                id=int(id.repetition),
                name=str(id.repetition)
            ), models.RawCollection.select(
                models.RawCollection.repetition
            ).distinct().order_by(models.RawCollection.repetition).execute()))
    elif target == customs.EntityTarget.agricultural_cycle:
        return list(
            map(lambda id: customs.ResponseTarget(
                id=int(id.agricultural_cycle),
                name=id.agricultural_cycle
            ), models.FieldCollection.select(
                models.FieldCollection.agricultural_cycle
            ).distinct().order_by(
                models.FieldCollection.agricultural_cycle
            ).execute()))
    raise ValueError("Unsupported target")
