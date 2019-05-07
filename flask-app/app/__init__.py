from flask import Flask, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.getcwd() + '/upload'

app.secret_key = "mocatfrio"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

from app import routes

