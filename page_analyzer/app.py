import os
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    get_flashed_messages
)
from page_analyzer import db_module, validator


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route('/')
def home_page():
    errors = {}
    url_adress = request.args.get('url', '')
    return render_template(
        'index.html',
        search=url_adress,
        messages=get_flashed_messages(with_categories=True),
        errors=errors
    )


@app.post('/')
def post_url():
    url = request.form.to_dict()
    errors = validator.validate(url)

    if errors:
        flash('URL не добавлен', 'error')
        return render_template(
            'index.html',
            search=url['url'],
            messages=get_flashed_messages(with_categories=True),
            errors=errors
        ), 422

    conn = db_module.connect_db(DATABASE_URL)

    id = db_module.url_unique_id(conn, url)
    if id is not None:
        db_module.close(conn)
        flash(f'URL был добавлен ранее c id: {id}', 'warning')
        return redirect(url_for('get_url', id=id), code=302)

    id = db_module.add_url(conn, url)
    db_module.close(conn)

    flash(f'URL был успешно добавлен c id: {id}', 'success')
    return redirect(url_for('get_url', id=id), code=302)


@app.route('/urls/<int:id>')
def get_url(id):
    conn = db_module.connect_db(DATABASE_URL)
    url_info = db_module.get_url(conn, id)
    url_check = db_module.show_url_checks(conn, id)

    if not url_info:
        db_module.close(conn)
        return render_template('urls/not_found.html')

    db_module.close(conn)
    return render_template(
        'urls/id_info.html',
        url_info=url_info,
        url_check=url_check,
        messages=get_flashed_messages(with_categories=True)
    )


@app.route('/urls')
def get_urls_list():
    messages = get_flashed_messages(with_categories=True)
    conn = db_module.connect_db(DATABASE_URL)
    urls = db_module.show_urls(conn)
    db_module.close(conn)

    return render_template(
        'urls/show_urls.html',
        urls=urls,
        messages=messages
    )


@app.post('/urls/<int:id>/cheks')
def post_url_check(id):
    conn = db_module.connect_db(DATABASE_URL)
    url_info = db_module.get_url(conn, id)

    # if errors:
    #     flash('Произошла ошибка: сайт не прошёл проверку', 'error')
    #     return redirect(url_for('get_url', id=id), code=406)

    id = db_module.add_url_check(conn, url_info)
    db_module.close(conn)

    flash(f'проверка URL была успешно добавлена для id: {id}', 'success')
    return redirect(url_for('get_url', id=id), code=302)
