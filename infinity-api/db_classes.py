from peewee import SqliteDatabase, Model, CharField, BooleanField, \
    IntegerField, ForeignKeyField, FloatField


db = SqliteDatabase("infinity.db")


class BaseModel(Model):

    class Meta:
        database = db


class String(BaseModel):
    string_id = CharField(primary_key=True)
    spanish = CharField(null=True)
    english = CharField(null=True)
    french = CharField(null=True)


class Ammo(BaseModel):
    ammo_id = IntegerField(primary_key=True)
    name = ForeignKeyField(String, backref="ammo_names")


class Sectorial(BaseModel):
    sectorial_id = IntegerField(primary_key=True)
    name = ForeignKeyField(String, backref="sectorials")
    is_faction = BooleanField()


class Ability(BaseModel):
    ability_id = IntegerField(primary_key=True)
    name = ForeignKeyField(String, backref="abilities")
    # TODO: Separate items to a different class?
    is_item = BooleanField()
    wiki_url = CharField(null=True)


class Characteristic(BaseModel):
    characteristic_id = IntegerField(primary_key=True)
    name = ForeignKeyField(String, backref="characteristics")


class Unit(BaseModel):
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
    profile_id = IntegerField(primary_key=True)
    unit_id = IntegerField()
    cap = FloatField()
    point_cost = IntegerField()
    name = ForeignKeyField(String)
    regular_orders = IntegerField(null=True)
    irregular_orders = IntegerField(null=True)
    impetuous_orders = IntegerField(null=True)


class Weapon(BaseModel):
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
    weapon_property_id = IntegerField(primary_key=True)
    name = ForeignKeyField(String, backref="weapon_properties")


class ProfileWeapon(BaseModel):
    profile = ForeignKeyField(Profile)
    weapon = ForeignKeyField(Weapon)


class WeaponProperty(BaseModel):
    weapon = ForeignKeyField(Weapon)
    weapon_property = ForeignKeyField(Property)


class ProfileCharacteristic(BaseModel):
    profile = ForeignKeyField(Profile)
    characteristic = ForeignKeyField(Characteristic)


class ProfileAbility(BaseModel):
    profile = ForeignKeyField(Profile)
    ability = ForeignKeyField(Ability)
