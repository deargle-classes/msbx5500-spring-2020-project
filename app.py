from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
import gridfs
import os
import subprocess
import datetime
from io import BytesIO
import pandas as pd
# May need this if not imported in PyMongo: from bson.objectid import ObjectId 

app = Flask(__name__)
# add cross-origin allow to all routes
CORS(app)

# convenience class for throwing api errors in valid format
# https://flask.palletsprojects.com/en/1.1.x/patterns/apierrors/
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

########
### PSQL
########
# get psql db up. quickstart here: https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Alert(db.Model):
    '''
    look at documentation for flask_sqlalchemy and for SQLAlchemy
    '''
    id = db.Column(db.Integer, primary_key=True, nullable= False)
    srcaddr= db.Column(db.String(39), nullable = False)
    dstaddr=db.Column(db.String(39), nullable = False)
    pkts=db.Column(db.Integer)
    octets=db.Column(db.Integer)
    srcport=db.Column(db.Integer, nullable = False)
    dstport=db.Column(db.Integer, nullable = False)
    prot=db.Column(db.Integer)
    timestamp=db.Column(db.DateTime)
    reso=db.Column(db.Integer, nullable = False, default = 0)
    time_resolved=db.Column(db.DateTime, onupdate=datetime.datetime.now())
    
###########
### MONGODB
###########
# get a mongodb up
# quickstart https://flask-pymongo.readthedocs.io/en/latest/
app.config["MONGO_URI"] = os.getenv('MONGODB_URI')
mongo = PyMongo(app)
fs = gridfs.GridFS(mongo.db) # direct access to the gridfs file system
                             # within the mongo database

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

############
## Files
#############
'''
the code below should only allow pcap files
'''
#allowed_extensions = {'pcap'}
#def allowed_file(filename):
#    return '.' in filename and \
#        filename.rsplit('.',1)[1].lower() in allowed_extensions

@app.route('/files/<path:filename>', methods=['POST'])
def upload_file(filename):
    '''
    The file will (should) be available under the `request.files` key,
    where `request` is a flask object provided to the route
    '''
    the_file = request.files['the_file']
    mongo.save_file(filename, the_file)
    return ('', 204)

@app.route('/files/process/<string:_id>', methods=['GET'])
def process_file(_id):
    '''
    This should fetch the hopefully-pcap file from GridFS, parse it into NetFlow
    records, and run each record against your sklearn model(s). If the prediction
    is above :shurg: some threshold, save the record (along with the prediction
    threshold? and maybe the model that made the prediction?) to the Alerts table.

    Feel free to write smaller helper functions  that this function in turn calls.
    (Please write helper functions. This is way too much for just one function.)

    the below example reads from an example `example_capture.pcap` file.
    But you will need to modify the code to read from stdin, instead. (e.g., `-r -`).
    Then, pass in a file as the `input` argument to the `check_output` call. This
    will be read by the subprocess as stdin.

    e.g., you will need to do:
        net_flows_bytes = subprocess.check_output('argus -F argus.conf -r - -w - | ra -r - -n -F ra.conf -Z b',
            input=fs.find_one({"filename": "lisa.txt"}),
            shell=True)
    '''
    '''
    From GOOGLE DOC:
    def process_file():
	Parse a pcap into netflows
	Ask a model to evaluate (make predictions for) each netflow record
	For each netflow_plus_prediction:
		If netflow_plus_prediction[prediction] > threshold:
			New_alert = Alert(netflow_plus_prediction)
			db.add(new_alert)

		db.commit()
    '''
    
    # Get file to process and parse to netflows
    file = fs.get(_id).read()
    net_flows_bytes = subprocess.check_output('argus -F argus.conf -r - -w - | ra -r - -n -F ra.conf -Z b',
            input=file,
            shell=True)
    net_flows_bytesIO = BytesIO(net_flows_bytes)
    net_flows = pd.read_csv(net_flows_bytesIO)
    
    # Feed netflow(s) to model
    path = 'https://github.com/deargle-classes/msbx5500-spring-2020-project/blob/master/pickle.pkl?raw=true'
    with open(path, 'rb') as f:
        model = pkl.load(f)
    y_score = model.predict_proba(net_flows)
    
    # Feed netflows to second model [todo]
    
    # Compare output to some threshold
    threshold = .1
    for row in y_score:
        if row > threshold:
            new_alert = Alert(row)
            db.add(new_alert)
        # If row is above threshold, commit that row to the DB
        db.commit()
    
    return ('', 204)

@app.route('/files.json', methods=['GET'])
def list_files():
    '''
    Do a "find_all" of some sort against your mongo gridfs object.
    Make sure that you're at least returning the `_id` of each file;
    will be important for the rendering of the action buttons for
    our "files" html table.

    Note: The direct return of a return from a gridfs query is not
    json-serializable because it includes _dadgum files_.
    '''
    files = [{'_id':file,
                'filename':'file_{}.pcap'.format(file)
            } for file in [1,2,3,4,5]]
    return jsonify(files)

############
## Alerts
############

@app.route('/alerts.json', methods=['GET'])
def list_alerts():
    '''
    Do some kind of find_all against your Alert class. Return the list. Make
    sure that you return some kind of `id` for each alert. Will be important
    for rendering the action buttons for our HTML table of alerts.

    See "resolve_alert" function. Perhaps filter to only return alerts that are
    not flagged as "resolved."
    '''

    alerts = [{'_id':i.id, 'n_packet': i.pkts,
                'src_bytes':i.octets, 'src_addr':i.srcaddr, 'dst_addr': i.dstaddr, 'Protocol':i.prot,'Timestamp':i.timestamp } for i in Alert.query.filter_by(reso=0).all() ]
    return jsonify(alerts)

@app.route('/alerts/<string:_id>', methods=['DELETE'])
def resolve_alert(_id):
    '''
    Ha, maybe don't actually "delete" it per se. Perhaps just "flag" it as deleted.
    (Would require an additional column in the Alerts table, something like
    "is_deleted", perhaps also with a timestamp for when it was deleted).
    Does it hurt your sensibilities to not actually "delete" something from a
    database yet pretend that it is deleted? Welcome to Ashley Madison. Else, how
    else could you "undelete" something?
    '''
    update=Alert.query.filter_by(id = _id).first()
    update.reso=1
    db.session.commit()
    return ('', 204)
