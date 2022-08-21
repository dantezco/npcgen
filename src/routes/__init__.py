"""Module to store all routes"""

from flask import render_template, request
from flask_breadcrumbs import register_breadcrumb
from flask_wtf import FlaskForm
from werkzeug.datastructures import ImmutableMultiDict

from src.flask_app import app
from src.forms import (
    create_char_class_complete_form,
    create_char_class_simple_form,
    create_char_form,
)
from src.mongo.operations import get_char_information, list_available_characters
from src.routes.utils import (
    balance_weights,
    convert_simple_class_data_to_complete,
    create_character,
    create_class,
    list_available_systems,
    list_classes,
    split_form,
)
from src.system import SYSTEMS_ATTRIBUTES


@app.route("/system/<system_name>/class/new/complete", methods=["GET", "POST"])
@register_breadcrumb(app, ".system_name.class", "Create New Class - Complete")
def create_new_class_complete_route(system_name: str):
    """Screen to create a new class -- Complete table"""
    if request.method == "POST":
        form: ImmutableMultiDict[str, str] = request.form
        new_class_id = create_class(system_name=system_name, form=form)
        return f"New class for {system_name} stored with id={new_class_id}"
    fields = SYSTEMS_ATTRIBUTES[system_name]
    form: FlaskForm = create_char_class_complete_form(fields=fields)
    form.fields.data = ",".join(fields)
    return render_template(
        "create_class_complete.html", fields=fields, form=form, system_name=system_name
    )


@app.route("/system/<system_name>/class/new/simple", methods=["GET", "POST"])
@register_breadcrumb(app, ".system_name.class", "Create New Class - Simple")
def create_new_class_simple_route(system_name: str):
    """Screen to create a new class -- Only one row"""
    if request.method == "POST":
        form: ImmutableMultiDict[str, str] = request.form
        complete_form = convert_simple_class_data_to_complete(form)
        new_class_id = create_class(system_name=system_name, form=complete_form)
        return f"New class for {system_name} stored with id={new_class_id}"
    fields = SYSTEMS_ATTRIBUTES[system_name]
    form: FlaskForm = create_char_class_simple_form(fields=fields)
    form.fields.data = ",".join(fields)
    return render_template(
        "create_class_simple.html", fields=fields, form=form, system_name=system_name
    )


@app.route("/system/<system_name>/char/<char_id>")
@register_breadcrumb(app, ".system_name.id", "View Character")
def view_character_route(system_name: str, char_id: str):
    """Screen to view character details"""
    char_info = get_char_information(system_name, char_id)
    return render_template("view_char.html", system_name=system_name, form=char_info)


@app.route("/system/<system_name>/char/new", methods=["GET", "POST"])
@register_breadcrumb(app, ".system_name.char", "Create Character")
def create_character_route(system_name: str):
    """Screen to create a new character"""
    if request.method == "POST":
        form = request.form
        new_char_id = create_character(system_name=system_name, form=form)
        return f"{new_char_id=}"
    newchar_form = create_char_form(system_name=system_name)
    return render_template(
        "create_char.html", system_name=system_name, form=newchar_form
    )


@app.route("/system/<system_name>")
@register_breadcrumb(app, ".system_name", "Choose Character")
def choose_character_route(system_name: str):
    """Screen that lists all characters and allows opening details for one"""
    char_list = list_available_characters(system_name=system_name)
    return render_template(
        "choose_character.html", characters=char_list.items(), system_name=system_name
    )


@app.route("/")
@register_breadcrumb(app, ".", "Home")
def index_screen_route():
    """Index screen, lists all available systems"""
    systems_list = list_available_systems()
    return render_template("index.html", systems=systems_list)
