from requests import get
from json import dumps
from os import mkdir, path
from re import findall
import json


def generate_dict(object_string: str) -> dict:
    """Modifies a JS object and returns a list with all valid python dictionaries on it."""

    object_string = object_string.replace(r"\'", r"\"")
    invalid_chars = ["'", "+", " ", "\n", "\r", "//"]
    for char in invalid_chars:
        object_string = object_string.replace(char, "")

    parsed_string = findall(r"(JSON_\w+)=(.*?[]}]);", object_string)

    return {item[0]: json.loads(item[1]) for item in parsed_string}


def fetch_json(lang: str) -> None:
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
                    f"https://army.infinitythegame.com/import/json_dataUnidades_{faction+sectorial}_{lang.upper()}.js")
                if request.status_code == 200:
                    request_dict = generate_dict(request.text)
                    for content in request_dict.values():
                        with open(f"json_{lang.upper()}/{faction+sectorial}.json", "w") as open_file:
                            print(
                                f"Writting file json_{lang.upper()}/{faction+sectorial}.json")
                            json.dump(content, open_file)
            except ConnectionError:
                print(
                    f"There was an issue trying to establich a connection to the sectorial {faction+sectorial}.")

    try:
        request = get(
            f"https://army.infinitythegame.com/import/idioma_{lang.upper()}.js")
        if request.status_code == 200:
            generate_dict(request.text)

            with open(f"json_{lang.upper()}/{lang.upper()}.json", "w") as open_file:
                open_file.write(request.text.lstrip(
                    "JSON_UNIDADES = '").rstrip("';").replace("'", "\""))
    except ConnectionError:
        print(
            f"There was an issue trying to establich a connection to the core content idioma_{lang.upper()}.")


fetch_json("ESP")
# fetch_json("ENG")
