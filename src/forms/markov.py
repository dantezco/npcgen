"""Form Objects declaration"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, HiddenField


def create_markov_mapping_form(fields: list) -> FlaskForm:
    class MarkovMapping(FlaskForm):
        pass

    for section in fields:
        for from_node in fields[section]:
            for to_node in fields[section]:
                field_name = f"{section}_{from_node}_to_{to_node}"
                setattr(MarkovMapping, field_name, FloatField(field_name, default=0.0))
    MarkovMapping.fields = HiddenField("fields")
    MarkovMapping.class_name = StringField("class_name")
    MarkovMapping.submit = SubmitField("Submit")
    return MarkovMapping()

