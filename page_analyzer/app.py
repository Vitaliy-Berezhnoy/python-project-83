import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from page_analyzer.db import UrlsRepo
from page_analyzer.url_utilities import is_valid_url, normalize_url

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
app.config['DATABASE_URL'] = DATABASE_URL

repo = UrlsRepo(DATABASE_URL)


@app.route("/")
def home():
    return render_template('new.html')


@app.route("/urls")
def urls_get():
    urls = repo.get_all_urls()
    return render_template('index.html', urls=urls)


@app.post("/urls")
def urls_post():
    url = request.form.get('url', '').strip()
    if not is_valid_url(url):
        flash('Некорректный URL', 'danger')
        return render_template("new.html", url=url), 422
    url = normalize_url(url)
    existing_url = repo.find_same_url(url)
    if existing_url:
        flash('Страница уже существует', 'info')
        url_id = existing_url
        print('22222', url_id, '333333')
    else:
        url_id = repo.add_url(url)
        flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_get', id=url_id))


@app.route("/urls/<int:id>")
def url_get(id):
    url = repo.get_url(id)
    return render_template('show.html', url=url)


