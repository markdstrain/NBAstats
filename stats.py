from bs4 import BeautifulSoup
from models import Stat,db
import pandas as pd
import requests, re


current_season = 2022
league_min = '$449,115'
class Statistics():

    def __init__(self, players=None, year=current_season):
        self.players = players
        self.year = year

    def get_table_headers(self,year=current_season): 
        """This function is to get the tabe headers for stats"""
    
        url = f'https://www.basketball-reference.com/leagues/NBA_{year}_totals.html'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find_all(class_="full_table")
        head = soup.find(class_="thead")
        column_names_raw=[head.text for item in head][0]
        column_names_clean = column_names_raw.replace("\n",",").split(",")[2:-1]

        all_players = []

        for i in range(len(table)):
            player_ = []
            for td in table[i].find_all("td"):
                player_.append(td.text) 
            all_players.append(player_)
        df = pd.DataFrame( all_players, columns = column_names_clean).set_index("Player")

        df.index = df.index.str.replace('*', '')

        return (column_names_clean) 
    
    
    def populating_player_stats(self, year=current_season):
        """This function scrapes basketball-reference.com for all player stats with tablle heads in the year that is given"""

        url = f'https://www.basketball-reference.com/leagues/NBA_{year}_totals.html'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find_all(class_="full_table")
        head = soup.find(class_="thead")
        column_names_raw=[head.text for item in head][0]
        column_names_clean = column_names_raw.replace("\n",",").split(",")[2:-1]


        all_players = []
        for i in range(len(table)):
            player_ = []
            for td in table[i].find_all("td"):
                player_.append(td.text) 
            all_players.append(player_)

        df = pd.DataFrame( all_players, columns = column_names_clean).set_index("Player")

        
        return(all_players)

    def getting_player_ids(self, year=current_season):
        """This function gets the ids in the same order populated by the populating_stats_function"""
    
        url = f'https://www.basketball-reference.com/leagues/NBA_{year}_totals.html'
        page = requests.get(url)
        soupier = BeautifulSoup(page.content,'lxml')
        csv_var = soupier.select('td[data-append-csv]')

        plid=[]

        for data in csv_var:
            plid.append(data['data-append-csv'])
        plid = list(dict.fromkeys(plid))

        return(plid)
    
    def get_table_headers_for_logs(self, players, year=current_season): 
        """This function is to get the tabe headers for stats"""


        url = f'https://www.basketball-reference.com/players/{players[0]}/{players}/gamelog/{year}'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find_all(class_="row_summerable sortable stats_table now_sortable")
        head = soup.find("thead")
        column_names_raw=[head.text for item in head][0]
        column_names_clean = column_names_raw.replace("\n",",").split(",")[2:-1]

        all_games = []
        for i in range(len(table)):
            game_ = []
            for td in table[i].find_all("td"):
                game_.append(td.text) 
            all_games.append(game_)
        df = pd.DataFrame(all_games, columns = column_names_clean).set_index("G")

        df.index = df.index.str.replace('*', '')

        return (column_names_clean)

    def get_player_game_logs(self, players, year=current_season):
        """"Here Im getting the player game logs for the season that is requested defaulted to current season"""

        url = f'https://www.basketball-reference.com/players/{players[0]}/{players}/gamelog/{year}'
        page = requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser')
        table = soup.find_all(['tr'],id=re.compile('^pgl_basic.'))

        all_games = []
        for i in range(len(table)):
            game_ = []
            for td in table[i].find_all(["th","td"]):

                game_.append(td.text) 
            all_games.append(game_)

        return(all_games)

    def getting_fantasy_points(self,players,year=current_season):
        """calculating fantasy league points here. This is good if you want to look at an individuals 
        game by game fantasy points. It scrapes and doesn't save to sql table."""
        table_data = self.get_player_game_logs(players,year)

        fantasy_array=[]
        for i in range(len(table_data)):
            points=0
            #Points Scored
            points+=(int(table_data[i][27])*1)
            #3 Pointers Made
            points+=(int(table_data[i][13])*1)
            #Field Goals Attempted
            points+=(int(table_data[i][11])*-1)
            #Field Goals Made
            points+=(int(table_data[i][10])*2)
            #Free Throws Attempted
            points+=(int(table_data[i][17])*-1)
            #Free Throw Made
            points+=(int(table_data[i][16])*1)
            #Rebounds Made
            points+=(int(table_data[i][21])*1)
            #Assists Made
            points+=(int(table_data[i][22])*2)
            #Steels Made
            points+=(int(table_data[i][23])*4)
            #Blocks Made
            points+=(int(table_data[i][24])*4)
            #Turn Overs Made
            points+=(int(table_data[i][25])*-2)

            fantasy_array.append(points)

        return fantasy_array
        

    def getting_an_array_fantasy_points(self,players):
        """Here I'm making an array of fantasy league points to populate my table this will only be helpful
        if I'm looking at players from past years. It won't be implemented until later when I can call on historical
        data"""
        fantasy_array=[]
        for i in range(len(players)):
            points=0
            #Points Scored
            points+=(int(players[i][28])*1)
            #3 Pointers Made
            points+=(int(players[i][10])*1)
            #Field Goals Attempted
            points+=(int(players[i][8])*-1)
            #Field Goals Made
            points+=(int(players[i][7])*2)
            #Free Throws Attempted
            points+=(int(players[i][18])*-1)
            #Free Throw Made
            points+=(int(players[i][17])*1)
            #Rebounds Made
            points+=(int(players[i][22])*1)
            #Assists Made
            points+=(int(players[i][23])*2)
            #Steels Made
            points+=(int(players[i][24])*4)
            #Blocks Made
            points+=(int(players[i][25])*4)
            #Turn Overs Made
            points+=(int(players[i][26])*-2)

            fantasy_array.append(points)

        return fantasy_array

    def getting_an_array_of_salaries(self):
        """I'm trying to scrape current years salary"""
        url = 'https://www.basketball-reference.com/contracts/players.html'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find_all(id="player-contracts")
        
        # This right here I'm calling all my players id from my SQL table
        pstats=self.getting_player_ids()
        # getting all the salaries that are known by the nba-reference
        salaries=[]
        for player in pstats:
            
            results = soup.find('td',{'data-append-csv': player})
            if results == None:
                sal= 'Unknown'
            else:
                sal = results.find_next_sibling('td',{'data-stat':'y1'})
                sal = sal.text
            salaries.append([player,sal])
        
        #here I'm changing unknown salaries and I'm setting them to found salaries or to a league minimum
        #will have to change every year
        for i in range(len(salaries)):
            
            if salaries[i][0]== 'cabocbr01':
                salaries[i][1]='$2,028,594'
            if salaries[i][0]== 'doziepj01':
                salaries[i][1]='$1,762,796'
            if salaries[i][0]=='makerth01':
                salaries[i][1]='$1,737,145'
            if salaries[i][0]=='morgaju01':
                salaries[i][1]='$1,517,981'
            if salaries[i][0]=='robinje01':
                salaries[i][1]='$3,737,520'
            if salaries[i][0]=='belljo01':
                salaries[i][1]='$1,845,433'
            if salaries[i][0]=='dotsode01':
                salaries[i][1]='$2,000,000'
            if salaries[i][0]=='masonfr01':
                salaries[i][1]='$1,378,242'
            if salaries[i][0]=='pelleno01':
                salaries[i][1]='$1,079,322'
            if salaries[i][1]=='Unknown'or salaries[i][1]=='':
                salaries[i][1]=league_min
        
        #turning salaries to an integer
        for i in range(len(salaries)):
            salaries[i][1]=int(salaries[i][1][1:].replace(',',''))
        return salaries

    def updating_player_stats(self):

        pstats=Stat.query.all()
        player_stats = self.populating_player_stats()

        #make sure I don't have any empty strings in function
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
        
        #now match player from sql table with player from scraping and update the stats in sql table
        #Also I'm doing this way so that new players on weird short contracts won't be added and cause it to crash
        for stats in pstats:
            for j in range(len(player_stats)):
                if stats.player == player_stats[j][0]:
                    
                    stats.age = int(player_stats[j][2])
                    stats.team = player_stats[j][3]
                    stats.g = int(player_stats[j][4])
                    stats.gs = int(player_stats[j][5])
                    stats.mp = int(player_stats[j][6])
                    stats.fg = int(player_stats[j][7])
                    stats.fga = int(player_stats[j][8])
                    stats.fgp = float(player_stats[j][9])
                    stats.threep = int(player_stats[j][10])
                    stats.threepa = int(player_stats[j][11])
                    stats.threepper = float(player_stats[j][12])
                    stats.two = int(player_stats[j][13])
                    stats.twoa = int(player_stats[j][14])
                    stats.twoper = float(player_stats[j][15])
                    stats.efg = float(player_stats[j][16])
                    stats.ft = int(player_stats[j][17])
                    stats.fta = int(player_stats[j][18])
                    stats.ftper = float(player_stats[j][19])
                    stats.orb = int(player_stats[j][20])
                    stats.drb = int(player_stats[j][21])
                    stats.trb = int(player_stats[j][22])
                    stats.ast = int(player_stats[j][23])
                    stats.stl = int(player_stats[j][24])
                    stats.blk = int(player_stats[j][25])
                    stats.tov = int(player_stats[j][26])
                    stats.pf = int(player_stats[j][27])
                    stats.pts = int(player_stats[j][28])

                    db.session.commit()
                    
        return('done')
    
    def finding_missing_players(self):

        pstats=Stat.query.all()
        player_stats = self.populating_player_stats()

        #finding new players that haven't been added

        missing=[]
        for j in range(len(player_stats)):
            missing.append(player_stats[j][0])
        for players in pstats:    
            missing.remove(players.player)
        
                    
        return(missing)   