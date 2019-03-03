from db_manager import db
from db_classes import Unit, Weapon, Ammo, Ability, Characteristic, Sectorial, Profile, String, WeaponProperty
from peewee import SqliteDatabase
from json import load
from os import listdir
from collections import defaultdict


def generate_db(db: SqliteDatabase) -> None:
    """Generates all the database tables."""
    with db as open_db:
        open_db.create_tables(
            [Unit, Weapon, Ammo, Ability, Characteristic, Sectorial,
             Profile, String, WeaponProperty])


def populate_ammo(db: SqliteDatabase) -> None:
    """Populates the ammo types in it's database table. It will fetch the information from the specified language"""

    ammo_dict = {}

    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_MUNICION.json") as ammo_file:
            for item in load(ammo_file):
                if item["id"] not in ammo_dict.keys():
                    ammo_dict[item["id"]] = {language: ""}
                ammo_dict[item["id"]][language] = item["nombre"]

    Ammo.bulk_create(
        tuple(Ammo(ammo_id=ammo, name=f"ammo_{ammo}")
              for ammo in ammo_dict.keys()))

    populate_strings("ammo", ammo_dict)


def populate_strings(id_prefix: str, string_dict: tuple) -> None:
    """Generates the strings in the database. It needs a dict of dicts,
    with the key of each dict being the string id in the database and the values being the strings in each language.
    The key of each language has to be the three initials in upper case (ENG, ESP, FRA...)"""

    # TODO: Remove hardcoded languages and make it depend on the String defined languages only
    String.bulk_create(
        tuple(String(
            string_id=f"{id_prefix}_{str_id}", english=strings["ENG"],
            spanish=strings["ESP"], french=strings["FRA"])
            for str_id, strings in string_dict.items()))


def populate_sectorials(db: SqliteDatabase) -> None:
    """Populates the database with a list of sectorials and their respective ID's."""

    sectorial_dict = {}

    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_SECTORIAL_NOMBRE.json") as ammo_file:
            for sectorial, name in load(ammo_file)["nombresSectorial"].items():
                sectorial_id = int(sectorial.lstrip("idSectorial_"))
                if sectorial_id not in sectorial_dict.keys():
                    sectorial_dict[sectorial_id] = {}
                sectorial_dict[sectorial_id][language] = name

    Sectorial.bulk_create(
        tuple(
            Sectorial(
                sectorial_id=sectorial,
                name=f"sectorial_{sectorial}",
                is_faction=True if sectorial % 100 == 1 else False)
            for sectorial in sectorial_dict.keys()))

    populate_strings("sectorial", sectorial_dict)


def populate_weapons(db: SqliteDatabase) -> None:
    """Populates the weapons and weapon characteristic tables."""
    populate_weapon_properties(db)


def populate_weapon_properties(db: SqliteDatabase) -> None:
    """Based on the local weapons JSON, extracts all the weapon properties
    and populates the corresponding database table, and adds the strings to the string table."""

    weapon_property_dict = {}

    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_ARMAS.json") as weapon_file:
            for weapon in load(weapon_file):
                for property_id, property_name in zip(
                    # TODO: Modify this workaround for weapons with no properties
                    [int(identifier or 0)
                     for identifier in weapon["propiedades"].split("|")],
                        weapon["lista_propiedades"].split("|")):
                    if property_id not in weapon_property_dict.keys():
                        weapon_property_dict[property_id] = {}
                    weapon_property_dict[property_id][language] = property_name

    WeaponProperty.bulk_create([
        WeaponProperty(
            weapon_property_id=property_id,
            name=f"weapon_property_{property_id}")
        for property_id in weapon_property_dict.keys()])

    populate_strings("weapon_property", weapon_property_dict)
    print("wew")


def populate_db(db: SqliteDatabase) -> None:
    """Populates the database tables with the local JSON information."""
    with db as open_db:
        populate_ammo(open_db)
        populate_sectorials(open_db)
        populate_weapons(open_db)


if "infinity.py" not in listdir():
    generate_db(db)
populate_db(db)
