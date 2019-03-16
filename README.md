# Infinity API
## An open-source API for [Infinity: The Game](https://infinitythegame.com/)

This project's goal is to offer an easily accesible, constantly updated API to all the game data related to the Corvus Belli Wargame, infinity: The Game.

## Features

This API currently provides the following resources:

- All the units in the game, and their different profiles
- All the weapons in the game
- Every ability, ammo type, characteristic and keyword
- Support for all the translated languages (English, Spanish and French)

In addition, since all the data is fetched directly from the [Infinity army builder](https://army.infinitythegame.com/), the data is constantly updated without any need to manually add entries

## Instructions

If you want to run this by yourself, all you have to do is following this steps:

```
git clone https://github.com/Kurolox/infinity-api
cd inginity-api
pipenv install
pipenv run infinity-api/db_operations.py
pipenv run infinity-api/infinity_api.py
```

## Documentation

Here's a link to the [API wiki documentation](https://github.com/Kurolox/infinity-api/wiki).

## Bug reports and feature requests

If you've found a bug or have a feature request, feel free to open an issue in the repository giving all the details possible related to the issue or suggestion at hand.

## License

This project is licensed under the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html).
