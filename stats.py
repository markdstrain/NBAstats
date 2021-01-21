from bs4 import BeautifulSoup
import pandas as pd
import requests, re


current_season = 2021
class Stat():

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

        df.index = df.index.str.replace('*', '')
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
        """calculating fantasy league points here"""
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
        """Here I'm making an array of fantasy league points to populate my table"""
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