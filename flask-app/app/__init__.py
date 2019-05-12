from flask import Flask, url_for
import os

app = Flask(__name__)

app.secret_key = "mocatfrio"
app.config['UPLOAD_DIR'] = os.getcwd() + '/app/upload'
app.config['LOG_DIR'] = os.getcwd() + '/app/log'
app.config['PANDORA_FILE'] = app.config['UPLOAD_DIR'] + '/pandora_box.csv'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

from app import routes
