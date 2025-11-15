from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    level = db.Column(db.String(20), nullable=False)
    city = db.Column(db.Integer, nullable=False)
    people = db.Column(db.Integer, nullable=False)
    detail = db.Column(db.String(300), nullable=True)
    file_name = db.Column(db.String(100), nullable=True)

    # 리더: User와 1:1
    leader_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        unique=True,
        nullable=False
    )
    leader = db.relationship(
        'User',
        backref=db.backref('leading_team', uselist=False, passive_deletes=True)
    )
    members = db.relationship('Member', back_populates='team', cascade='all, delete')
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(300), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    memberships = db.relationship('Member', back_populates='user', cascade='all, delete')
    boards = db.relationship('Board', backref='author', cascade='all, delete', passive_deletes=True)

user = {"id":"abc123", "name":"정서윤", "email":"test@test.com", "city":"서울"}

class Board(db.Model): #Board N
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(15), nullable=False)
    time = db.Column(db.String(15), nullable=False)
    level = db.Column(db.String(15), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.String(300), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now()) #자동 생성 시간 기록
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now()) #자동 수정 시간 기록
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)


#가입 신청 대기열
class JoinList(db.Model):
    __tablename__ = 'joinlist'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), nullable=False)
    details = db.Column(db.String(300), nullable=False)    
    team_id = db.Column(db.Integer, db.ForeignKey('team.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
 
    
class Member(db.Model):
    """ User - Team 다대다 관계를 풀어내는 테이블 """
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    team = db.relationship('Team', back_populates='members')
    user = db.relationship('User', back_populates='memberships')

class Match(db.Model):
    __tablename__ = 'match'
    id = db.Column(db.Integer, primary_key=True)
    request_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)  
    opponent_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False) 
    request_team_score = db.Column(db.Integer, default=0)  
    opponent_team_score = db.Column(db.Integer, default=0) 
    details = db.Column(db.String(500))                    
    isEnd = db.Column(db.Boolean, default=False)        
    match_datetime = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    is_accept = db.Column(db.Boolean, default=False)    # 승인 여부 추가




