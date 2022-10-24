import os
from datetime import timedelta

from flask import Flask

app = Flask(__name__,
            template_folder='./templates'
            , static_folder='./templates'
            , static_url_path='')

app.config['SECRET_KEY'] = os.urandom(24)
print(app.config['SECRET_KEY'])
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # 一天
from app import index, user_send_email, user_register, user_login, user_token_check, \
    movie_detail, movie_like, movie_list, movie_countries, movie_genres, movie_persons, \
    person_list, person_like, person_detail
