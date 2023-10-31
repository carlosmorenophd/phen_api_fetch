from peewee import CharField, ForeignKeyField, IntegerField, Model, TextField

from database import db


class WebFile(Model):
    name = CharField(max_length=200)

    class Meta:
        database = db


class Trial(Model):
    name = CharField(unique=True, index=True)

    class Meta:
        database = db


class Unit(Model):
    name = CharField(unique=True, index=True)

    class Meta:
        database = db


class Trait(Model):
    name = CharField(unique=True, index=True)
    number = CharField()
    description = TextField(null=True)
    co_trait_name = CharField(null=True)
    variable_name = CharField(null=True)
    co_id = CharField(null=True)

    class Meta:
        database = db


class Genotype(Model):
    c_id = IntegerField()
    s_id = IntegerField()
    cross_name = CharField(index=True)
    history_name = TextField()

    class Meta:
        database = db


class Location(Model):
    number = IntegerField()
    country = CharField()
    institute_name = CharField()
    cooperator = CharField()
    latitude = CharField(null=True)
    latitude_degrees = IntegerField(null=True)
    latitude_minutes = IntegerField(null=True)
    longitude = CharField(null=True)
    longitude_degrees = IntegerField(null=True)
    longitude_minutes = IntegerField(null=True)
    altitude = IntegerField(null=True)

    class Meta:
        database = db


class CropOntology(Model):
    ontology_db_id = CharField()
    name = CharField()

    class Meta:
        database = db


class TraitOntology(Model):
    trait_db_id = CharField()
    name = CharField()
    class_family = CharField()
    description = TextField()
    crop_ontology = ForeignKeyField(CropOntology, backref="trait_ontologies")

    class Meta:
        database = db


class MethodOntology(Model):
    method_db_id = CharField()
    name = CharField()
    class_family = CharField()
    description = TextField()
    formula = TextField()

    class Meta:
        database = db


class ScaleOntology(Model):
    scale_db_id = CharField(unique=True, index=True)
    name = CharField()
    data_type = CharField()
    valid_values = TextField()

    class Meta:
        database = db


class VariableOntology(Model):
    name = CharField()
    synonyms = TextField()
    growth_stage = TextField()
    observation_variable_db_id = CharField()
    trait_ontology = ForeignKeyField(
        TraitOntology, backref="variable_ontologies")
    trait = ForeignKeyField(Trait, backref="variable_ontology")
    method_ontology = ForeignKeyField(
        MethodOntology, backref="variable_ontologies")
    scale_ontology = ForeignKeyField(
        ScaleOntology, backref="variable_ontologies")

    class Meta:
        database = db


class FieldCollection(Model):
    agricultural_cycle = CharField(max_length=4)
    occurrence = IntegerField()
    description = TextField()
    location = ForeignKeyField(Location, backref="field_collections")
    trial = ForeignKeyField(Trial, backref="field_collections")
    web_file = ForeignKeyField(WebFile, backref="filed_collections")

    class Meta:
        database = db


class EnvironmentDefinition(Model):
    number = IntegerField()
    name = CharField(max_length=300)

    class Meta:
        database = db


class FieldCollectionEnvironment(Model):
    field_collection = ForeignKeyField(
        FieldCollection, backref="field_environments"
    )
    environment_definition = ForeignKeyField(
        EnvironmentDefinition, backref="field_environments"
    )
    unit = ForeignKeyField(
        Unit, backref="field_environments"
    )
    value_data = CharField(max_length=200)

    class Meta:
        database = db


class RawCollection(Model):
    hash_raw = CharField(max_length=500)
    repetition = IntegerField()
    sub_block = IntegerField()
    plot = IntegerField()
    trait = ForeignKeyField(
        Trait, backref="raw_collections"
    )
    unit = ForeignKeyField(
        Unit, backref="raw_collections"
    )
    field_collection = ForeignKeyField(
        FieldCollection, backref="raw_collections"
    )
    value_data = CharField()
    gen_number = IntegerField()
    genotype = ForeignKeyField(
        Genotype, backref="field_collections"
    )

    class Meta:
        database = db
