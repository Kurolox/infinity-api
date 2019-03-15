from db_classes import db, Unit, Weapon, Ammo, Ability, Characteristic, \
    Sectorial, Profile, String, WeaponProperty, Property, ProfileWeapon, \
    ProfileCharacteristic, ProfileAbility, UnitCharacteristic, \
    UnitAbility
from peewee import SqliteDatabase
from json import load
from os import listdir
from collections import defaultdict
from fetcher import fetch_json
from re import findall


def generate_db(db: SqliteDatabase) -> None:
    """Generates all the database tables."""
    with db as open_db:
        open_db.create_tables(
            [Unit, Weapon, Ammo, Ability, Characteristic, Sectorial, Profile,
             String, Property, WeaponProperty, ProfileWeapon,
             ProfileCharacteristic, ProfileAbility,
             UnitCharacteristic, UnitAbility])


def populate_ammo() -> None:
    """Populates the ammo types in it's database table."""

    ammo_dict = defaultdict(dict)

    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_MUNICION.json") as ammo_file:
            for item in load(ammo_file):
                ammo_dict[item["id"]][language] = item["nombre"]

    populate_strings("ammo", ammo_dict)

    print("Generating DB Ammo entries...", end=" ")

    for ammo in ammo_dict.keys():
        Ammo.get_or_create(ammo_id=ammo, name=String.get_by_id(
            f"ammo_{ammo}"))

    print("Done.")


def populate_strings(id_prefix: str, string_dict: tuple) -> None:
    """Generates the strings in the database. It needs a dict of dicts,
    with the key of each dict being the string id in the database,
    and the values being the strings in each language.
    The key of each language has to be the three initials (ENG, ESP, FRA...)"""

    # TODO: Make language recognition automated rather than hardcoded

    print(f"Generating DB String entries for {id_prefix}...", end=" ")

    for string_id, strings in string_dict.items():

        String.get_or_create(
            string_id=f"{id_prefix}_{string_id}",
            english=strings["ENG"] if "ENG" in strings.keys() else None,
            spanish=strings["ESP"] if "ESP" in strings.keys() else None,
            french=strings["FRA"] if "FRA" in strings.keys() else None)

    print("Done.")


def populate_units() -> None:
    """Populates the database with the units and their profiles."""

    strings = defaultdict(dict)

    # 901 sectorial is an outlier that makes everything harder since it doesn't
    # follow any structure, so we blacklist it.
    sectorials = [item.sectorial_id for item in Sectorial.select()
                  if item.sectorial_id != 901]

    for language in listdir("JSON"):
        for sectorial in sectorials:
            with open(f"JSON/{language}/{sectorial}.json") as sectorial_json:
                for unit in load(sectorial_json):
                    for profile in unit["perfiles"]:
                        unit_id = int(profile["id"])
                        strings[unit_id][language] = profile["nombre"]

    populate_strings("unit", strings)

    print("Generating DB Unit entries...", end=" ")

    for sectorial in sectorials:
        file_path = f"JSON/{listdir('JSON')[0]}/{sectorial}.json"
        with open(file_path) as sectorial_json:
            for unit in load(sectorial_json):
                for profile in unit["perfiles"]:
                    unit_id = int(profile["id"])
                    unit_dict = {
                        "unit_id": unit_id,
                        "name": String.get_by_id(f"unit_{unit_id}"),
                        "mov_1": int(profile["atributos"]["MOV1"]),
                        "mov_2": int(profile["atributos"]["MOV2"]),
                        "close_combat": int(profile["atributos"]["CC"]),
                        "ballistic_skill": int(profile["atributos"]["CD"]),
                        "phisique": int(profile["atributos"]["FIS"]),
                        "willpower": int(profile["atributos"]["VOL"]),
                        "armor": int(profile["atributos"]["BLI"]),
                        "bts": int(profile["atributos"]["PB"]),
                        "wounds": int(profile["atributos"]["H"]),
                        "silhouette": int(profile["atributos"]["S"]),
                        "availability": int(profile["atributos"]["Disp"]),
                        "has_structure": bool(int(profile["atributos"]["EST"])),
                        "sectorial": Sectorial.get_by_id(int(unit["idFaccion"])),
                        # TODO: Fix svg_icon to work with non-first profiles
                        "svg_icon": f"https://assets.infinitythegame.net/infinityarmy/img/logos/logos_{sectorial}/logo_{unit['IDArmy']}.svg"
                    }

                    unit_item = Unit.get_or_create(**unit_dict)[0]

                    for characteristic_id in strip_separators(
                            profile["caracteristicas"]):

                        UnitCharacteristic.get_or_create(
                            unit=unit_item,
                            characteristic=Characteristic.get_by_id(
                                characteristic_id))

                    for ability_id in strip_separators(
                            profile["equipo_habs"]):

                        UnitAbility.get_or_create(
                            unit=unit_item, ability=Ability.get_by_id(
                                ability_id))

    print("Done.")

    populate_unit_profiles()


def populate_unit_profiles() -> None:
    """Populates each unit profile in the database."""

    strings = defaultdict(dict)

    # 901 sectorial is an outlier that makes everything harder since it doesn't
    # follow any structure, so we blacklist it.
    sectorials = [item.sectorial_id for item in Sectorial.select()
                  if item.sectorial_id != 901]

    for language in listdir("JSON"):
        for sectorial in sectorials:
            with open(f"JSON/{language}/{sectorial}.json") as sectorial_json:
                for unit in load(sectorial_json):
                    for unit_profile in unit["perfiles"]:
                        for profile in unit_profile["opciones"]:
                            profile_id = int(profile["id"])
                            strings[profile_id][language] = profile["nombre"]

    populate_strings("profile", strings)

    print("Generating DB Profile entries...", end=" ")

    for sectorial in sectorials:
        file_path = f"JSON/{listdir('JSON')[0]}/{sectorial}.json"
        with open(file_path) as sectorial_json:
            for unit in load(sectorial_json):
                for unit_profile in unit["perfiles"]:
                    for profile in unit_profile["opciones"]:
                        profile_id = int(profile["id"])
                        reg, irreg, impetuous = get_orders(profile["ordenes"])
                        profile_dict = {
                            "profile_id": profile_id,
                            "name": String.get_by_id(
                                f"profile_{int(profile['id'])}"),
                            "unit": Unit[int(profile["idPerfil"])],
                            "cap": float(profile["CAP"])
                            if profile["CAP"].replace("-", "") else 0.,
                            "point_cost": int(profile["puntos"]),
                            "regular_orders": reg,
                            "irregular_orders": irreg,
                            "impetuous_orders": impetuous}

                        profile_item = Profile.get_or_create(**profile_dict)[0]

                        for weapon_id in strip_separators(profile["armas"]):
                            ProfileWeapon.get_or_create(
                                weapon=Weapon.get_by_id(weapon_id),
                                profile=profile_item)

                        for characteristic_id in strip_separators(
                                profile["caracteristicas"]):

                            ProfileCharacteristic.get_or_create(
                                characteristic=Characteristic.get_by_id(
                                    characteristic_id), profile=profile_item)

                        for ability_id in strip_separators(profile["extra"]):

                            ProfileAbility.get_or_create(
                                ability=Ability.get_by_id(ability_id),
                                profile=profile_item)

    print("Done.")


def strip_separators(raw_string: str, separator: str = "|") -> tuple:
    """Given a string with numerical values separated by separators, 
    it returns a tuple with it's contents."""

    # TODO: Remove extra replace due to some scenarios where multiple
    # separators are being used at once
    return tuple(
        int(value) for value in findall(r"(\d+)", raw_string)
        if raw_string.strip("|"))


def get_orders(raw_orders: str) -> tuple:
    """Returns a tuple with the orders of an unit. They are, from left to right,
    the regular, irregular, and impetuous orders."""

    orders = [int(order) if int(order) else None
              for order in raw_orders.split("%")]

    return orders[0], orders[1], orders[2]


def populate_sectorials() -> None:
    """Populates the database with the sectorials and their respective ID's."""

    sectorial_dict = defaultdict(dict)

    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_SECTORIAL_NOMBRE.json") as ammo_file:
            for sectorial, name in load(ammo_file)["nombresSectorial"].items():
                sectorial_dict[int(sectorial.lstrip(
                    "idSectorial_"))][language] = name

    populate_strings("sectorial", sectorial_dict)

    print("Generating DB Sectorial entries...", end=" ")

    for sectorial in sectorial_dict.keys():
        Sectorial.get_or_create(
            sectorial_id=sectorial, name=String.get_by_id(
                f"sectorial_{sectorial}"),
            is_faction=True if sectorial % 100 == 1 else False)

    print("Done.")


def populate_weapons() -> None:
    """Populates the weapons and weapon characteristic tables."""

    populate_properties()

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

    print("Generating DB Weapon entries...", end=" ")

    with open(f"JSON/{listdir('JSON')[0]}/JSON_ARMAS.json") as weapon_file:
        # This has to be sorted, otherwise it may attempt to generate weapons
        # with a parent that hasn't been generated yet
        for weapon in sorted(load(weapon_file), key=lambda x: x["parent"]):
            burst_range, burst_melee = calculate_burst(weapon)
            weapon_stats = {
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
                "burst_range": burst_range,
                "burst_melee": burst_melee,
                "parent_weapon": Weapon.get_by_id(int(weapon["parent"]))
                if int(weapon["parent"]) else None}
            db_weapon = Weapon.get_or_create(**weapon_stats)

            properties = [int(prop_id)
                          for prop_id in weapon["propiedades"].split("|")
                          if weapon["propiedades"]]
            for property_id in properties:
                WeaponProperty.get_or_create(
                    weapon=db_weapon[0],
                    weapon_property=Property.get_by_id(property_id))

        print("Done.")


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


def populate_properties() -> None:
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

    populate_strings("property", weapon_properties)

    print("Generating DB Property entries...", end=" ")

    for property_id in weapon_properties.keys():
        Property.get_or_create(
            property_id=property_id, name=String.get_by_id(
                f"property_{property_id}"))

    print("Done.")


def populate_abilities() -> None:
    """Populates the database with the list of abilities."""

    abilities = defaultdict(dict)
    wiki_links = defaultdict(dict)

    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_HABILIDADES.json") as abilities_file:
            for ability in load(abilities_file):
                abilities[ability["id"]][language] = ability["nombre"]

    populate_strings("ability", abilities)

    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_HABS_WIKI_URLS.json") as wiki_file:
            for ability_id, name in load(wiki_file).items():
                wiki_links[int(ability_id)][language] = name

    populate_strings("ability_wiki", wiki_links)

    print("Generating DB Ability entries...", end=" ")

    with open(f"JSON/{listdir('JSON')[0]}/JSON_HABILIDADES.json") as skill_file:
        for ability in load(skill_file):
            ability_id = int(ability["id"])
            ability_breakdown = {
                "ability_id": ability_id, "name": String.get_by_id(
                    f"ability_{ability_id}"),
                "is_item": bool(int(ability["equipo"])),
                "wiki_url": String.get_or_none(
                    String.string_id == f"ability_wiki_{ability_id}")}

            Ability.get_or_create(**ability_breakdown)

    print("Done.")


def populate_characteristics() -> None:
    """Populates the database with the list of characteristics."""

    characteristics = defaultdict(dict)

    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_CARACTERISTICAS.json") as traits_file:
            for item in load(traits_file):
                characteristics[item["id"]][language] = item["nombre"]

    populate_strings("characteristic", characteristics)

    print("Generating DB Characteristic entries...", end=" ")

    for characteristic in characteristics.keys():
        Characteristic.get_or_create(
            characteristic_id=characteristic, name=String.get_by_id(
                f"characteristic_{characteristic}"))

    print("Done.")


def populate_db(db: SqliteDatabase) -> None:
    """Populates the database tables with the local JSON information."""

    db.connect()

    populate_ammo()
    populate_abilities()
    populate_characteristics()
    populate_sectorials()
    populate_weapons()
    populate_units()

    db.close()


if "infinity.db" not in listdir():
    generate_db(db)
    if "JSON" not in listdir():
        for language in ["ENG", "ESP", "FRA"]:
            fetch_json(language)
    populate_db(db)
