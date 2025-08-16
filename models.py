from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    level = db.Column(db.String(20), nullable=False)
    city = db.Column(db.Integer, nullable=False)
    people = db.Column(db.Integer, nullable=False)
    detail = db.Column(db.String(20), nullable=True)
    file_name = db.Column(db.String(20), nullable=True)
    #memeber = db.Column(db.Interger, nullable = True)
    leader_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), unique=True, nullable=False)
    leader = db.relationship('User', backref=db.backref('team', uselist=False, cascade='all, delete', passive_deletes=True))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    boards = db.relationship('Board', backref='author', cascade='all, delete', passive_deletes=True)


class Board(db.Model): #Board N
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(15), nullable=False)
    time = db.Column(db.String(15), nullable=False)
    level = db.Column(db.String(15), nullable=False)
    title = db.Column(db.String(15), nullable=False)
    detail = db.Column(db.String(300), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    


#가입 신청 대기열
class JoinList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Integer)
    details = db.Column(db.String(300), nullable=False)    
    #team_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)