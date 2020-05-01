from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Prediction(db.Model):
    __tablename__ = 'prediction'

    # id = db.Column(db.Integer, primary_key=True)
    netflow_id = db.Column(db.Integer, db.ForeignKey('netflow.id', ondelete='CASCADE'), primary_key=True)
    predictive_model_id = db.Column(db.Integer, db.ForeignKey('predictive_model.id', ondelete='CASCADE'), primary_key=True)
    predicted_probability = db.Column(db.Float)

    netflow = db.relationship("NetFlow", backref="predictive_models")
    predictive_model = db.relationship("PredictiveModel", backref="netflows")

class NetFlow(db.Model):
    '''
    look at documentation for flask_sqlalchemy and for SQLAlchemy
    '''
    __tablename__ = "netflow"

    id = db.Column(db.Integer, primary_key=True)
    StartTime=db.Column(db.String(30))
    Dur=db.Column(db.Float)
    Proto=db.Column(db.String(7))
    SrcAddr= db.Column(db.String(39), nullable = False)
    Sport=db.Column(db.String(10), nullable = False)
    Dir=db.Column(db.String(10))
    DstAddr=db.Column(db.String(39), nullable = False)
    Dport=db.Column(db.String(10), nullable = False)
    State=db.Column(db.String(15))
    sTos=db.Column(db.Float)
    dTos=db.Column(db.Float)
    TotPkts=db.Column(db.Integer)
    TotBytes=db.Column(db.Integer)
    SrcBytes=db.Column(db.Integer)
    Predictions=db.Column(db.String)
    reso=db.Column(db.String(1), server_default = '0')
    time_resolved=db.Column(db.DateTime, onupdate=datetime.datetime.now())

class PredictiveModel(db.Model):
    __tablename__ = "predictive_model"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
