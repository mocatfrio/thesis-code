import os, json
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import app
from app.src import solution as ss
from app.src import precompute as pr
from app.src import precomputenew as prnew

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_precomputed():
    if not os.path.exists(app.config['PANDORA_FILE']):
        return False
    else:
        return True

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title = 'Index')

@app.route('/precompute', methods=['GET', 'POST'])
def precompute():
    if request.method == 'GET':
        return render_template('precompute.html', title = 'Precomputing')
    else:
        datasets, filenames = [], []
        datasets.append(request.files.get('p_dataset'))
        datasets.append(request.files.get('c_dataset'))
        algorithm = request.form.get('algorithm')
        for file in datasets:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if not os.path.exists(app.config['UPLOAD_DIR']):
                    os.mkdir(app.config['UPLOAD_DIR'])
                file.save(os.path.join(app.config['UPLOAD_DIR'], filename))
                filenames.append(app.config['UPLOAD_DIR'] + '/' + filename)
            else:
                flash('not allowed')
                return redirect(request.url)
        if algorithm == 'kmppti':
            # print(filenames)
            app.pandora_file = pr.kmpp_precompute(filenames[0], filenames[1])
            flash('success')
        elif algorithm == 'kmppti-2':
            app.pandora_file = prnew.kmpp_precompute(filenames[0], filenames[1])
            flash('success')
        return redirect ( url_for('input') )

@app.route('/input', methods=['GET', 'POST'])
def input():
    if request.method == 'GET':
        return render_template('input.html', title = 'Input')
    else:
        if is_precomputed():
            k_product = request.form.get('num-of-product')
            time_start = request.form.get('time-start')
            time_end = request.form.get('time-end')

            result = ss.kmpp_solution(app.config['PANDORA_FILE'], k_product, time_start, time_end)
            result_json = json.dumps(result)
            loaded_r = json.loads(result_json)
            return render_template('input.html', title = 'Input', result = loaded_r, param = [k_product, time_start, time_end]) 
        else:
            flash('error')
            return redirect(request.url)
