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
    
    username = db.Column(db.String,
                        nullable=False,
                        unique=True,
                        primary_key=True
                        )

    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    team = db.relationship('Team', cascade = "all, delete-orphan")
    
    
    @property
    def full_name(self):
        """Return the full name"""
        return f"{self.first_name} {self.last_name}"
    @classmethod
    def register(cls,username, password, email, first_name, last_name):
        """Register user w/ hashed password & Return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string 
        hashed_utf8 = hashed.decode("utf8")

        user = cls(

            username = username,
            password = hashed_utf8,
            email = email,
            first_name = first_name,
            last_name = last_name,
            )

        db.session.add(user)

        return user 

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct. return user if valid; else return False."""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False   
    
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
    team = db.Column(db.String,
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
    sal = db.Column(db.Integer,
                        nullable = False)
    assignments = db.relationship('TeamPlayers', backref='player', cascade = "all, delete-orphan")
    
    @property
    def flp(self):
        """This property is to add up the stats and return Fantasy League Point"""
        points = self.pts + self.threep + self.fga*(-1) + self.fg*(2) + self.fta*(-1) + self.ft + self.trb + self.ast*(2) + self.stl*(4) + self.blk*(4) + self.tov*(-2)
        return (points)
    @property
    def cost(self):
        """This is going to divide the Salaray by the Fantasy League Points and return with $and , s"""
        if self.flp <= 0:
            return self.sal
        else:
            sal_per_flp =  "{:.2f}".format(self.sal/self.flp)
        return sal_per_flp

    
class Team(db.Model):
    """This data will contain data from the current season"""

    __tablename__='teams'

    id = db.Column(db.Integer,
            primary_key=True,
            autoincrement=True
    )

    name = db.Column(
            db.String,
            nullable = False,
            unique = True
    )
    team_image = db.Column(
            db.Text,
            nullable=False,
            default = '/static/images/basketball.jpeg'
    )
    user_id = db.Column(
            db.String,
            db.ForeignKey('users.username', ondelete='CASCADE'),
            nullable=False
    )
    
    assignments = db.relationship('TeamPlayers', backref = 'team', cascade = "all, delete-orphan")
    
    players = db.relationship('Stat', secondary='teamplayers', backref=db.backref('teams', lazy = 'dynamic'))

    @property
    def totalsal(self):
        """Add up the salaries of the players on our team"""

        total=0
        for self.player in self.players:
            total += (self.player.sal)
        return total

    @property
    def totalFlp(self):
        total = 0
        for self.player in self.players:
            total += (self.player.flp)
        return total
    

class TeamPlayers(db.Model):
    """Mapping teams to players"""

    __tablename__='teamplayers'

    id = db.Column(db.Integer,
         primary_key=True
    )
    team_id = db.Column(
        db.Integer,
        db.ForeignKey('teams.id', ondelete='cascade')
    )
    stats_id = db.Column(
        db.Integer,
        db.ForeignKey('stats.id', ondelete='cascade')
    )
    position = db.Column(
        db.String,
        nullable = False
    )
    
   