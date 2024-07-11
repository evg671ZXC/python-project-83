from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    get_flashed_messages
)
from dotenv import load_dotenv
from .validators_url import validate
from .db import (
    get_url,
    get_urls,
    add_url
)
import os


app = Flask(__name__)


load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'])
def urls():
    urls = get_urls()
    messages = get_flashed_messages(with_categories=True)

    if request.method == 'POST':
        search_url = request.form.get('url')
        errors = validate(search_url)
        if errors:
            for error in errors:
                flash(error, "danger")
                return render_template("index.html", messages=messages), 422

        for url in urls:
            if search_url in url.name:
                id = url.id
                flash('Страница уже существует', 'info')
                return redirect(url_for('url_show', id=id))

        id = add_url(search_url)
        flash("Страница успешно добавлена", "success")
        return redirect(url_for("url_show", id=id))

    return render_template(
        "urls.html",
        urls=urls,
        code=200
    )


@app.route("/urls/<int:id>")
def url_show(id):
    url = get_url(id)

    return render_template(
        "url.html",
        id=url.id,
        name=url.name,
        date=url.created_at
    )
