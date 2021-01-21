from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """This will be my User Table. People who log in can use this to keep track of their own players"""
    __tablename__ = 'users'
                
    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
        primary_key=True)

    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    
    
class Stat(db.Model):
    """This data will contain data from the current season"""

    __tablename__='stats'

    id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    plid = db.Column(db.String,
                        nullable=False)
    player = db.Column(db.String,
                        nullable = False)
    pos = db.Column(db.String,
                        nullable = False)
    age = db.Column(db.Integer,
                        nullable = False)
    team = db.Column(db.Integer,
                        nullable = False)
    g = db.Column(db.Integer,
                        nullable = False)
    gs = db.Column(db.Integer,
                        nullable = False)
    mp = db.Column(db.Integer,
                        nullable = False)
    fg = db.Column(db.Integer,
                        nullable = False)
    fga = db.Column(db.Integer,
                        nullable = False)
    fgp = db.Column(db.Float,
                        nullable = True)
    threep = db.Column(db.Integer,
                        nullable = False)
    threepa = db.Column(db.Integer,
                        nullable = False)
    threepper = db.Column(db.Float,
                        nullable = True)
    two = db.Column(db.Integer,
                        nullable = False)
    twoa = db.Column(db.Integer,
                        nullable = False)
    twoper = db.Column(db.Float,
                        nullable = True)
    efg = db.Column(db.Float,
                        nullable = False)
    ft = db.Column(db.Integer,
                        nullable = False)
    fta = db.Column(db.Integer,
                        nullable = False)
    ftper = db.Column(db.Float,
                        nullable = True)
    orb = db.Column(db.Integer,
                        nullable = False)
    drb = db.Column(db.Integer,
                        nullable = False)
    trb = db.Column(db.Integer,
                        nullable = False)
    ast = db.Column(db.Integer,
                        nullable = False)
    stl = db.Column(db.Integer,
                        nullable = False)
    blk = db.Column(db.Integer,
                        nullable = False)
    tov = db.Column(db.Integer,
                        nullable = False)
    pf = db.Column(db.Integer,
                        nullable = False)
    pts = db.Column(db.Integer,
                        nullable = False)
    
class Salary(db.Model):
    """This area wil have a table of players salaries"""
    __tablename__ = "salaries"

    plid = db.Column(db.String,
                        nullable = False,
                        unique = True,
                        primary_key = True)
    
    salary = db.Column(db.Integer,
                        nullable = False)