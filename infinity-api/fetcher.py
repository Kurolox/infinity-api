from requests import get
from json import dumps
from os import mkdir, path


def fetch_json(lang):
    """Attempts to fetch the newest JSON files with the data from all the units in the game.
    Possible lang values: esp, eng"""

    if lang.upper() not in ("ESP", "ENG"):
        raise ValueError(f"The language '{lang}' isn't supported.")

    if not path.exists(f"json_{lang.upper()}"):
        mkdir(f"json_{lang.upper()}")

    for faction in range(100, 1000, 100):
        for sectorial in range(10):
            try:
                request = get(
                    f"https://army.infinitythegame.com/import/json_dataUnidades_{faction+sectorial}_ENG.js")
                if request.status_code == 200:
                    with open(f"json_{lang.upper()}/{faction+sectorial}.json", "w") as open_file:
                        open_file.write(request.text.lstrip(
                            "JSON_UNIDADES = '").rstrip("';").replace("'", "\""))
            except ConnectionError:
                pass

    # TODO: Also fetch https://army.infinitythegame.com/import/idioma_ENG.js items for ID resolution


fetch_json("ESP")
fetch_json("ENG")
