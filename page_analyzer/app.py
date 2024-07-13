from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from dotenv import load_dotenv
from urllib.parse import urlparse
from .validators_url import validate
from .db import (
    get_url,
    get_urls,
    add_url,
    add_url_checks,
    get_urls_checks,
    get_url_checks_by_id
)
from requests import RequestException
from .log import LOGGER
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

    if request.method == 'POST':
        search_url = request.form.get('url')
        errors = validate(search_url)
        if errors:
            for error in errors:
                flash(error, "danger")
                return render_template("index.html"), 422

        url = urlparse(search_url)
        correct_url = f"{url.scheme}://{url.hostname}"

        for url in urls:
            if correct_url in url.name:
                id = url.id
                flash('Страница уже существует', 'info')
                return redirect(url_for('url_show', id=id))

        id = add_url(correct_url)
        flash("Страница успешно добавлена", "success")
        return redirect(url_for("url_show", id=id))

    return render_template(
        "urls.html",
        urls=urls,
        code=200
    )


@app.route('/urls/<int:id>')
def url_show(id):
    url = get_url(id)
    urls_checks = get_urls_checks()
    return render_template(
        "url.html",
        id=url.id,
        name=url.name,
        date=url.created_at,
        checks=urls_checks
    )


@app.post('/urls/<id>/checks')
def url_check(id):
    try:
        result_check = {"status_code": 200, "h1": "", "title":"", "description":""}
        add_url_checks(id, result_check)
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('url_show', id=id))
    
    except RequestException as e:
        flash('Произошла ошибка при проверке', 'danger')
        LOGGER.error(e)
        return redirect(url_for('url_show', id=id))