"""Main class of the project"""
import os

from flask import Flask, render_template, request, url_for
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

from src.forms.markov import ChooseAttributesForm, create_dynamic_form
from src.markov.parser import MarkovModel
from src.system.charsheet import Charsheet, FNVTT_ATTRIBUTES

app = Flask(__name__)
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'


@app.route("/choose_section", methods=["GET", "POST"])
def choose_section():
    """Where the user chooses the attributes to generate the markov chain"""
    form = ChooseAttributesForm()
    if form.validate_on_submit():
        print(form)
        return form
    return render_template('choose_section.html', form=form, template="form-template")


@app.route("/markov_input", methods=["GET", "POST"])
def markov_input():
    """Markov graph definition screen"""
    if len(request.form) > 0:
        fields = request.form["choices"][2:-2].split("', '")
        form = create_dynamic_form(fields=fields)
        form.fields.data = ",".join(fields)
        return render_template("markov_input.html", fields=fields, form=form)
    return "You should not be seeing this"


@app.route("/results", methods=["GET", "POST"])
def process_input():
    form = request.form
    parser = MarkovModel(payload=form)
    result = parser.process_form()
    return f"{str(result)}<br><br>{form['class_name']}"


"""Next steps
STORE NEWLY CREATED CLASS
LIST ALL AVAILABLE CLASSES, BUTTONS TO EDIT OR CREATE NEW CHARACTER OF CHOSEN CLASS
CREATE NEW CHARACTER SCREEN - GENERATE MARKOV STUFF, DISPLAY WITH FIELDS FOR OTHER THINGS, LIKE NAME AND STUFF
"""

@app.route("/")
def test_screen():
    """Sample path function"""
    charsheet = Charsheet(system_name="fnv_tt")
    return str(charsheet.system_name)


def create_app():
    app.run(host="0.0.0.0", port=5000, debug=os.getenv("FLASK_ENV") == "dev")
