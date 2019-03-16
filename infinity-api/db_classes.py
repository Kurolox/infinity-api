from peewee import SqliteDatabase, Model, CharField, BooleanField, \
    IntegerField, ForeignKeyField, FloatField


db = SqliteDatabase('infinity.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1 * 64000,  # 64MB
    'foreign_keys': 1,
    'ignore_check_constraints': 0,
    'synchronous': 0})


class BaseModel(Model):

    class Meta:
        database = db


class String(BaseModel):
    """This class stores all the strings in their respective languages."""

    string_id = CharField(primary_key=True)
    spanish = CharField(null=True)
    english = CharField(null=True)
    french = CharField(null=True)


class Ammo(BaseModel):
    """This class stores the ammunition types."""

    ammo_id = IntegerField(primary_key=True)
    name = ForeignKeyField(String, backref="ammo")


class Sectorial(BaseModel):
    """This class stores the sectorials and factions in the game."""

    sectorial_id = IntegerField(primary_key=True)
    name = ForeignKeyField(String, backref="sectorials")
    is_faction = BooleanField()


class Ability(BaseModel):
    """This class stores all the abilities (and wiki URLs, if any)."""

    ability_id = IntegerField(primary_key=True)
    name = ForeignKeyField(String, backref="abilities")
    is_item = BooleanField()
    wiki_url = CharField(null=True)


class Characteristic(BaseModel):
    """This class stores all the characteristics."""

    characteristic_id = IntegerField(primary_key=True)
    name = ForeignKeyField(String, backref="characteristics")


class Unit(BaseModel):
    """This class stores all the units, their stats and their SVG URL."""

    unit_id = IntegerField(primary_key=True)
    name = ForeignKeyField(String, backref="units")
    svg_icon = CharField()
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
    has_structure = BooleanField()
    sectorial = ForeignKeyField(Sectorial, backref="units")


class Profile(BaseModel):
    """This class stores all the profiles of each unit."""

    profile_id = IntegerField(primary_key=True)
    unit = ForeignKeyField(Unit, backref="profiles")
    cap = FloatField()
    point_cost = IntegerField()
    name = ForeignKeyField(String, backref="profiles")
    regular_orders = IntegerField(null=True)
    irregular_orders = IntegerField(null=True)
    impetuous_orders = IntegerField(null=True)
    linked_units = ForeignKeyField(Unit, null=True, backref="linked_units")


class Weapon(BaseModel):
    """This class stores all the weapons and their stats."""

    weapon_id = IntegerField(primary_key=True)
    damage = CharField()
    name = ForeignKeyField(String, backref="weapons")
    is_melee = BooleanField()
    short_range = CharField(null=True)
    medium_range = CharField(null=True)
    long_range = CharField(null=True)
    maximum_range = CharField(null=True)
    ammo = ForeignKeyField(Ammo, null=True, backref="weapons")
    burst_melee = IntegerField(null=True)
    burst_range = IntegerField(null=True)
    parent_weapon = ForeignKeyField("self", null=True, backref="childs")


class Property(BaseModel):
    """This class stores all the weapon properties."""

    property_id = IntegerField(primary_key=True)
    name = ForeignKeyField(String, backref="properties")


class ProfileWeapon(BaseModel):
    """This class stores the relations between an unit profile and
    all the weapons that profile has available."""

    profile = ForeignKeyField(Profile, backref="weapons")
    weapon = ForeignKeyField(Weapon, backref="profiles")


class WeaponProperty(BaseModel):
    """This class stores the relations between a weapon and
     all of it's properties."""

    weapon = ForeignKeyField(Weapon, backref="properties")
    weapon_property = ForeignKeyField(Property, backref="weapons")


class ProfileCharacteristic(BaseModel):
    """This class stores the relations between an unit profile and
        all the characteristics that profile adds."""

    profile = ForeignKeyField(Profile, backref="characteristics")
    characteristic = ForeignKeyField(Characteristic, backref="profiles")


class ProfileAbility(BaseModel):
    """This class stores the relations between an unit profile and
        all the abilities that profile adds."""

    profile = ForeignKeyField(Profile, backref="abilities")
    ability = ForeignKeyField(Ability, backref="profiles")


class UnitCharacteristic(BaseModel):
    """This class stores the relations between an unit and all the
    characteristics that unit has."""

    unit = ForeignKeyField(Unit, backref="characteristics")
    characteristic = ForeignKeyField(Characteristic, backref="units")


class UnitAbility(BaseModel):
    """This class stores the relations between an unit and all the abilities 
    that unit has."""
    unit = ForeignKeyField(Unit, backref="abilities")
    ability = ForeignKeyField(Ability, backref="units")
