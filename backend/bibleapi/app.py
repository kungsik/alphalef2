'''
app.py 
플라스크 인스턴스를 정의함
api 블루프린트 정의
api 호출을 위해 cors 설치 필요함
'''

from flask import Flask
from flask_cors import CORS

def create_app(app_name='AlphAlefBible'):
    app = Flask(app_name)
    CORS(app)

    from bibleapi.api import api
    app.register_blueprint(api, url_prefix="/api")

    return app

