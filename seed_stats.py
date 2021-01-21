from models import Stat, db
from app import app, getting_player_is, populating_player_stats

#Create all tables I want to put this on a daily timer
db.drop_all()
db.create_all()

player_id = getting_player_ids()
player_stats = populating_player_stats()



for i in range(len(player_id)):
    s = Stat(plid=player_id[i], player=player_stats[i][0],pos=player_stats[i][1],age=int(player_stats[i][2],team=player_stats[i][3],
        g=int(player_stats[i][4]),gs=int(player_stats[i][5]), mp=int(player_stats[i][6]), fg=int(player_stats[i][7]), fga=int(player_stats[i][8]),
        fgp=int(player_stats[i][9]), threep=int(player_stats[i][10]), threepa=int(player_stats[i][11]), threeper=float(player_stats[i][12]),
        two=int(player_stats[i][13]), twoa=int(player_stats[i][14]), twoper=float(player_stats[i][15]), efg=float(player_stats[i][16]),
        ft=int(player_stats[i][17]), fta=int(player_stats[i][18]), ftper=float(player_stats[i][19]), orb=int(player_stats[i][20]),
        drb=int(player_stats[i][21]), trb=int(player_stats[i][22]), ast=int(player_stats[i][23]), stl=int(player_stats[i][24]), 
        blk=int(player_stats[i][25]), tov=int(player_stats[i][26]), pf=int(player_stats[i][27]), pts=int(player_stats[i][28]))
        
   print(s)
