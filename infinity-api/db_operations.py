from db_classes import Session, Strings, Ammo, Unit, Profile, Ability,\
    Characteristic, Weapon, Sectorial, Property
from json import load
from os import listdir
from collections import defaultdict
from fetcher import fetch_json
from re import findall


def populate_ammo(session: Session) -> None:
    """Populates the ammo types in it's database table."""

    ammo_dict = defaultdict(dict)

    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_MUNICION.json") as ammo_file:
            for item in load(ammo_file):
                ammo_dict[item["id"]][language] = item["nombre"]

    populate_strings("ammo", ammo_dict, session)

    print("Generating DB Ammo entries...")

    for ammo in ammo_dict.keys():
        if session.query(Ammo).get(ammo):
            continue

        session.add(
            Ammo(id=ammo, name=session.query(Strings).get(f"ammo_{ammo}")))


def populate_abilities(session: Session) -> None:
    """Populates the database with the list of abilities."""

    abilities = defaultdict(dict)
    wiki_links = defaultdict(dict)

    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_HABILIDADES.json") as abilities_file:
            for ability in load(abilities_file):
                abilities[ability["id"]][language] = ability["nombre"]

    populate_strings("ability", abilities, session)

    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_HABS_WIKI_URLS.json") as wiki_file:
            for ability_id, name in load(wiki_file).items():
                wiki_links[int(ability_id)][language] = name

    populate_strings("ability_wiki", wiki_links, session)

    print("Generating DB Ability entries...")

    with open(f"JSON/{listdir('JSON')[0]}/JSON_HABILIDADES.json") as skill_file:
        for ability in load(skill_file):
            ability_id = int(ability["id"])

            if session.query(Ability).get(ability_id):
                continue

            data = {
                "id": ability_id,
                "name": session.query(Strings).get(f"ability_{ability_id}"),
                "is_item": bool(int(ability["equipo"])),
                "wiki_url": session.query(Strings).get(
                    f"ability_wiki_{ability_id}")}

            session.add(Ability(**data))


def populate_characteristics(session: Session) -> None:
    """Populates the database with the list of characteristics."""

    characteristics = defaultdict(dict)

    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_CARACTERISTICAS.json") as traits_file:
            for item in load(traits_file):
                characteristics[item["id"]][language] = item["nombre"]

    populate_strings("characteristic", characteristics, session)

    print("Generating DB Characteristic entries...")

    for characteristic in characteristics.keys():
        if session.query(Characteristic).get(characteristic):
            continue

        session.add(
            Characteristic(
                id=characteristic,
                name=session.query(Strings).get(
                    f"characteristic_{characteristic}")))


def populate_sectorials(session: Session) -> None:
    """Populates the database with the sectorials and their respective ID's."""

    sectorial_dict = defaultdict(dict)

    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_SECTORIAL_NOMBRE.json") as ammo_file:
            for sectorial, name in load(ammo_file)["nombresSectorial"].items():
                sectorial_dict[int(sectorial.lstrip(
                    "idSectorial_"))][language] = name

    populate_strings("sectorial", sectorial_dict, session)

    print("Generating DB Sectorial entries...")

    for sectorial in sectorial_dict.keys():

        if session.query(Sectorial).get(sectorial):
            continue

        session.add(
            Sectorial(
                id=sectorial, name=session.query(Strings).get(
                    f"sectorial_{sectorial}"),
                is_faction=True if sectorial % 100 == 1 else False))


def populate_weapons(session: Session) -> None:
    """Populates the weapons and weapon characteristic tables."""

    populate_properties(session)

    weapon_dict = defaultdict(dict)

    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_ARMAS.json") as weapon_file:
            for weapon in load(weapon_file):
                weapon_dict[int(weapon["id"])
                            ][language] = weapon["nombre_completo"]

    populate_strings("weapon", weapon_dict, session)

    weapon_wiki_dict = defaultdict(dict)
    for language in listdir("JSON"):
        with open(f"JSON/{language}/JSON_ARMAS_WIKI_URLS.json") as weapon_wiki:
            for weapon_id, weapon_wiki_link in load(weapon_wiki).items():
                weapon_wiki_dict[int(weapon_id)][language] = weapon_wiki_link

    populate_strings("weapon_wiki", weapon_wiki_dict, session)

    print("Generating DB Weapon entries...")

    with open(f"JSON/{listdir('JSON')[0]}/JSON_ARMAS.json") as weapon_file:
        # This has to be sorted, otherwise it may attempt to generate weapons
        # with a parent that hasn't been generated yet
        for weapon in sorted(load(weapon_file), key=lambda x: x["parent"]):
            weapon_id = int(weapon["id"])

            if session.query(Weapon).get(weapon_id):
                continue

            burst_range, burst_melee = calculate_burst(weapon)
            weapon_stats = {
                "id": weapon_id,
                # TODO: Correct damage language by using JSON_ATRIBUTOS_ROT
                "damage": weapon["dano"],
                "name": session.query(Strings).get(f"weapon_{weapon['id']}"),
                "is_melee": True if weapon["CC"] == "1" else False,
                "short_range": validate_range(weapon["corta"]),
                "medium_range": validate_range(weapon["media"]),
                "long_range": validate_range(weapon["larga"]),
                "maximum_range": validate_range(weapon["maxima"]),
                "ammo": session.query(Ammo).get(int(weapon["idMunicion"])),
                "burst_range": burst_range,
                "burst_melee": burst_melee,
                "parent_weapon": session.query(Weapon).get(int(weapon["parent"]))}

            weapon_object = Weapon(**weapon_stats)

            properties = [int(prop_id)
                          for prop_id in weapon["propiedades"].split("|")
                          if weapon["propiedades"]]

            weapon_object.properties = [
                session.query(Property).get(property_id)
                for property_id in properties]

            session.add(weapon_object)


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


def populate_properties(session: Session) -> None:
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

    populate_strings("property", weapon_properties, session)

    print("Generating DB Property entries...", end=" ")

    for property_id in weapon_properties.keys():
        if session.query(Property).get(property_id):
            continue

        session.add(Property(id=property_id, name=session.query(Strings).get(
            f"property_{property_id}")))

    print("Done.")


def populate_units(session: Session) -> None:
    """Populates the database with the units and their profiles."""

    strings = defaultdict(dict)

    # 901 sectorial is an outlier that makes everything harder since it doesn't
    # follow any structure, so we blacklist it.
    sectorials = [sectorial.id for sectorial in session.query(Sectorial)
                  if sectorial.id != 901]

    for language in listdir("JSON"):
        for sectorial in sectorials:
            with open(f"JSON/{language}/{sectorial}.json") as sectorial_json:
                for unit in load(sectorial_json):
                    for profile in unit["perfiles"]:
                        unit_id = int(profile["id"])
                        strings[unit_id][language] = profile["nombre"]

    populate_strings("unit", strings, session)

    print("Generating DB Unit entries...")

    for sectorial in sectorials:
        file_path = f"JSON/{listdir('JSON')[0]}/{sectorial}.json"
        with open(file_path) as sectorial_json:
            for unit in load(sectorial_json):
                for profile in unit["perfiles"]:
                    unit_id = int(profile["id"])

                    if session.query(Unit).get(unit_id):
                        continue

                    unit_dict = {
                        "id": unit_id,
                        "name": session.query(Strings).get(f"unit_{unit_id}"),
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
                        "sectorial": session.query(Sectorial).get(int(unit["idFaccion"])),
                        # TODO: Fix svg_icon to work with non-first profiles
                        "svg_icon": f"https://assets.infinitythegame.net/infinityarmy/img/logos/logos_{sectorial}/logo_{unit['IDArmy']}.svg"
                    }

                    unit_item = Unit(**unit_dict)

                    for characteristic_id in strip_separators(
                            profile["caracteristicas"]):

                        unit_item.characteristics.append(
                            session.query(Characteristic).get(characteristic_id))

                    for ability_id in strip_separators(
                            profile["equipo_habs"]):

                        unit_item.abilities.append(
                            session.query(Ability).get(ability_id))

                    session.add(unit_item)

    populate_unit_profiles(session)


def populate_unit_profiles(session: Session) -> None:
    """Populates each unit profile in the database."""

    strings = defaultdict(dict)

    # 901 sectorial is an outlier that makes everything harder since it doesn't
    # follow any structure, so we blacklist it.
    sectorials = [sectorial.id for sectorial in session.query(Sectorial)
                  if sectorial.id != 901]

    for language in listdir("JSON"):
        for sectorial in sectorials:
            with open(f"JSON/{language}/{sectorial}.json") as sectorial_json:
                for unit in load(sectorial_json):
                    for unit_profile in unit["perfiles"]:
                        for profile in unit_profile["opciones"]:
                            profile_id = int(profile["id"])
                            strings[profile_id][language] = profile["nombre"]

    populate_strings("profile", strings, session)

    print("Generating DB Profile entries...")

    for sectorial in sectorials:
        file_path = f"JSON/{listdir('JSON')[0]}/{sectorial}.json"
        with open(file_path) as sectorial_json:
            for unit in load(sectorial_json):
                for unit_profile in unit["perfiles"]:
                    for profile in unit_profile["opciones"]:
                        profile_id = int(profile["id"])

                        if session.query(Profile).get(profile_id):
                            continue

                        reg, irreg, impetuous = get_orders(profile["ordenes"])
                        name_id = f"profile_{profile['id']}"
                        profile_dict = {
                            "id": profile_id,
                            "name": session.query(Strings).get(name_id),
                            "unit": session.query(Unit).get(int(profile["idPerfil"])),
                            "cap": float(profile["CAP"])
                            if profile["CAP"].replace("-", "") else 0.,
                            "point_cost": int(profile["puntos"]),
                            "regular_orders": reg,
                            "irregular_orders": irreg,
                            "impetuous_orders": impetuous}

                        profile_item = Profile(**profile_dict)

                        for weapon_id in strip_separators(profile["armas"]):
                            weapon_item = session.query(Weapon).get(weapon_id)
                            if weapon_item not in profile_item.weapons:
                                profile_item.weapons.append(weapon_item)

                        for characteristic_id in strip_separators(
                                profile["caracteristicas"]):
                            char_item = session.query(Characteristic).get(
                                characteristic_id)
                            if char_item not in profile_item.characteristics:
                                profile_item.characteristics.append(char_item)

                        for ability_id in strip_separators(profile["extra"]):
                            ability_item = session.query(
                                Ability).get(ability_id)
                            if ability_item not in profile_item.abilities:
                                profile_item.abilities.append(ability_item)

                        session.add(profile_item)


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


def populate_strings(
        id_prefix: str, string_dict: tuple, session: Session) -> None:
    """Generates the strings in the database. It needs a dict of dicts,
    with the key of each dict being the string id in the database,
    and the values being the strings in each language.
    The key of each language has to be the three initials (ENG, ESP, FRA...)"""

    # TODO: Make language recognition automated rather than hardcoded

    print(f"Generating DB String entries for {id_prefix}...")

    for numeric_id, strings in string_dict.items():
        string_id = f"{id_prefix}_{numeric_id}"
        if session.query(Strings).get(string_id):
            continue
        session.add(Strings(
            id=string_id,
            english=strings["ENG"] if "ENG" in strings.keys() else None,
            spanish=strings["ESP"] if "ESP" in strings.keys() else None,
            french=strings["FRA"] if "FRA" in strings.keys() else None)
        )


def populate_db() -> None:
    """Populates the database tables with the local JSON information."""

    session = Session()

    populate_ammo(session)
    populate_abilities(session)
    populate_characteristics(session)
    populate_sectorials(session)
    populate_weapons(session)
    populate_units(session)

    session.commit()
    session.close()


if "JSON" not in listdir():
    for language in ["ENG", "ESP", "FRA"]:
        fetch_json(language)
populate_db()

