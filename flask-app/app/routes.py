import os, json, csv
from collections import OrderedDict
from flask import render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from app import app
from app.src import solution as ss
from app.src import precompute as pr
from app.src import precompute_kmppti as pre

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_session():
  data = json.load(open(app.config['SESSION_FILE']))
  session = []
  for key in data['session']:
    session.append(key)
  return session

def get_metadata(session_name):
  data = json.load(open(app.config['SESSION_FILE']))
  return data['session'][session_name]

def get_data(session_name):
  data = json.load(open(app.config['SESSION_FILE']))
  product_path = app.config['UPLOAD_DIR'] + '/' + data['session'][session_name]['product_data']
  customer_path = app.config['UPLOAD_DIR'] + '/' + data['session'][session_name]['customer_data']
  p_data = read_csv(product_path)
  c_data = read_csv(customer_path)
  return p_data, c_data

def read_csv(path):
  data = []
  with open(path) as csv_file:  
    reader = csv.DictReader(csv_file)
    for row in reader:
      data.append(dict(OrderedDict(row)))
  return data

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
  return render_template('index.html', title = 'Index')

@app.route('/precompute', methods=['GET', 'POST'])
def precompute():
  if request.method == 'GET':
    return render_template('precompute.html', title = 'Precomputing', session = read_session())
  else:
    if request.form.get('session'):
      session_name = request.form.get('session')
      return redirect ( url_for('search', session_name = session_name) )
    else:
      datasets, filenames = [], []
      datasets.append(request.files.get('p_dataset'))
      datasets.append(request.files.get('c_dataset'))
      algorithm = request.form.get('algorithm')
      for dataset in datasets:
        if dataset and allowed_file(dataset.filename):
          filename = secure_filename(dataset.filename)
          if not os.path.exists(app.config['UPLOAD_DIR']):
            os.mkdir(app.config['UPLOAD_DIR'])
          dataset.save(os.path.join(app.config['UPLOAD_DIR'], filename))
          filenames.append(app.config['UPLOAD_DIR'] + '/' + filename)
        else:
          flash('not allowed')
          return redirect(request.url)
      if algorithm == 'kmppti':
        session_name = pr.kmpp_precompute(filenames[0], filenames[1])
        flash('success')
      elif algorithm == 'kmppti-2':
        session_name = pre.kmppti_precompute(filenames)
        flash('success')
      return redirect ( url_for('search', session_name = session_name) )

@app.route('/search', methods=['GET', 'POST'])
def search_session():
  if request.method == 'GET':
    return render_template('search_session.html', title = 'Search', session = read_session())
  else:
    session_name = request.form.get('session')
    return redirect ( url_for('search', session_name = session_name) )

@app.route('/search/<session_name>', methods=['GET', 'POST'])
def search(session_name):
  if request.method == 'GET':
    return render_template('search.html', title = 'Search', session_name = session_name)
  else:
    k_product = request.form.get('num-of-product')
    time_start = request.form.get('time-start')
    time_end = request.form.get('time-end')
    pandora_path = app.config['SESSION_DIR'] + '/' + session_name + '/pandora_box.csv'

    result = ss.kmpp_solution(pandora_path, k_product, time_start, time_end)
    result_json = json.dumps(result)
    loaded_r = json.loads(result_json)
    return render_template('search.html', title = 'Search', result = loaded_r, param = [k_product, time_start, time_end], session_name = session_name) 

@app.route('/visualization', methods=['GET', 'POST'])
def visualization():
  if request.method == 'GET':
    return render_template('visualization.html', title = 'Visualization', session = read_session())
  else:
    session_name = request.form.get('session')
    return redirect ( url_for('vis', session_name = session_name) )

@app.route('/visualization/<session_name>', methods=['GET'])
def vis(session_name):
  metadata = get_metadata(session_name)
  p_data, c_data = get_data(session_name)
  return render_template('vis.html', title = 'Visualization', session_name = session_name, metadata = metadata, product = p_data, customer = c_data)

@app.route('/get_vis_data/<session_name>', methods=['GET'])
def get_vis_data(session_name):
  p_data, c_data = get_data(session_name)
  data = p_data + c_data
  new_data = []
  counter = 0
  for d in data:
    dt = {}
    dt['id'] = counter
    dt['content'] = d['label']
    dt['start'] = d['ts_in']
    dt['end'] = d['ts_out']
    new_data.append(dt)
    counter += 1
  return jsonify(new_data)
  
