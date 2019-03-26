from sqlalchemy import create_engine, Table, Column, String, Integer, Float,\
    ForeignKey, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db = create_engine("sqlite:///infinity.db")
BaseModel = declarative_base()
Session = sessionmaker(db)

profileweapon = Table(
    "profile_weapons", BaseModel.metadata,
    Column(
        "profile_id", Integer, ForeignKey("profiles.id"),
        primary_key=True),
    Column(
        "weapon_id", Integer, ForeignKey("weapons.id"),
        primary_key=True))

weaponproperty = Table(
    "weapon_properties", BaseModel.metadata,
    Column(
        "weapon_id", Integer, ForeignKey("weapons.id"),
        primary_key=True),
    Column(
        "property_id", Integer, ForeignKey("properties.id"),
        primary_key=True))

profilecharacteristic = Table(
    "profile_characteristics", BaseModel.metadata,
    Column(
        "profile_id", Integer, ForeignKey("profiles.id"),
        primary_key=True),
    Column(
        "characteristic_id", Integer, ForeignKey("characteristics.id"),
        primary_key=True))

profileability = Table(
    "profile_abilities", BaseModel.metadata,
    Column(
        "profile_id", Integer, ForeignKey("profiles.id"),
        primary_key=True),
    Column(
        "ability_id", Integer, ForeignKey("abilities.id"),
        primary_key=True))

unitability = Table(
    "unit_abilities", BaseModel.metadata,
    Column(
        "unit_id", Integer, ForeignKey("units.id"),
        primary_key=True),
    Column(
        "ability_id", Integer, ForeignKey("abilities.id"),
        primary_key=True))

unitcharacteristic = Table(
    "unit_characteristics", BaseModel.metadata,
    Column(
        "unit_id", Integer, ForeignKey("units.id"),
        primary_key=True),
    Column(
        "characteristic_id", Integer, ForeignKey("characteristics.id"),
        primary_key=True))


class Strings(BaseModel):
    """This class stores all the strings in their respective languages."""

    __tablename__ = "strings"

    id = Column(String, primary_key=True)
    spanish = Column(String)
    english = Column(String)
    french = Column(String)


class Ammo(BaseModel):
    """This class stores the ammunition types."""

    __tablename__ = "ammo"

    id = Column(Integer, primary_key=True)
    name_id = Column(ForeignKey(Strings.id))

    name = relationship("Strings")
    weapons = relationship("Weapon")


class Sectorial(BaseModel):
    """This class stores the sectorials and factions in the game."""

    __tablename__ = "sectorials"

    id = Column(Integer, primary_key=True)
    name_id = Column(ForeignKey(Strings.id))
    is_faction = Column(Boolean)

    name = relationship("Strings")
    units = relationship("Unit")


class Ability(BaseModel):
    """This class stores all the abilities (and wiki URLs, if any)."""

    __tablename__ = "abilities"

    id = Column(Integer, primary_key=True)
    name_id = Column(ForeignKey(Strings.id))
    is_item = Column(Boolean)
    wiki_url = Column(String)

    name = relationship("Strings")
    profiles = relationship(
        "Profile", secondary=profileability, back_populates="abilities")
    units = relationship("Unit", secondary=unitability,
                         back_populates="abilities")


class Characteristic(BaseModel):
    """This class stores all the characteristics."""

    __tablename__ = "characteristics"

    id = Column(Integer, primary_key=True)
    name_id = Column(ForeignKey(Strings.id))

    name = relationship("Strings")
    profiles = relationship(
        "Profile", secondary=profilecharacteristic,
        back_populates="characteristics")
    units = relationship("Unit", secondary=unitcharacteristic,
                         back_populates="characteristics")


class Unit(BaseModel):
    """This class stores all the units, their stats and their SVG URL."""

    __tablename__ = "units"

    id = Column(Integer, primary_key=True)
    name_id = Column(ForeignKey(Strings.id))
    sectorial_id = Column(ForeignKey(Sectorial.id))
    svg_icon = Column(String)
    mov_1 = Column(Integer)
    mov_2 = Column(Integer)
    close_combat = Column(Integer)
    ballistic_skill = Column(Integer)
    phisique = Column(Integer)
    willpower = Column(Integer)
    armor = Column(Integer)
    bts = Column(Integer)
    wounds = Column(Integer)
    silhouette = Column(Integer)
    availability = Column(Integer)
    has_structure = Column(Boolean)

    name = relationship("Strings")
    sectorial = relationship("Sectorial", back_populates="units")
    profiles = relationship("Profile")
    abilities = relationship(
        "Ability", secondary=unitability, back_populates="units")
    characteristics = relationship("Characteristic",
                                   secondary=unitcharacteristic,
                                   back_populates="units")


class Profile(BaseModel):
    """This class stores all the profiles of each unit."""

    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    unit_id = Column(ForeignKey(Unit.id))
    name_id = Column(ForeignKey(Strings.id))
    # linked_units = ForeignKeyField(Unit, null=True, backref="linked_units")
    # linked_units = Column(ForeignKey(Unit.id))
    cap = Column(Float)
    point_cost = Column(Integer)
    regular_orders = Column(Integer)
    irregular_orders = Column(Integer)
    impetuous_orders = Column(Integer)

    unit = relationship("Unit", back_populates="profiles")
    name = relationship("Strings")
    weapons = relationship(
        "Weapon", secondary=profileweapon, back_populates="profiles")
    characteristics = relationship(
        "Characteristic", secondary=profilecharacteristic,
        back_populates="profiles")
    abilities = relationship(
        "Ability", secondary=profileability, back_populates="profiles")


class Weapon(BaseModel):
    """This class stores all the weapons and their stats."""

    __tablename__ = "weapons"

    id = Column(Integer, primary_key=True)
    damage = Column(String)
    name_id = Column(ForeignKey(Strings.id))
    ammo_id = Column(ForeignKey(Ammo.id))
    parent_weapon_id = Column(ForeignKey("weapons.id"))
    is_melee = Column(Boolean)
    short_range = Column(String)
    medium_range = Column(String)
    long_range = Column(String)
    maximum_range = Column(String)
    burst_melee = Column(Integer)
    burst_range = Column(Integer)

    name = relationship("Strings")
    ammo = relationship("Ammo", back_populates="weapons")
    parent_weapon = relationship("Weapon", remote_side=id)
    profiles = relationship(
        "Profile", secondary=profileweapon, back_populates="weapons")
    properties = relationship(
        "Property", secondary=weaponproperty, back_populates="weapons")


class Property(BaseModel):
    """This class stores all the weapon properties."""

    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    name_id = Column(ForeignKey(Strings.id))

    name = relationship("Strings")
    weapons = relationship(
        "Weapon", secondary=weaponproperty, back_populates="properties")


BaseModel.metadata.create_all(db)
