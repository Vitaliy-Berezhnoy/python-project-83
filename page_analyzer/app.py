import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from requests.exceptions import ConnectionError, HTTPError, ReadTimeout

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
    else:
        url_id = repo.add_url(url)
        flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_get', url_id=url_id))


@app.route("/urls/<int:url_id>")
def url_get(url_id):
    url = repo.get_url(url_id)
    url_checks = repo.get_url_checks(url_id)
    return render_template('show.html', url=url, checks=url_checks)


@app.post("/urls/<int:url_id>/checks")
def checks_post(url_id):
    url = repo.get_url(url_id)
    try:
        resp = requests.get(url['name'], timeout=5)
        resp.raise_for_status()
    except (HTTPError, ReadTimeout, ConnectionError):
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('url_get', url_id=url_id))

    soup = BeautifulSoup(resp.text)
    meta_tag = soup.find('meta', attrs={'name': 'description'})

    check = {
        'url_id': url_id,
        'status_code': resp.status_code,
        'h1': soup.h1.text if soup.h1 else None,
        'title': soup.title.string if soup.title else None,
        'description': meta_tag.get('content', None) if meta_tag else None
    }
    repo.add_check(check)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('url_get', url_id=url_id))



