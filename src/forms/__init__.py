"""Form Objects declaration"""

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    FloatField,
    HiddenField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
)

from src.mongo.operations import list_available_classes


def create_char_class_simple_form(fields: list) -> FlaskForm:
    """Creates a dynamic character class form for Flask,
    based on the attributes listed under <system_name>/charsheet.py"""

    class CharClassForm(FlaskForm):
        """Dummy class, will be populated dynamically below"""

    for section in fields:
        for node in fields[section]:
            field_name = f"{section}_{node}"
            setattr(CharClassForm, field_name, FloatField(field_name, default=0.0))

    CharClassForm.fields = HiddenField("fields")
    CharClassForm.class_name = StringField("class_name")
    CharClassForm.has_name = BooleanField("has_name")
    CharClassForm.submit = SubmitField("Submit")

    return CharClassForm()


def create_char_class_complete_form(fields: list) -> FlaskForm:
    """Creates a dynamic character class form for Flask,
    based on the attributes listed under <system_name>/charsheet.py"""

    class CharClassForm(FlaskForm):
        """Dummy class, will be populated dynamically below"""

    for section in fields:
        for from_node in fields[section]:
            for to_node in fields[section]:
                field_name = f"{section}_{from_node}_to_{to_node}"
                setattr(CharClassForm, field_name, FloatField(field_name, default=0.0))

    CharClassForm.fields = HiddenField("fields")
    CharClassForm.class_name = StringField("class_name")
    CharClassForm.has_name = BooleanField("has_name")
    CharClassForm.submit = SubmitField("Submit")

    return CharClassForm()


def create_char_form(system_name: str) -> FlaskForm:
    """Creates a dynamic new character form for Flask,
    based on the attributes listed under <system_name>/charsheet.py"""

    class CreateCharForm(FlaskForm):
        """Dummy class, will be populated dynamically below"""

    available_classes = list_available_classes(system_name=system_name)
    choices = [(c, c) for c in available_classes]
    CreateCharForm.level = IntegerField("level")
    CreateCharForm.char_class = SelectField("class", choices=choices)
    CreateCharForm.submit = SubmitField("Submit")

    return CreateCharForm()
