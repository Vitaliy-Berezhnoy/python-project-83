import os
#import psycopg2

from page_analyzer.db import UrlsRepo

from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL =os.getenv('DATABASE_URL')
app.config['DATABASE_URL'] = DATABASE_URL

repo = UrlsRepo(DATABASE_URL)


@app.route("/")
def home():
    return render_template('new.html')


@app.route("/urls")
def urls_get():
    urls = repo.get_all_urls()
    return render_template('index.html', urls=urls)