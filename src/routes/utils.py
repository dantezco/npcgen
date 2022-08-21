"""Utilitary methods for use in the routes module"""

import os

from werkzeug.datastructures import ImmutableMultiDict

from src.markov.points_generator import MarkovPointsGenerator
from src.mongo.constants import ASSET_CHARACTER_ID
from src.mongo.operations import (
    get_class_information,
    mongo_fetch_collection,
    store_new_asset_to_system,
)
from src.system import NPC_TEMPLATE, SYSTEMS_ATTRIBUTES
from src.system.fnv_tt.charsheet import IDENTIFIER_FNVTT

SYSTEMS_PATH = f"{os.getcwd()}/src/system"


def convert_simple_class_data_to_complete(form: ImmutableMultiDict[str, str]):
    """Converts a simple form data structure to complete form data structure
    Works on the assumption that values for each column are
    equal through all lines of the Markov probability matrix
    If that is not your case, you should use the create complete character"""
    form_weights = split_form(form)
    form_complete_data = {}

    # adds weighted fields to new form dict
    for section in form_weights.items():
        weights = form_weights[section]
        field_labels = list(form_weights[section].keys())
        complete_section = {}
        for label_from in field_labels:
            for label_to in field_labels:
                complete_section[f"{section}_{label_from}_to_{label_to}"] = weights[
                    label_to
                ]
        form_complete_data.update(complete_section)

    # adds other fields to dict
    sections = form["fields"].split(",")
    for key in form:
        if not any(key.startswith(section) for section in sections):
            form_complete_data[key] = form[key]

    return ImmutableMultiDict(form_complete_data)


def split_form(payload: dict) -> dict:
    """Split the payload between two sections"""
    mappings = {}
    sections = payload["fields"].split(",")
    for section in sections:
        mappings[section] = {
            key.removeprefix(f"{section}_"): value
            for key, value in payload.items()
            if key.startswith(section)
        }
    return mappings


def is_system_dir(folder: str):
    """Checks if folder is a valid system under the system folder
    BE AWARE that ALL folders created under system will be considered systems"""
    return os.path.isdir(f"{SYSTEMS_PATH}/{folder}") and not folder.startswith("_")


def list_available_systems() -> list[str]:
    """Creates a list based on folder structure under system folder"""
    available_systems = [
        folder for folder in os.listdir(SYSTEMS_PATH) if is_system_dir(folder)
    ]
    return available_systems


def balance_weights(system_name: str, weights: dict) -> dict:
    """Redistributes leftover probabilitie 1 - sum(weights) between nulled nodes"""
    balanced_weights = {}
    for section in weights:
        payload = weights[section]
        payload.update({"fields": SYSTEMS_ATTRIBUTES[system_name][section]})
        graph = MarkovPointsGenerator(payload=payload)  # rename payload
        balanced_weights[section] = graph.create_chain()
    return balanced_weights


def list_classes(system_name: str) -> list:
    """Builds a list with all classes names available for system"""
    collection = "classes"
    classes_collection = mongo_fetch_collection(
        system_name=system_name, collection=collection
    )
    return [char_class["class_name"] for char_class in classes_collection]


def create_character(system_name: str, form: ImmutableMultiDict[str, str]) -> int:
    """Creates a new character for system_name based on data from form"""
    char_class = form["char_class"]
    level = int(form["level"])
    class_information = get_class_information(
        system_name=IDENTIFIER_FNVTT, class_name=char_class
    )
    new_char = NPC_TEMPLATE[system_name](
        class_name=char_class, level=level, class_information=class_information
    )
    serialized_char = new_char.serialize()
    new_char_id = store_new_asset_to_system(
        new_class=serialized_char,
        system_name=system_name,
        asset_type=ASSET_CHARACTER_ID,
    )
    return new_char_id


def create_class(system_name: str, form: ImmutableMultiDict[str, str]) -> int:
    """Creates a new class for system_name based on data from form"""
    weights = split_form(form)
    balanced_weights = balance_weights(system_name=system_name, weights=weights)
    new_class = {
        "probabilities": balanced_weights,
        "class_name": form["class_name"],
    }
    new_class_id = store_new_asset_to_system(
        new_class=new_class, system_name=system_name, asset_type="classes"
    )
    return new_class_id
