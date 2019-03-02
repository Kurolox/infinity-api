from db_manager import db
from db_classes import Unit, Weapon, Ammo, Ability, Characteristic, Faction, Sectorial, Profile


def generate_db() -> None:
    """Generates all the database tables."""
    db.connect()

    db.create_tables([Unit, Weapon, Ammo, Ability,
                      Characteristic, Faction, Sectorial, Profile])

generate_db()