from db_classes import db, Unit, Weapon, Ammo, Ability, Characteristic, \
    Sectorial, Profile, String, WeaponProperty
from peewee import SqliteDatabase
from json import load
from os import listdir
from collections import defaultdict
from fetcher import fetch_json


def generate_db(db: SqliteDatabase) -> None:
    """Generates all the database tables."""
    with db as open_db:
        open_db.create_tables(
            [Unit, Weapon, Ammo, Ability, Characteristic, Sectorial,
             Profile, String, WeaponProperty])


def populate_ammo() -> None:
    """Populates the ammo types in it's database table."""

    ammo_dict = defaultdict(dict)

    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_MUNICION.json") as ammo_file:
            for item in load(ammo_file):
                ammo_dict[item["id"]][language] = item["nombre"]

    populate_strings("ammo", ammo_dict)

    for ammo in ammo_dict.keys():
        if Ammo.get_or_create(ammo_id=ammo, name=String.get_by_id(
                f"ammo_{ammo}"))[1]:
            print(f"Generating entry {ammo} in Ammo table...")


def populate_strings(id_prefix: str, string_dict: tuple) -> None:
    """Generates the strings in the database. It needs a dict of dicts,
    with the key of each dict being the string id in the database, 
    and the values being the strings in each language.
    The key of each language has to be the three initials (ENG, ESP, FRA...)"""

    # TODO: Make language recognition automated rather than hardcoded

    for string_id, strings in string_dict.items():

        if String.get_or_create(
                string_id=f"{id_prefix}_{string_id}",
                english=strings["ENG"] if "ENG" in strings.keys() else None,
                spanish=strings["ESP"] if "ESP" in strings.keys() else None,
                french=strings["FRA"] if "FRA" in strings.keys() else None)[1]:
            print(
                f"Generating entry {id_prefix}_{string_id} in String table...")


def populate_sectorials() -> None:
    """Populates the database with the sectorials and their respective ID's."""

    sectorial_dict = defaultdict(dict)

    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_SECTORIAL_NOMBRE.json") as ammo_file:
            for sectorial, name in load(ammo_file)["nombresSectorial"].items():
                sectorial_dict[int(sectorial.lstrip(
                    "idSectorial_"))][language] = name

    populate_strings("sectorial", sectorial_dict)

    for sectorial in sectorial_dict.keys():
        if Sectorial.get_or_create(
                sectorial_id=sectorial, name=String.get_by_id(
                    f"sectorial_{sectorial}"),
                is_faction=True if sectorial % 100 == 1 else False)[1]:
            print(f"Generating entry {sectorial} in Sectorial table...")


def populate_weapons() -> None:
    """Populates the weapons and weapon characteristic tables."""

    populate_weapon_properties()

    weapon_dict = defaultdict(dict)

    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_ARMAS.json") as weapon_file:
            for weapon in load(weapon_file):
                weapon_dict[int(weapon["id"])
                            ][language] = weapon["nombre_completo"]

    populate_strings("weapon", weapon_dict)

    weapon_wiki_dict = defaultdict(dict)
    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_ARMAS_WIKI_URLS.json") as weapon_wiki:
            for weapon_id, weapon_wiki_link in load(weapon_wiki).items():
                weapon_wiki_dict[int(weapon_id)][language] = weapon_wiki_link

    populate_strings("weapon_wiki", weapon_wiki_dict)

    with open(f"JSON/{listdir('JSON')[0]}/JSON_ARMAS.json") as weapon_file:
        for weapon in load(weapon_file):
            burst_range, burst_melee = calculate_burst(weapon)
            weapon_properties = {
                "weapon_id": int(weapon["id"]),
                # TODO: Correct damage language by using JSON_ATRIBUTOS_ROT
                "damage": weapon["dano"],
                "name": String.get_by_id(f"weapon_{weapon['id']}"),
                "is_melee": True if weapon["CC"] == "1" else False,
                "short_range": validate_range(weapon["corta"]),
                "medium_range": validate_range(weapon["media"]),
                "long_range": validate_range(weapon["larga"]),
                "maximum_range": validate_range(weapon["maxima"]),
                "ammo": Ammo.get_by_id(int(weapon["idMunicion"]))
                if int(weapon["idMunicion"]) else None,
                "burst_range": burst_range, "burst_melee": burst_melee}
            if Weapon.get_or_create(**weapon_properties)[1]:
                print(
                    f"Generating entry {weapon['id']} in Weapon table...")


def calculate_burst(weapon: dict) -> tuple:
    """Get the burst values of a weapon depending if it's melee, ranged or both.
    The first value is the ranged burst, while the second one is the CC burst.
    If the weapon only has one type of burst, the other one will be None."""

    burst = weapon["rafaga"]

    if "(" in burst:
        return tuple(int(char) for char in burst if char.isdigit())
    if not [char for char in burst if char.isdigit()]:
        return None, None
    return (int(burst), None) if not int(weapon["CC"]) else (None, int(burst))


def validate_range(weapon_range: str) -> str:
    """Given a weapon value range, it checks if it's a valid range or not.
     If it isn't, this returns Null."""

    return weapon_range.replace("|", ",") if "|" in weapon_range else None


def populate_weapon_properties() -> None:
    """Based on the local weapons JSON, extracts all the weapon properties
    and populates the database with them.."""

    weapon_properties = defaultdict(dict)

    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_ARMAS.json") as weapon_file:
            for weapon in load(weapon_file):
                for property_id, property_name in zip(
                    [int(identifier or -1)
                     for identifier in weapon["propiedades"].split("|")],
                        weapon["lista_propiedades"].split("|")):
                    if property_id != -1:
                        weapon_properties[property_id][language] = property_name

    populate_strings("weapon_property", weapon_properties)

    for property_id in weapon_properties.keys():
        if WeaponProperty.get_or_create(
            weapon_property_id=property_id, name=String.get_by_id(
                f"weapon_property_{property_id}"))[1]:
            print(f"Generating entry {property_id} in WeaponProperty table...")


def populate_db(db: SqliteDatabase) -> None:
    """Populates the database tables with the local JSON information."""
    with db as open_db:
        populate_ammo()
        populate_sectorials()
        populate_weapons()


if "infinity.db" not in listdir():
    generate_db(db)
    # TODO: Uncomment this before merging to develop
    # for language in ["ENG", "ESP", "FRA"]:
    #    fetch_json(language)

populate_db(db)
