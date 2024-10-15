import os
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from page_analyzer import db_module, validator


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def home_page():
    return render_template(
        'page.html'
    )


@app.post('/')
def post_url():
    url = request.form.to_dict()
    errors = validator.validate(url)

    if errors:
        return render_template(
            'page.html',
            url=url,
            errors=errors
        )
    conn = db_module.connect_db(DATABASE_URL)
    id = db_module.add_url(conn, url)
    flash(f'URL был успешно добавлен c id: {id}', 'success')
    db_module.close(conn)
    return f'URL был успешно добавлен c id: {id}'
