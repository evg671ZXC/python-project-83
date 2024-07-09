from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort
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
    if request.method == 'POST':
        search_url = request.form.get('url')
        errors = validate(search_url)
        if errors:
            return render_template(
                'index.html',
                error=errors[0]
            )
        id = add_url(search_url)
        urls = get_urls()
        flash("Страница успешно добавлена", "success")
        redirect(url_for("url_show", id=id))

    urls = get_urls()

    return render_template(
        "urls/index.html",
        data=urls,
    )


@app.route("/urls/<int:id>")
def url_show(id):
    url = get_url(id)
    if url is None:
        abort(404)

    return render_template(
        "urls/url.html",
        url=url
    )
