from app import app, db, PredictiveModel

with app.app_context():
    db.drop_all()
    db.create_all()

    kddcup = PredictiveModel(name='kddcup')
    ctu_13 = PredictiveModel(name='ctu_13')
    db.session.add(kddcup)
    db.session.add(ctu_13)
    db.session.commit()
