from requests import get
from os import mkdir, path
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

    # TODO: Change paths and don't store data in .json when the db is set up
    if not path.exists(file_path):
        mkdir(file_path)

    try:
        request = get(url)
        if request.status_code == 200:
            request_dict = generate_dict(request.text)
            for item, content in request_dict.items():
                with open(f"{file_path}/{file_name or item}.json", "w") as open_file:
                    print(
                        f"Writting file {file_path}/{file_name or item}.json...")
                    json.dump(content, open_file, sort_keys=True,
                              indent=4, separators=(',', ': '))
    except ConnectionError:
        print(f"There was an issue trying to fetch the url {url}.")


def fetch_json(lang: str) -> None:
    """Attempts to fetch the newest JSON files with the data from all the units in the game.
    Possible lang values: esp, eng"""

    if lang.upper() not in ("ESP", "ENG"):
        raise ValueError(f"The language '{lang}' isn't supported.")

    store_remote_data(
        f"https://army.infinitythegame.com/import/idioma_{lang.upper()}.js",
        file_path=lang.upper())

    for faction in range(100, 1000, 100):
        for sectorial in range(10):
            store_remote_data(
                f"https://army.infinitythegame.com/import/json_dataUnidades_{faction + sectorial}_{lang.upper()}.js",
                file_name=str(faction + sectorial),
                file_path=lang.upper())


fetch_json("ESP")
fetch_json("ENG")
