from flask import Flask
from flask_restplus import Resource, Api
from playhouse.shortcuts import model_to_dict
from db_classes import db, Unit, Weapon, Ammo, Ability, Characteristic, \
    Sectorial, Profile, String, WeaponProperty, Property, ProfileWeapon, \
    ProfileCharacteristic, ProfileAbility, UnitCharacteristic, \
    UnitAbility


app = Flask(__name__)
api = Api(app)


@api.route('/unit/<int:unit_id>')
class ReturnUnit(Resource):
    def get(self, unit_id):
        try:
            unit = Unit[unit_id]
        except Unit.DoesNotExist:
            return "Unit not found", 404
        return model_to_dict(Unit[unit_id])


@api.route('/unit')
class ReturnAllUnits(Resource):
    def get(self):
        units = {}
        for unit in Unit.select():
            units[unit.unit_id] = model_to_dict(unit)
        return units


if __name__ == '__main__':
    app.run()
