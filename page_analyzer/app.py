import os
import requests
import psycopg2
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from page_analyzer.utilities import (
    parse_url,
    parse_response,
    validate_url
)
from page_analyzer.url_analisys_repository import UrlRepository


app = Flask(__name__)
load_dotenv()
database_url = os.getenv('DATABASE_URL')
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

repo = UrlRepository(psycopg2.connect(database_url))


@app.route('/')
def home_page():
    errors = {}
    url_adress = request.args.get('url', '')
    return render_template(
        'index.html',
        search=url_adress,
        errors=errors
    )


@app.post('/urls')
def post_url():
    entered_address = request.form.to_dict()
    normalized_url = parse_url(entered_address['url'])
    errors = validate_url(normalized_url)

    if errors:
        flash('Некорректный URL', 'error')
        return render_template(
            'index.html',
            search=normalized_url,
            errors=errors
        ), 422

    id = repo.get_id(normalized_url)
    if id is not None:
        flash('Страница уже существует', 'warning')
        return redirect(url_for('get_url', id=id), code=302)

    id = repo.add(normalized_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', id=id), code=302)


@app.route('/urls/<int:id>')
def get_url(id):
    url_info = repo.find(id)
    url_check = repo.get_checks(id)

    if not url_info:
        return render_template('urls/not_found.html')

    return render_template(
        'urls/id_info.html',
        url_info=url_info,
        url_check=url_check
    )


@app.route('/urls')
def get_urls_list():
    urls = repo.get_content()

    return render_template(
        'urls/show_urls.html',
        urls=urls
    )


@app.post('/urls/<int:id>/cheks')
def post_url_check(id):
    url_info = repo.find(id)

    try:
        response = requests.get(url_info.get('name'), timeout=0.3)
        response.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('get_url', id=id))

    status = response.status_code
    analysis = parse_response(response)

    id = repo.check(
        url_info,
        status,
        analysis
    )

    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url', id=id), code=302)
