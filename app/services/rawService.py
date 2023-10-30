import os
from app.schemas import customs, schemas
from csv import writer
from app.cruds import (
    fieldCollectionCrud,
    genotypeCrud,
    locationCrud,
    rawCrud,
    traitCrud,
    trialCrud,
    unitCrud,
    webFileCrud,
)
from app.services.MeanRawCountryInstituteService import MeanRawCountryInstitute


def get_raw_join_all(raw_filter: customs.RawAllFilter) -> str:
    """ To delete
    Args:
        raw_filter (schemas.RawAllFilter): _description_

    Returns:
        str: _description_
    """
    name_csv = "text.csv"
    if os.path.exists(name_csv):
        os.remove(name_csv)
    write_on_csv(name_csv=name_csv, list_element=["padre", "tipo", "id", "occurencia", "ciclo", "gen numero", "repeticion", "sub bloque", "plot", "genotipo id", "locacion id", "nombre genotipo", "pais", "ciudad", "instituto", "GRAIN_YIELD", "GRAIN_YIELD Unidad",
                 "1000_GRAIN_WEIGHT", "1000_GRAIN_WEIGHT Unidad", "PLANT_HEIGHT", "PLANT_HEIGHT Unidad", "AGRONOMIC_SCORE", "AGRONOMIC_SCORE Unidad", "DAYS_TO_HEADING", "DAYS_TO_HEADING Unidad", "DAYS_TO_MATURITY", "DAYS_TO_MATURITY Unidad", "TEST_WEIGHT", "TEST_WEIGHT Unidad", "mean", "grain_yield_class"])
    mean = MeanRawCountryInstitute(
        country="MEXICO", institute="CIMMYT", index_country=10, index_institute=12, index_data=13)
    for id in raw_filter.ids:
        cursor = rawCrud.get_raw_all_join_by_id(id)
        for row in cursor.fetchall():
            mean.clean()
            cursor_same_genotype = rawCrud.get_raw_join_by_cycle_genotype_id(
                cycle=row[2], genotype_id=int(row[7]))
            for row_child in cursor_same_genotype:
                mean.add_item(row_child=row_child)

            write_on_csv(name_csv=name_csv, list_element=[
                "", "principal", *row, mean.get_mean(),
                mean.get_tag(data_parent=float(row[13]))])
            if raw_filter.is_details:
                for row_child in cursor_same_genotype:
                    type = "otro experimento"
                    if row_child[10] == "MEXICO" and row_child[12] == "CIMMYT":
                        type = "control"
                    write_on_csv(name_csv=name_csv, list_element=[
                        row[0], type, *row_child, ])
    return "OK"


def get_raw_join_all_trait(raw_filter: customs.RawAllFilter) -> str:
    name_csv = "text.csv"
    if 1 in raw_filter.trait_ids:
        raise ValueError(
            "Trait id 1 can't be adding by the user in automatic is adding")
    if os.path.exists(name_csv):
        os.remove(name_csv)
    list_head = ["padre", "tipo", "id", "occurencia", "ciclo", "gen numero",
                 "repeticion", "sub bloque", "plot",
                 "genotipo id", "locacion id", "nombre genotipo", "pais",
                 "ciudad", "instituto", "GRAIN_YIELD"]
    trait_ids = raw_filter.trait_ids
    trait_ids.insert(0, 1)
    traits = rawCrud.get_list_trait(trait_ids=trait_ids)
    for trait in traits:
        list_head.append(trait.name)
    list_head.extend(["mean", "grain_yield_class"])
    write_on_csv(name_csv=name_csv, list_element=list_head)
    mean = MeanRawCountryInstitute(
        country="MEXICO",
        institute="CIMMYT",
        index_country=10,
        index_institute=12,
        index_data=13
    )
    for id in raw_filter.ids:
        cursor = rawCrud.get_raw_by_id_with_trait(id=id, trait_ids=trait_ids)
        for row in cursor.fetchall():
            mean.clean()
            cursor_same_genotype = rawCrud.get_raw_by_cycle_genotype_id_with_trait(
                trait_ids=trait_ids,
                cycle=row[2],
                genotype_id=int(row[7])
            )
            for row_child in cursor_same_genotype:
                mean.add_item(row_child=row_child)
            write_on_csv(name_csv=name_csv, list_element=[
                "", "principal", *row, mean.get_mean(),
                mean.get_tag(data_parent=float(row[13]))])
            if raw_filter.is_details:
                cursor_same_genotype = rawCrud.get_raw_by_cycle_genotype_id_with_trait(
                    trait_ids=trait_ids,
                    cycle=row[2],
                    genotype_id=int(row[7])
                )
                for row_child in cursor_same_genotype:
                    type = "otro experimento"
                    if row_child[10] == "MEXICO" and row_child[12] == "CIMMYT":
                        type = "control"
                    write_on_csv(name_csv=name_csv, list_element=[
                        row[0], type, *row_child, ])
    return "OK"


def write_on_csv(name_csv, list_element):
    with open(name_csv, 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(list_element)
        f_object.close()


def save_raw_data(raw_data: customs.RawData):
    db_location = locationCrud.find_by_country_number(
        country=raw_data.location_country,
        number=raw_data.location_number,
    )
    if not db_location:
        raise ValueError("Can not find location : {}".format(
            raw_data.location_number
        ))
    db_trial = trialCrud.find_by_name(
        name=raw_data.trial_name,
    )
    if not db_trial:
        raise ValueError("Can not found trial {}".format(
            raw_data.trial_name
        ))

    db_unit = unitCrud.get_or_create(
        unit=schemas.UnitCreate(
            name=raw_data.unit_name,
        )
    )
    db_web_file = webFileCrud.get_or_create(
        web_file=schemas.WebFileCreate(
            name=raw_data.web_file_name
        )
    )
    db_trait = traitCrud.get_or_create(
        trait=schemas.TraitCreate(
            name=raw_data.trait_name,
            number=raw_data.trait_number,
            co_id="",
            co_trait_name="",
            description="",
            variable_name="",
        )
    )
    db_field_collection = fieldCollectionCrud.get_by_raw(
        occurrence=raw_data.field_occurrence,
        description=raw_data.field_description,
        agricultural_cycle=raw_data.field_agricultural_cycle,
        web_file=db_web_file,
        trial=db_trial,
        location=db_location,
    )
    db_genotype = genotypeCrud.find_by_ids(
        c_id=raw_data.genotype_c_id,
        s_id=raw_data.genotype_s_id,
    )
    db_raw_collection = rawCrud.create(
        raw_collection=schemas.RawCollectionCreate(
            field_collection_id=db_field_collection.id,
            gen_number=raw_data.genotype_number,
            genotype_id=db_genotype.id,
            hash_raw=raw_data.hash_raw,
            plot=raw_data.plot,
            repetition=raw_data.repetition,
            sub_block=raw_data.sub_block,
            trait_id=db_trait.id,
            unit_id=db_unit.id,
            value_data=raw_data.value_data,
        )
    )
    return db_raw_collection


def search_field_data(raw_collection_field: customs.RawCollectionFieldFilter, name_csv: str):
    if os.path.exists(name_csv):
        os.remove(name_csv)
    result = fieldCollectionCrud.find_by_raw_optional(
        genotype_ids=raw_collection_field.genotype_ids)
    trait_ids = raw_collection_field.trait_ids
    basic_column = ["name", "c_id", "s_id", "country",
                    "institute_name"]
    trait_column = []
    data_sheet = {}
    print("[1-3]-[0-{}]".format(len(result)))
    i = 0
    for field in result:
        print("[1-3]-[{}-{}]".format(i, len(result)))
        i = i+1
        for id in trait_ids:
            trait = traitCrud.find_by_id(id)
            raws = filter(lambda raw: raw.trait.id ==
                          id, field.raw_collections)
            for raw in raws:
                genotype_key = str(raw.genotype.id)
                if not genotype_key in data_sheet:
                    data_sheet[genotype_key] = {}
                    data_sheet[genotype_key]["name"] = raw.genotype.cross_name
                    data_sheet[genotype_key]["c_id"] = raw.genotype.c_id
                    data_sheet[genotype_key]["s_id"] = raw.genotype.s_id
                    data_sheet[genotype_key]["country"] = field.location.country
                    data_sheet[genotype_key]["institute_name"] = field.location.institute_name
                    for environment in field.field_environments:
                        environment_name = "{}:({})".format(
                            environment.environment_definition.name, environment.unit.name)
                        basic_column = adding_whit_out_retired(
                            item=environment_name, list_array=basic_column)
                        data_sheet[genotype_key][environment_name] = environment.value_data
                unit = unitCrud.find_by_id(raw.unit.id)
                name_trait = "{}:{}:({})".format(
                    trait.name, raw.repetition, unit.name)
                adding_whit_out_retired(
                    item=name_trait, list_array=trait_column)
                data_sheet[genotype_key][name_trait] = raw.value_data
    trait_column.sort()
    trait_with_out_repetition = {}
    for trait in trait_column:
        name = trait.split(":")[0]
        if not name in trait_with_out_repetition:
            trait_with_out_repetition[trait.split(":")[0]] = [trait]
        else:
            trait_with_out_repetition[trait.split(
                ":")[0]] = trait_with_out_repetition[trait.split(":")[0]] + [trait]
    print("[2-1][0-{}]".format(len(data_sheet)))
    i = 0
    for key_sheet in data_sheet:
        print("[2-1][{}-{}]".format(i, len(data_sheet)))
        i = i + 1
        for key_trait in trait_with_out_repetition:
            name = "{}:avg".format(key_trait)
            data_sheet[key_sheet][name] = ""
            trait_column = adding_whit_out_retired(
                item=name, list_array=trait_column)
            avg_sum = 0
            avg_count = 0
            for trait in trait_with_out_repetition[key_trait]:
                if trait in data_sheet[key_sheet]:
                    if is_float(data_sheet[key_sheet][trait]):
                        avg_sum = avg_sum + \
                            float(data_sheet[key_sheet][trait])
                        avg_count = avg_count + 1
            if avg_sum != 0:
                data_sheet[key_sheet][name] = avg_sum / avg_count
    trait_column.sort()
    head_column = basic_column + trait_column
    write_on_csv(name_csv=name_csv, list_element=head_column)
    print("[2-1][0-{}]".format(len(data_sheet)))
    i = 0
    for key_sheet in data_sheet:
        print("[2-1][{}-{}]".format(i, len(data_sheet)))
        i = i + 1
        save = []
        for head in head_column:
            if head in data_sheet[key_sheet]:
                save.append(data_sheet[key_sheet][head])
            else:
                save.append("")
        write_on_csv(name_csv=name_csv, list_element=save)
    # TODO: Adding only trait that was valid
    # TODO: adding parameter to request
    #     for head in head_column:
    #         print(head)


def adding_whit_out_retired(item: str, list_array: list) -> list:
    if len(list_array) == 0:
        list_array.append(item)
    if not item in list_array:
        list_array.append(item)
    return list_array


def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
