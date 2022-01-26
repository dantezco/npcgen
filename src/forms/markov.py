"""Form Objects declaration"""

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, FloatField, HiddenField

from src.system.fnv_tt.fields import FNVTT_ATTRIBUTES


class ChooseAttributesForm(FlaskForm):
    """Choose from which set of attributes to generate a Markov form"""

    choices = SelectField("Attributes Sets", choices=((x, x) for x in FNVTT_ATTRIBUTES))
    submit = SubmitField('Submit')


def create_dynamic_form(fields: list) -> FlaskForm:
    class MyForm(FlaskForm):
        pass

    for from_node in fields:
        for to_node in fields:
            field_name = f"{from_node}_to_{to_node}"
            setattr(MyForm, field_name, FloatField(field_name, 0.0))
    MyForm.fields = HiddenField(fields)
    MyForm.submit = SubmitField("Submit")
    return MyForm()

