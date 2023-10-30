from typing import Any, Union
from peewee import ModelSelect
from pydantic import BaseModel
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        return res


class WebFileBase(BaseModel):
    name: str


class WebFileCreate(WebFileBase):
    pass


class WebFile(WebFileBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class TrialBase(BaseModel):
    name: str


class TrialCreate(TrialBase):
    pass


class Trial(TrialBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class UnitBase(BaseModel):
    name: str


class UnitCreate(UnitBase):
    pass


class Unit(UnitBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class TraitBase(BaseModel):
    name: str
    number: str
    description: str
    co_trait_name: str
    variable_name: str
    co_id: str


class TraitCreate(TraitBase):
    pass


class Trait(TraitBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class GenotypeBase(BaseModel):
    c_id: int
    s_id: int
    cross_name: str
    history_name: str


class GenotypeCreate(GenotypeBase):
    pass


class Genotype(GenotypeBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class LocationBase(BaseModel):
    number: int
    country: str
    institute_name: str
    cooperator: str
    latitude: Union[str, None]
    latitude_degrees: Union[int, None]
    latitude_minutes: Union[int, None]
    longitude: Union[str, None]
    longitude_degrees: Union[int, None]
    longitude_minutes: Union[int, None]
    altitude: Union[int, None]


class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class CropOntologyBase(BaseModel):
    ontology_db_id: str
    name: str


class CropOntologyCreate(CropOntologyBase):
    pass


class CropOntology(CropOntologyBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class TraitOntologyBase(BaseModel):
    trait_db_id: str
    name: str
    class_family: str
    description: str


class TraitOntologyCreate(TraitOntologyBase):
    crop_ontology_id: int


class TraitOntology(TraitOntologyBase):
    id: int
    crop_ontology: CropOntology

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class MethodOntologyBase(BaseModel):
    method_db_id: str
    name: str
    class_family: str
    description: str
    formula: str


class MethodOntologyCreate(MethodOntologyBase):
    pass


class MethodOntology(MethodOntologyBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class ScaleOntologyBase(BaseModel):
    scale_db_id: str
    name: str
    data_type: str
    valid_values: str


class ScaleOntologyCreate(ScaleOntologyBase):
    pass


class ScaleOntology(ScaleOntologyBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class VariableOntologyBase(BaseModel):
    growth_stage: str
    name: str
    observation_variable_db_id: str
    synonyms: str


class VariableOntologyCreate(VariableOntologyBase):
    method_ontology_id: int
    scale_ontology_id: int
    trait_id: int
    trait_ontology_id: int


class VariableOntology(VariableOntologyBase):
    id: int
    method_ontology: MethodOntology
    scale_ontology: ScaleOntology
    trait_ontology: TraitOntology
    trait: Trait

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class FieldCollectionBase(BaseModel):
    occurrence: int
    agricultural_cycle: str
    description: str


class FieldCollectionCreate(FieldCollectionBase):
    trial_id: int
    location_id: int
    web_file_id: int


class FieldCollection(FieldCollectionBase):
    id: int
    trial: Trial
    location: Location
    web_file: WebFile

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class EnvironmentDefinitionBase(BaseModel):
    number: int
    name: str


class EnvironmentDefinitionCreate(EnvironmentDefinitionBase):
    pass


class EnvironmentDefinition(EnvironmentDefinitionBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class FieldCollectionEnvironmentBase(BaseModel):
    value_data: str


class FieldCollectionEnvironmentCreate(FieldCollectionEnvironmentBase):
    field_collection_id: int
    environment_definition_id: int
    unit_id: int


class FieldCollectionEnvironment(FieldCollectionEnvironmentBase):
    id: int
    field_collection: FieldCollection
    environment_definition: EnvironmentDefinition
    unit: Unit

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class RawCollectionBase(BaseModel):
    hash_raw: str
    gen_number: int
    repetition: int
    sub_block: int
    plot: int
    value_data: str


class RawCollectionCreate(RawCollectionBase):
    trait_id: int
    genotype_id: int
    field_collection_id: int
    unit_id: int


class RawCollection(RawCollectionBase):
    id: int
    trait: Trait
    genotype: Genotype
    field_collection: FieldCollection
    unit: Unit

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
