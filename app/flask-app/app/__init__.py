from flask import Flask, url_for
import os

app = Flask(__name__)

app.secret_key = "mocatfrio"
app.config['UPLOAD_DIR'] = os.getcwd() + '/app/upload'
app.config['LOG_DIR'] = os.getcwd() + '/app/log'
app.config['SESSION_DIR'] = os.getcwd() + '/app/session'
app.config['SESSION_FILE'] = os.getcwd() + '/app/session/session.json'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

from app import routes

