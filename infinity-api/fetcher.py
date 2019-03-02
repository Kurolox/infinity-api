from requests import get
from pathlib import Path
from re import findall
import json


def generate_dict(object_string: str) -> dict:
    """Modifies a JS object and returns a list with all valid python dictionaries on it."""

    object_string = object_string.replace(r"\'", r"\"")
    invalid_chars = ["'", "+", "\n", "\r", "//"]
    for char in invalid_chars:
        object_string = object_string.replace(char, "")

    parsed_string = findall(r"(JSON_\w+)\s?=\s?(.*?[]}]);", object_string)
    with open("debug.txt", "w") as my_file:
        my_file.write(object_string)

    return {item[0]: json.loads(item[1]) for item in parsed_string}


def store_remote_data(
        url: str, file_name: str = "", file_path: str = "") -> None:
    """Given an URL with a series of JS objects, it will attempt to fetch them and store them locally as JSON."""

    # TODO: Async requests to fetch multiple JSON?
    request = get(url)
    if request.status_code != 200:
        raise ConnectionError

    # TODO: Change paths and don't store data in .json when the db is set up
    Path(file_path).mkdir(parents=True, exist_ok=True)

    request_dict = generate_dict(request.text)
    for item, content in request_dict.items():
        with open(f"{file_path}/{file_name or item}.json", "w") as open_file:
            print(f"Writting file {file_path}/{file_name or item}.json...")
            json.dump(content, open_file, sort_keys=True,
                      indent=4, separators=(',', ': '))


def fetch_sectorial_list(path: str) -> tuple:
    """Returns a tuple with all the IDs of every sectorial.
    The data is read from the locally stored JSON folder passed as argument."""

    with open(f"{path}/JSON_SECTORIAL_NOMBRE.json", "r") as local_json_file:
        return tuple(int(sectorial.split("_")[-1])
                     for sectorial in json.load(local_json_file)
                     ["nombresSectorial"].keys())


def fetch_json(lang: str) -> None:
    """Attempts to fetch the newest JSON files with the data from all the units in the game.
    Possible lang values: esp, eng"""

    try:
        store_remote_data(
            f"https://army.infinitythegame.com/import/idioma_{lang.upper()}.js",
            file_path=f"JSON/{lang.upper()}")

    except ConnectionError:
        print(
            f"There was an issue trying to connect to the URL https://army.infinitythegame.com/import/idioma_{lang.upper()}.js.")
        return

    for sectorial in fetch_sectorial_list(lang.upper()):
        store_remote_data(
            f"https://army.infinitythegame.com/import/json_dataUnidades_{sectorial}_{lang.upper()}.js",
            file_name=str(sectorial),
            file_path=f"JSON/{lang.upper()}")


fetch_json("ESP")
fetch_json("ENG")
fetch_json("FRA")
