from peewee import Model, CharField, BooleanField, IntegerField
from db_manager import db


class Unit(Model):
    unit_id = IntegerField()
    name = CharField()
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
    is_regular = BooleanField()
    is_irregular = BooleanField()
    is_impetuous = BooleanField()
    is_extremely_impetuous = BooleanField()
    has_structure = BooleanField()

    class Meta:
        database = db


class Profile(Model):
    profile_id = IntegerField()
    unit_id = IntegerField()
    cap = IntegerField()
    point_cost = IntegerField()

    class Meta:
        database = db


class Weapon(Model):
    weapon_id = IntegerField()
    damage = IntegerField()
    name = CharField()
    burst_range = IntegerField()
    burst_melee = IntegerField()
    is_melee = BooleanField()

    class Meta:
        database = db


class Ammo(Model):
    ammo_id = IntegerField()
    name = CharField()

    class Meta:
        database = db


class Sectorial(Model):
    sectorial_id = IntegerField()
    name = CharField()

    class Meta:
        database = db


class Faction(Model):
    faction_id = IntegerField()
    name = CharField()

    class Meta:
        database = db


class Ability(Model):
    ability_id = IntegerField()
    name = CharField()
    wiki_url = CharField()

    class Meta:
        database = db


class Characteristic(Model):
    characteristic_id = IntegerField()
    name = CharField()
    wiki_url = CharField()

    class Meta:
        database = db
