"""Collection of functions to manipulate Mongo"""
import pymongo
from bson.objectid import ObjectId
from pymongo import MongoClient

from src.mongo.constants import COLLECTION_CHARACTERS, COLLECTION_CLASSES


def mongo_fetch_collection(system_name: str, collection: str) -> list:
    """Retrieves a collection from the database for given system"""
    mongo = pymongo.MongoClient()
    collection_data = mongo[system_name][collection].find({}, None)
    processed_data = []
    for line in collection_data:
        processed_data.append(line)
    return processed_data


def list_available_classes(system_name: str) -> list:
    """Lists all available Markov mappings for system"""
    mongo = pymongo.MongoClient()
    classes = [
        collection["class_name"]
        for collection in mongo[system_name].get_collection(COLLECTION_CLASSES).find({})
    ]
    return classes


def list_available_characters(system_name: str) -> dict:
    """Lists all IDs of available characters for system"""
    mongo = pymongo.MongoClient()
    classes = {
        collection["_id"]: collection["name"]
        for collection in mongo[system_name]
        .get_collection(COLLECTION_CHARACTERS)
        .find({})
    }
    return classes


def get_class_information(system_name: str, class_name: str) -> dict:
    """Gets all information regarding a class from system"""
    mongo = pymongo.MongoClient()
    char_class = (
        mongo[system_name]
        .get_collection(COLLECTION_CLASSES)
        .find_one({"class_name": class_name}, None)
    )
    return char_class


def get_char_information(system_name: str, char_id: str) -> dict:
    """Gets all information regarding a character from system"""
    mongo = pymongo.MongoClient()
    character = (
        mongo[system_name]
        .get_collection(COLLECTION_CHARACTERS)
        .find_one({"_id": ObjectId(char_id)}, None)
    )
    return character


def store_new_asset_to_system(
    new_class: dict, system_name: str, asset_type: str
) -> int:
    """Writes a new asset to Mongodb"""
    mongo = MongoClient()
    new_item_id = mongo[system_name][asset_type].insert_one(new_class).inserted_id
    return new_item_id
