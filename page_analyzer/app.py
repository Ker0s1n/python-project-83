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
    id = db_module.add_url(conn, url)
    db_module.close(conn)

    flash(f'URL был успешно добавлен c id: {id}', 'success')
    return redirect(url_for('home_page'), code=302)


@app.route('/urls/<int:id>')
def get_url(id):
    conn = db_module.connect_db(DATABASE_URL)
    url_info = db_module.get_url(conn, id)

    if not url_info:
        db_module.close(conn)
        return '<h1>Page not found</h1>'

    db_module.close(conn)
    return render_template(
        'urls/id_info.html',
        url_info=url_info
    )
