from flask_babel import _  # noqa: F401
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import Email, EqualTo, InputRequired, Length, Optional, Regexp

from app.models.users import User


class LoginForm(FlaskForm):
    username = StringField(_l("Username"), validators=[InputRequired()], render_kw={"placeholder": _l("Username")})
    password = PasswordField(_l("Password"), validators=[InputRequired()], render_kw={"placeholder": _l("Password")})
    remember_me = BooleanField(_l("Remember me"))
    submit = SubmitField(_l("Sign In"))


class RegisterForm(FlaskForm):
    username = StringField(
        _l("Username"),
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                _l("Usernames must have only letters, numbers, dots or underscores"),
            ),
        ],
        render_kw={"placeholder": _l("Username")},
    )
    email = StringField(validators=[InputRequired(), Email(), Length(1, 120)], render_kw={"placeholder": _l("Email")})
    first_name = StringField(validators=[Optional(), Length(1, 80)], render_kw={"placeholder": _l("First Name")})
    last_name = StringField(validators=[Optional(), Length(1, 120)], render_kw={"placeholder": _l("Last Name")})
    password = PasswordField(
        _l("Password"), validators=[InputRequired(), Length(8, 72)], render_kw={"placeholder": _l("Password")}
    )
    confirm_password = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("password", message=_l("Passwords must match !")),
        ],
        render_kw={"placeholder": _l("Confirm Password")},
    )
    submit = SubmitField(_l("Sign Up"))

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError(_l("Email already registered!"))

    def validate_uname(self, uname):
        if User.query.filter_by(username=uname.data).first():
            raise ValidationError(_l("Username already taken!"))
