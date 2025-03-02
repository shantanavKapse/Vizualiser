from app import db
from sqlalchemy import JSON


class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    file_name = db.Column(db.String , nullable = False)
   
    def __repr__(self):
        return f"Dashboard('{self.id}')"
    

class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    data = db.Column(JSON  , nullable = False)
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboard.id'))
    dashboard = db.relationship('Dashboard', backref='component')
   
    def __repr__(self):
        return f"Deshboard('{self.name}')"