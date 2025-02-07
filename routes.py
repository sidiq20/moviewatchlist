from flask import Blueprint, render_template, session, redirect, request
from forms import MovieForm
from models import Movie
import uuid



pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@pages.route("/")
def index():
    movie_data = current_app.db.movie.find({})
    movies = [Movie(**movie) for movie in movie_data]
    return render_template(
        "index.html",
        title="Movies Watchlist",
    )


@pages.route("/add", methods=["GET", "POST"])
def add_movie():
    form = MovieForm()

    if form.validate_on_submit():
        movie = Movie(
            _id=uuid.uuid4().hex,
            title=form.title.data,
            director=form.director.data,
            year=form.year.data
        )

        current_app.db.movie.insert_one(movie)

        return redirect(url_for(".index"))

    return render_template(
        "new_movie.html",
        title="Movies Watchlist - Add Movie",
        form=form
    )

@pages.get("/movie/<string:_id>")
def movie(_id: str):
    movie_data = current_app.db.movie.fine_one({"_id": _id})
    if not movie_data:
        abort(404)
    movie = Movie(**movie_data)
    return render_template(
        "movie_details.html",
                           movie=movie)


@pages.get("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"

    return redirect(request.args.get("current_page"))