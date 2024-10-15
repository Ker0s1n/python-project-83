import os
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)
from page_analyzer import db_module


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
    conn = db_module.connect_db(DATABASE_URL)
    url = request.form.to_dict()
    errors = validator.validate(url)

    if errors:
        return render_template(
            'page.html',
            url=url,
            errors=errors
        )
