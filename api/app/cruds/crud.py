from app import models
from app.schemas import schemas


def create_crop_ontology(crop_ontology: schemas.CropOntology):
    db_entity = models.CropOntology.filter(
        models.CropOntology.name == crop_ontology.name
    ).first()
    if db_entity:
        return db_entity
    db_entity = models.CropOntology(
        name=crop_ontology.name, ontology_db_id=crop_ontology.ontology_db_id
    )
    db_entity.save()
    return db_entity


def create_trait_ontology(trait_ontology: schemas.TraitOntology):
    db_entity = models.TraitOntology.filter(
        models.TraitOntology.trait_db_id == trait_ontology.trait_db_id
    ).first()
    if db_entity:
        return db_entity
    crop_ontology = models.CropOntology.filter(
        models.CropOntology.id == trait_ontology.crop_ontology_id
    ).first()
    if not crop_ontology:
        raise ValueError("The crop ontology is not valid")
    db_entity = models.TraitOntology(
        trait_db_id=trait_ontology.trait_db_id,
        name=trait_ontology.name,
        class_family=trait_ontology.class_family,
        description=trait_ontology.description,
        crop_ontology=crop_ontology,
    )
    db_entity.save()
    return db_entity


def create_method_ontology(method_ontology: schemas.MethodOntology):
    db_entity = models.MethodOntology.filter(
        models.MethodOntology.method_db_id == method_ontology.method_db_id
    ).first()
    if db_entity:
        return db_entity
    db_entity = models.MethodOntology(
        method_db_id=method_ontology.method_db_id,
        name=method_ontology.name,
        class_family=method_ontology.class_family,
        description=method_ontology.description,
        formula=method_ontology.formula,
    )
    db_entity.save()
    return db_entity


def create_scale_ontology(scale_ontology: schemas.ScaleOntology):
    db_entity = models.ScaleOntology.filter(
        models.ScaleOntology.scale_db_id == scale_ontology.scale_db_id
    ).first()
    if db_entity:
        return db_entity
    db_entity = models.ScaleOntology(
        scale_db_id=scale_ontology.scale_db_id,
        name=scale_ontology.name,
        data_type=scale_ontology.data_type,
        valid_values=scale_ontology.valid_values,
    )
    db_entity.save()
    return db_entity


def create_variable_ontology(variable_ontology: schemas.VariableOntology):
    db_entity = models.VariableOntology.filter(
        models.VariableOntology.observation_variable_db_id
        == variable_ontology.observation_variable_db_id
    ).first()
    if db_entity:
        return db_entity
    trait_ontology = models.TraitOntology.filter(
        models.TraitOntology.id == variable_ontology.trait_ontology_id
    ).first()
    if not trait_ontology:
        raise ValueError("The Crop Ontology is not valid")
    trait = models.Trait.filter(
        models.Trait.id == variable_ontology.trait_id).first()
    if not trait:
        raise ValueError("The Trait is not valid")
    method_ontology = models.MethodOntology.filter(
        models.MethodOntology.id == variable_ontology.method_ontology_id
    ).first()
    if not method_ontology:
        raise ValueError("The Method Ontology is not valid")
    scale_ontology = models.ScaleOntology.filter(
        models.ScaleOntology.id == variable_ontology.scale_ontology_id
    ).first()
    if not scale_ontology:
        raise ValueError("The Scale Ontology is not valid")
    db_entity = models.VariableOntology(
        name=variable_ontology.name,
        synonyms=variable_ontology.synonyms,
        growth_stage=variable_ontology.growth_stage,
        observation_variable_db_id=variable_ontology.observation_variable_db_id,
        trait_ontology=trait_ontology,
        trait=trait,
        method_ontology=method_ontology,
        scale_ontology=scale_ontology,
    )
    db_entity.save()
    return db_entity


def search_trial_by_name(name: str):
    return list(models.Trial.filter(models.Trial.name % name))
