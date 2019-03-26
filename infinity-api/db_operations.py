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
        if not session.query(Ammo).get(ammo):
            session.add(
                Ammo(
                    id=ammo,
                    name=session.query(Strings).get(f"ammo_{ammo}")))


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
        if not session.query(Strings).get(string_id):
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
    # populate_abilities()
    # populate_characteristics()
    # populate_sectorials()
    # populate_weapons()
    # populate_units()

    session.commit()
    session.close()


if "infinity.db" not in listdir():
    if "JSON" not in listdir():
        for language in ["ENG", "ESP", "FRA"]:
            fetch_json(language)
    populate_db()
