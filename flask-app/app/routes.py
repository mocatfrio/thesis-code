import os
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import app
from app.src import solution as ss
from app.src import precompute as pr

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    return render_template("index.html", title = "Index")

@app.route('/dataset', methods=['GET', 'POST'])
def dataset():
    if request.method == 'GET':
        return render_template("dataset.html", title = "Dataset")
    else:
        datasets, filenames = [], []
        datasets.append(request.files.get('p_dataset'))
        datasets.append(request.files.get('c_dataset'))
        algorithm = request.form.get('algorithm')
        for file in datasets:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.mkdir(app.config['UPLOAD_FOLDER'])
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filenames.append(app.config['UPLOAD_FOLDER'] + '/' + filename)
                flash('success_upload')
            else:
                flash('error_upload')
        if algorithm == 'kmpp':
            pr.kmpp_precompute(filenames[0], filenames[1])
        return redirect ( url_for('dataset') )

@app.route('/input', methods=['GET', 'POST'])
def input():
    if request.method == 'GET':
        return render_template("input.html", title = "Input")
    else:
        k_product = request.form.get('num_of_product')
        time_start = request.form.get('time_start')
        time_end = request.form.get('time_end')
        return redirect ( url_for('input') )
