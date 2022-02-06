"""Main class of the project"""
from flask import render_template, request
from pymongo import MongoClient

from src.flask_app import app
from src.forms.markov import create_markov_mapping_form
from src.routes.utils import list_available_characters, build_systems_list, store_new_class, split_form, balance_weights
from src.system import SYSTEMS_ATTRIBUTES


@app.route("/system/<system_name>/class/new/process", methods=["GET", "POST"])
def process_new_class(system_name: str):
    form = request.form
    weights = split_form(form)
    balanced_weights = balance_weights(system_name=system_name, weights=weights)
    new_class = {
        "probabilities": balanced_weights,
        "class_name": form["class_name"],
    }
    new_class_id = store_new_class(new_class=new_class, system_name=system_name)
    return f"New class {new_class} stored with id={new_class_id}"


@app.route("/system/<system_name>/class/new", methods=["GET", "POST"])
def create_new_class(system_name: str):
    """Screen to create a new class"""
    fields = SYSTEMS_ATTRIBUTES[system_name]
    form = create_markov_mapping_form(fields=fields)
    form.fields.data = ",".join(fields)
    return render_template("markov_input.html", fields=fields, form=form, system_name=system_name)


@app.route("/system/<system_name>/npc/<index>")
def view_character(system_name: str, index: int):
    return f'{system_name} -> {index}'


@app.route("/system/<system_name>")
def choose_character(system_name: str):
    char_list = list_available_characters(system_name=system_name)
    return render_template("choose_character.html", characters=char_list, system_name=system_name)


@app.route("/")
def index_screen():
    """Sample path function"""
    systems_list = build_systems_list()
    return render_template("index.html", systems=systems_list)
