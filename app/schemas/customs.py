from pydantic import BaseModel, Field
from enum import Enum


class EnvironmentData(BaseModel):
    trial_name: str
    location_number: int
    location_country: str
    trait_number: str
    trait_name: str
    occurrence: int
    description: str
    agricultural_cycle: str
    value_data: str
    unit_name: str
    web_file_name: str


class RawCollectionFilter(BaseModel):
    occurrence: int = Field(default=0)
    agricultural_cycle: str = Field(default="")
    gen_number: int = Field(default=0)
    repetition: int = Field(default=0)
    sub_block: int = Field(default=0)
    plot: int = Field(default=0)
    value_data: str = Field(default="")
    trial_id: int = Field(default=0)
    trait_id: int = Field(default=0)
    genotype_id: int = Field(default=0)
    location_id: int = Field(default=0)
    unit_id: int = Field(default=0)


class EntityTarget(str, Enum):
    genotype = "genotype"
    trait = "trait"
    repetition = "repetition"
    location = "location"
    agricultural_cycle = "agricultural_cycle"


class ResponseTarget (BaseModel):
    id: int
    name: str


class RawAllFilter(BaseModel):
    ids: list[int]
    is_details: bool = False
    trait_ids: list[int]


class RawData(BaseModel):
    trial_name: str
    location_number: int
    location_country: str
    trait_number: str
    trait_name: str
    field_occurrence: int
    field_description: str
    field_agricultural_cycle: str
    unit_name: str
    web_file_name: str
    genotype_c_id: int
    genotype_s_id: int
    genotype_name: str
    genotype_number: int
    repetition: int
    sub_block: int
    plot: int
    value_data: str
    hash_raw: str

class RawCollectionFieldFilter(BaseModel):
    trait_ids: list[int] = Field(default=[])
    genotype_ids: list[int] = Field(default=[])