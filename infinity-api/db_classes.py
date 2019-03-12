from peewee import SqliteDatabase, Model, CharField, BooleanField, \
    IntegerField, ForeignKeyField, FloatField


db = SqliteDatabase("infinity.db")


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
    name = ForeignKeyField(String, backref="ammo_names")


class Sectorial(BaseModel):
    """This class stores the sectorials and factions in the game."""

    sectorial_id = IntegerField(primary_key=True)
    name = ForeignKeyField(String, backref="sectorials")
    is_faction = BooleanField()


class Ability(BaseModel):
    """This class stores all the abilities (and wiki URLs, if any)."""

    ability_id = IntegerField(primary_key=True)
    name = ForeignKeyField(String, backref="abilities")
    # TODO: Separate items to a different class?
    is_item = BooleanField()
    wiki_url = CharField(null=True)


class Characteristic(BaseModel):
    """This class stores all the characteristics."""

    characteristic_id = IntegerField(primary_key=True)
    name = ForeignKeyField(String, backref="characteristics")


class Unit(BaseModel):
    """This class stores all the units, their stats and their SVG URL."""

    unit_id = IntegerField(primary_key=True)
    name = CharField(unique=True)
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


class Profile(BaseModel):
    """This class stores all the profiles of each unit."""

    profile_id = IntegerField(primary_key=True)
    unit_id = IntegerField()
    cap = FloatField()
    point_cost = IntegerField()
    name = ForeignKeyField(String)
    regular_orders = IntegerField(null=True)
    irregular_orders = IntegerField(null=True)
    impetuous_orders = IntegerField(null=True)
    linked_units = ForeignKeyField(Unit, null=True)


class Weapon(BaseModel):
    """This class stores all the weapons and their stats."""

    weapon_id = IntegerField(primary_key=True)
    damage = CharField()
    name = ForeignKeyField(String, backref="weapon_names")
    is_melee = BooleanField()
    short_range = CharField(null=True)
    medium_range = CharField(null=True)
    long_range = CharField(null=True)
    maximum_range = CharField(null=True)
    ammo = ForeignKeyField(Ammo, null=True, backref="weapon_ammo")
    burst_melee = IntegerField(null=True)
    burst_range = IntegerField(null=True)
    parent_weapon = ForeignKeyField("self", null=True)


class Property(BaseModel):
    """This class stores all the weapon properties."""

    weapon_property_id = IntegerField(primary_key=True)
    name = ForeignKeyField(String, backref="weapon_properties")


class ProfileWeapon(BaseModel):
    """This class stores the relations between an unit profile and
    all the weapons that profile has available."""

    profile = ForeignKeyField(Profile)
    weapon = ForeignKeyField(Weapon)


class WeaponProperty(BaseModel):
    """This class stores the relations between a weapon and
     all of it's properties."""

    weapon = ForeignKeyField(Weapon)
    weapon_property = ForeignKeyField(Property)


class ProfileCharacteristic(BaseModel):
    """This class stores the relations between an unit profile and
        all the characteristics that profile adds."""

    profile = ForeignKeyField(Profile)
    characteristic = ForeignKeyField(Characteristic)


class ProfileAbility(BaseModel):
    """This class stores the relations between an unit profile and
        all the abilities that profile adds."""

    profile = ForeignKeyField(Profile)
    ability = ForeignKeyField(Ability)


class UnitProfile(BaseModel):
    """This class stores the relations between an unit and all the profiles
    that unit has."""

    unit = ForeignKeyField(Unit)
    profile = ForeignKeyField(Profile)


class UnitCharacteristic(BaseModel):
    """This class stores the relations between an unit and all the
    characteristics that unit has."""

    unit = ForeignKeyField(Unit)
    characteristic = ForeignKeyField(Characteristic)


class UnitAbility(BaseModel):
    """This class stores the relations between an unit and all the abilities 
    that unit has."""
    unit = ForeignKeyField(Unit)
    ability = ForeignKeyField(Ability)
