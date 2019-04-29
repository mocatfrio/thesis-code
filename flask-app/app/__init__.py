from flask import Flask, url_for

app = Flask(__name__)

UPLOAD_FOLDER = '/Users/mocatfrio/Documents/thesis/tugas-akhir/csv'

app.secret_key = "mocatfrio"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

from app import routes

