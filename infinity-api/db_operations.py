from db_manager import db
from db_classes import Unit, Weapon, Ammo, Ability, Characteristic, Faction, Sectorial, Profile, String
from peewee import SqliteDatabase
from json import load
from os import listdir


def generate_db(db: SqliteDatabase) -> None:
    """Generates all the database tables."""
    with db as open_db:
        open_db.create_tables(
            [Unit, Weapon, Ammo, Ability, Characteristic, Faction, Sectorial,
             Profile, String])


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

    # TODO: Remove hardcoded languages and make it depend on the String defined languages only
    String.bulk_create(
        tuple(String(
            string_id=f"ammo_{ammo_id}", english=ammo["ENG"],
            spanish=ammo["ESP"], french=ammo["FRA"])
            for ammo_id, ammo in ammo_dict.items()))


def populate_db(db: SqliteDatabase) -> None:
    """Populates the database tables with the local JSON information."""
    with db as open_db:
        populate_ammo(open_db)


generate_db(db)
populate_db(db)
