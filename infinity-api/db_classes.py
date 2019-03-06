from peewee import SqliteDatabase, Model, CharField, BooleanField, IntegerField


db = SqliteDatabase("infinity.db")

class BaseModel(Model):

    class Meta:
        database = db


class Unit(BaseModel):
    unit_id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    svg_icon = CharField(unique=True)
    mov_1 = IntegerField()
    mov_2 = IntegerField()
    close_combat = IntegerField()
    ballistic_skill = IntegerField()
    phisique = IntegerField()
    willpower = IntegerField()
    armor = IntegerField()
    bts = IntegerField()
    wounds = IntegerField()
    silhouette = IntegerField()
    availability = IntegerField()
    is_regular = BooleanField()
    is_irregular = BooleanField()
    is_impetuous = BooleanField()
    is_extremely_impetuous = BooleanField()
    has_structure = BooleanField()


class Profile(BaseModel):
    profile_id = IntegerField(primary_key=True)
    unit_id = IntegerField()
    cap = IntegerField()
    point_cost = IntegerField()


class Weapon(BaseModel):
    weapon_id = IntegerField(primary_key=True)
    damage = CharField()
    name = CharField(unique=True)
    #burst_range = IntegerField(default=0)
    #burst_melee = IntegerField(default=0)
    is_melee = BooleanField()


class WeaponProperty(BaseModel):
    weapon_property_id = IntegerField(primary_key=True)
    name = CharField(unique=True)


class Ammo(BaseModel):
    ammo_id = IntegerField(primary_key=True)
    name = CharField(unique=True)


class Sectorial(BaseModel):
    sectorial_id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    is_faction = BooleanField()


class Ability(BaseModel):
    ability_id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    wiki_url = CharField()


class Characteristic(BaseModel):
    characteristic_id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    wiki_url = CharField()


class String(BaseModel):
    string_id = CharField(primary_key=True)
    spanish = CharField()
    english = CharField()
    french = CharField()
