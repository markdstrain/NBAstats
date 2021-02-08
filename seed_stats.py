from models import Stat, db
from app import app
from stats import Statistics
#Create all tables I want to put this on a daily timer

current_season = 2021
stats = Statistics()

db.drop_all()
db.create_all()

player_stats = stats.populating_player_stats()
player_id = stats.getting_player_ids()
player_sal = stats.getting_an_array_of_salaries()
for j in range(len(player_stats)):
    

    if player_stats[j][9]=='':
        player_stats[j][9]= .000
    if player_stats[j][12]=='':
        player_stats[j][12]= .000
    if player_stats[j][15]=='':
        player_stats[j][15]=.000
    if player_stats[j][16]=='':
        player_stats[j][16]= .000
    if player_stats[j][19]=='':
        player_stats[j][19]= .000
 


for i in range(len(player_id)):
   
    s= Stat(plid=player_id[i], player= player_stats[i][0],pos=player_stats[i][1],age=int(player_stats[i][2]),
        team=player_stats[i][3],g=int(player_stats[i][4]),gs=int(player_stats[i][5]),mp=int(player_stats[i][6]),
        fg=int(player_stats[i][7]),fga=int(player_stats[i][8]),fgp=float(player_stats[i][9]),threep=int(player_stats[i][10]),
        threepa=int(player_stats[i][11]),threepper=float(player_stats[i][12]),two=int(player_stats[i][13]),
        twoa=int(player_stats[i][14]),twoper=float(player_stats[i][15]),efg=float(player_stats[i][16]),
        ft=int(player_stats[i][17]),fta=int(player_stats[i][18]),ftper=float(player_stats[i][19]),
        orb=int(player_stats[i][20]),drb=int(player_stats[i][21]),trb=int(player_stats[i][22]),ast=int(player_stats[i][23]),
        stl=int(player_stats[i][24]),blk=int(player_stats[i][25]),tov=int(player_stats[i][26]),pf=int(player_stats[i][27]),
        pts=int(player_stats[i][28]),sal=int(player_sal[i][1]))
    
    db.session.add(s)
    db.session.commit()
# for i in range(len(player_id)):
#     s= Stat(plid=player_id[i], player= player_stats[i][0],pos=player_stats[i][1],age=player_stats[i][2],team=player_stats[i][3],g=player_stats[i][4],gs=player_stats[i][5],mp=player_stats[i][6],fg=player_stats[i][7],fga=player_stats[i][8],fgp=player_stats[i][9],threep=player_stats[i][10],threepa=player_stats[i][11],threepper=player_stats[i][12],two=player_stats[i][13],twoa=player_stats[i][14],twoper=player_stats[i][15],efg=player_stats[i][16],ft=player_stats[i][17],fta=player_stats[i][18],ftper=player_stats[i][19],orb=player_stats[i][20],drb=player_stats[i][21],trb=player_stats[i][22],ast=player_stats[i][23],stl=player_stats[i][24],blk=player_stats[i][25],tov=player_stats[i][26],pf=player_stats[i][27],pts=player_stats[i][28])
#     populate.append(s)
 



