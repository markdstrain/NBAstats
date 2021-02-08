from app import app
from models import db, Stat
from stats import Statistics

   
s1=Stat(plid='pelleno01',
    player= 'Norvel Pelle',
    pos='C',
    age=21,
    team='ORL',
    g=1,
    gs=0,
    mp=2,
    fg=0,
    fga=0,
    fgp=float(0),
    threep=0,
    threepa=0,
    threepper=float(0),
    two=0,
    twoa=0,
    twoper=float(0),
    efg=float(0),
    ft=0,
    fta=0,
    ftper=float(0),
    orb=0,
    drb=0,
    trb=0,
    ast=0,
    stl=0,
    blk=0,
    tov=1,
    pf=0,
    pts=0,
    sal=1079322)

db.session.add(s1)
db.session.commit()