from poorman import db
from datetime import datetime

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    first_surname = db.Column(db.String(50), nullable=False)
    second_surname = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True, nullable=False)
    job_code = db.Column(db.String(10), nullable=False, default='BE03-345')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.name}', '{self.first_surname}', '{self.email}')"