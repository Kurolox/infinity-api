import requests
from json import dumps


def fetch_json():
    """Attempts to fetch the newest JSON files with the data from all the units in the game."""

    for faction in range(100, 1000, 100):
        for sectorial in range(10):
            try:
                request = requests.get(
                    f"https://army.infinitythegame.com/import/json_dataUnidades_{faction+sectorial}_ENG.js")
                if request.status_code == 200:
                    with open(f"json/{faction+sectorial}.json", "w") as open_file:
                        open_file.write(request.text.lstrip(
                            "JSON_UNIDADES = '").rstrip("';").replace("'", "\""))
            except ConnectionError:
                pass

    #TODO: Also fetch https://army.infinitythegame.com/import/idioma_ENG.js items for ID resolution
    #TODO: Add support for ESP language too
    
fetch_json()
