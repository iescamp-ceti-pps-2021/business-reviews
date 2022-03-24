from flask import flash, redirect, render_template, request, url_for
from flask_babel import _  # noqa: F401
from flask_babel import lazy_gettext as _l
from flask_login import login_required, login_user, logout_user
from sqlalchemy.exc import (
    DatabaseError,
    DataError,
    IntegrityError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.urls import url_parse

from app.auth import bp
from app.auth.forms import LoginForm, RegisterForm
from app.models.users import User


@bp.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            username = form.username.data
            first_name = form.first_name.data or None
            last_name = form.last_name.data or None
            email = form.email.data
            password_hash = User.hash_password(form.password.data)

            new_user = User(
                username=username, first_name=first_name, last_name=last_name, email=email, password_hash=password_hash
            )
            new_user.create()

            flash(_l("Account Succesfully created"), "success")
            return redirect(url_for("main.index"))

        except InvalidRequestError:
            # db.session.rollback()
            flash(_l("Something went wrong!"), "danger")
        except IntegrityError:
            # db.session.rollback()
            flash(_l("User already exists!."), "warning")
        except DataError:
            # db.session.rollback()
            flash(_l("Invalid Entry"), "warning")
        except InterfaceError:
            # db.session.rollback()
            flash(_l("Error connecting to the database"), "danger")
        except DatabaseError:
            # db.session.rollback()
            flash(_l("Error connecting to the database"), "danger")
        except Exception as e:
            print(e)
            flash(e, "danger")
    return render_template(
        "auth.html", form=form, text=_l("Create a new account"), title=_l("Register"), btn_action=_l("Register account")
    )


@bp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = User.filter(username=form.username.data)
            if user.verify_password(form.password.data):
                login_user(user)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('main.index')
                return redirect(next_page)
            else:
                flash(_l("Invalid Username or password!"), "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html", form=form, text=_l("Sign In"), title=_l("Login"), btn_action=_l("Login"))


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
