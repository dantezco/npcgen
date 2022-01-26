"""Main class of the project"""
import os

from flask import Flask, render_template, request, url_for
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

from src.forms.markov import ChooseAttributesForm, create_dynamic_form
from src.system.charsheet import Charsheet, FNVTT_ATTRIBUTES

app = Flask(__name__)
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'


@app.route("/mc", methods=["GET", "POST"])
def markov_choose():
    form = ChooseAttributesForm()
    if form.validate_on_submit():
        print(form)
        return form
    return render_template('markov_choose.html', form=form, template="form-template")


@app.route("/mi", methods=["GET", "POST"])
def markov_input():
    """Sample path function"""
    if len(request.form) > 0:
        fields = request.form["choices"][2:-2].split("', '")
        form = create_dynamic_form(fields=fields)
        return render_template("markov_input.html", fields=fields, form=form)
    return "You should not be seeing this"

@app.route("/results", methods=["GET", "POST"])
def print_markov():
    form = request.form
    return form

@app.route("/")
def test_screen():
    """Sample path function"""
    charsheet = Charsheet(system_name="fnv_tt")
    return str(charsheet.system_name)


def create_app():
    app.run(host="0.0.0.0", port=5000, debug=os.getenv("FLASK_ENV") == "dev")
