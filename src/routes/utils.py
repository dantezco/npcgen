import json
import os

from pymongo import MongoClient
from werkzeug.datastructures import ImmutableMultiDict

from src.markov.parser import MarkoProbabilityMap
from src.system import SYSTEMS_ATTRIBUTES

SYSTEMS_PATH = f"{os.getcwd()}/src/system"


def list_available_characters(system_name: str) -> enumerate:
    with open(f"{SYSTEMS_PATH}/{system_name}/characters.json", "r") as char_file:
        characters = json.load(char_file)
    return enumerate([npc["name"] for npc in characters["npcs"]])


def split_form(payload: dict) -> dict:
    mappings = {}
    sections = payload["fields"].split(',')
    for section in sections:
        mappings[section] = {key.removeprefix(f"{section}_"): value for key, value in payload.items() if key.startswith(section)}
    return mappings


def is_system_dir(folder: str):
    return os.path.isdir(f"{SYSTEMS_PATH}/{folder}") and not folder.startswith("_")


def build_systems_list() -> list[str]:
    available_systems = [folder for folder in os.listdir(SYSTEMS_PATH) if is_system_dir(folder)]
    return available_systems


def store_new_class(new_class: dict, system_name: str) -> int:
    db = MongoClient()
    return db[system_name]["classes"].insert_one(new_class).inserted_id


def balance_weights(system_name: str, weights: dict) -> dict:
    balanced_weights = {}
    for section in weights:
        payload = weights[section]
        payload.update({"fields": SYSTEMS_ATTRIBUTES[system_name][section]})
        graph = MarkoProbabilityMap(payload=payload) #rename payload
        balanced_weights[section] = graph.balance_weights()
    return balanced_weights