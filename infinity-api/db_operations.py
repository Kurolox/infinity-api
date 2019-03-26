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

    print("Generating DB Ability entries...", end=" ")

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

    print("Done.")


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
    # populate_characteristics()
    # populate_sectorials()
    # populate_weapons()
    # populate_units()

    session.commit()
    session.close()


if "JSON" not in listdir():
    for language in ["ENG", "ESP", "FRA"]:
        fetch_json(language)
populate_db()
