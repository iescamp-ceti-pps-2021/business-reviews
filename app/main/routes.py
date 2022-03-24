from datetime import datetime, timedelta

from flask import flash, g, redirect, render_template, session, url_for
from flask_babel import _  # noqa: F401
from flask_babel import get_locale
from flask_babel import lazy_gettext as _l
from flask_login import current_user, login_required

from app.main import bp
from app.main.forms import BusinessForm, ReviewForm
from app.models.businesses import Business
from app.models.reviews import Review


@bp.before_request
def session_handler():
    session.permanent = True
    bp.permanent_session_lifetime = timedelta(minutes=1)


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.date_last_visited = datetime.utcnow()
        current_user.update()
        # g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route('/')
def index():
    businesses = Business.retrieve_all()
    return render_template('index.html', title=_l("Home"), businesses=businesses)


@bp.route('/business/<id>', methods=['GET'])
def details_business(id):
    business = Business.retrive_by_id(id)
    reviews = business.reviews.all()
    form = ReviewForm()
    return render_template('business_details.html', form=form, business=business, reviews=reviews)


@bp.route('/business', methods=['GET', 'POST'])
@login_required
def create_business():
    form = BusinessForm()

    if form.validate_on_submit():
        try:
            name = form.name.data
            address_street = form.address_street.data or None
            address_city = form.address_city.data
            description = form.description.data

            new_business = Business(
                name=name, address_street=address_street, address_city=address_city, description=description
            )
            new_business.create()

            flash(_l("Business succesfully created"), "success")
            return redirect(url_for("main.index"))
        except Exception as e:
            flash(e, "danger")

    return render_template("business.html", form=form, title=_l("New Business"))


@bp.route('/review/<id>', methods=['POST'])
@login_required
def create_review(id):
    form = ReviewForm()

    if form.validate_on_submit():
        try:
            rating = form.rating.data
            review_text = form.review_text.data

            new_review = Review(rating=rating, review_text=review_text, business_id=id, author_id=current_user.id)
            new_review.create()

            flash(_l("Review succesfully created"), "success")
        except Exception as e:
            flash(e, "danger")

    return redirect(url_for("main.details_business", id=id))


@bp.context_processor
def utility_processor():
    def star_rating(id):

        # reviews = Review.query.where(Review.business_id == id)
        business = Business.retrive_by_id(id)
        reviews = business.reviews.all()

        ratings = []
        review_count = 0
        for review in reviews:
            ratings += [review.rating]
            review_count += 1

        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        stars_percent = round((avg_rating / 5.0) * 100) if review_count > 0 else 0
        return {'avg_rating': avg_rating, 'review_count': review_count, 'stars_percent': stars_percent}

    return dict(star_rating=star_rating)
