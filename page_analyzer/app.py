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
    get_url_checks_by_id
)
from .log import LOGGER
from bs4 import BeautifulSoup
import requests
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
    )


@app.route('/urls/<int:id>')
def url_show(id):
    url = get_url(id)
    url_checks = get_url_checks_by_id(url.id)
    return render_template(
        "url.html",
        id=url.id,
        name=url.name,
        date=url.created_at,
        checks=url_checks
    )


def parse_page_htlm(htlm_data):
    soup = BeautifulSoup(htlm_data, "html.parser")
    for meta in soup.find_all('meta'):
        if meta.get("name") == "description":
            description = meta.get('content')
            break
    result_parse = {
        "h1": soup.find("h1").string if soup.find("h1") else "",
        "title": soup.find("title").string if soup.find("title") else "",
        "description": description[:250] + '...',
    }
    return result_parse


@app.post('/urls/<id>/checks')
def url_check(id):
    try:
        url = get_url(id)
        check = requests.get(url.name)
        check.raise_for_status()
        parser = parse_page_htlm(check.content)
        result_check = {
                        "status_code": check.status_code,
                        "h1": parser.get('h1'),
                        "title": parser.get('title'),
                        "description": parser.get('description')
                        }
        add_url_checks(id, result_check)
        flash('Страница успешно проверена', 'success')

    except requests.exceptions.RequestException as e:
        flash('Произошла ошибка при проверке', 'danger')
        LOGGER.error(e)

    finally:
        return redirect(url_for('url_show', id=id))
