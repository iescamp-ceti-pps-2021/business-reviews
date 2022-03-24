from flask_babel import _  # noqa: F401
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import IntegerRangeField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, NumberRange, Optional


class BusinessForm(FlaskForm):
    name = StringField(_l("Name"), validators=[InputRequired(), Length(1, 50)])
    address_street = StringField(_l("Street"), validators=[Optional(), Length(1, 100)])
    address_city = StringField(_l("City"), validators=[InputRequired(), Length(1, 50)])
    description = TextAreaField(_l("Description"), validators=[InputRequired(), Length(1, 250)])

    submit = SubmitField(_l("Submit"))


class ReviewForm(FlaskForm):
    rating = IntegerRangeField(_l("Rating"), validators=[InputRequired(), NumberRange(1, 5)])
    review_text = TextAreaField(_l("Text"), validators=[InputRequired(), Length(1, 500)])

    submit = SubmitField(_l("Submit"))
