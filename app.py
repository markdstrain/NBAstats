from flask import Flask, render_template, redirect, session, flash
from bs4 import BeautifulSoup
import pandas as pd
from flask_debugtoolbar import DebugToolbarExtension
import os, re
import requests





app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///nba"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)
# connect_db(app)


current_season = 2021

def get_table_headers(year=current_season): 
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
    

def populating_player_stats(year=current_season):
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


def getting_player_ids(year=current_season):
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

def get_table_headers_for_logs(player,year=current_season): 
    """This function is to get the tabe headers for stats"""
    
    
    url = f'https://www.basketball-reference.com/players/{player[0]}/{player}/gamelog/{year}'
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

def get_player_game_logs(player,year=current_season):
    """"Here Im getting the player game logs for the season that is requested defaulted to current season"""

    url = f'https://www.basketball-reference.com/players/{player[0]}/{player}/gamelog/{year}'
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

def getting_fantasy_points(player,year=current_season):
    """calculating fantasy league points here"""
    table_data = get_player_game_logs(player,year)
    
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
        

def getting_an_array_fantasy_points(players):
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

@app.route('/')
def hompe_page():
    
    column_names_clean = get_table_headers(2021)
    all_players = populating_player_stats(2021)
    plid = getting_player_ids(2021)
    FLP = getting_an_array_fantasy_points(all_players)
    return render_template('home.html',th=column_names_clean, all_players=all_players,plid=plid,FLP=FLP)
    
@app.route('/<player_bio>/stat/page')
def player_bio_page(player_bio):
    th = get_table_headers_for_logs(player_bio)
    logs = get_player_game_logs(player_bio)
    FLP = getting_fantasy_points(player_bio)

    return render_template('playerBio.html', logs=logs, th=th, player_bio=player_bio, FLP=FLP)


@app.route('/testing/<player_bio>')
def this_my_area_to_see_what_output_looks_like(player_bio):
    """This will go away I'm just using it to see what my data looks like"""
    
    stuff = getting_an_array_fantasy_points(2021)
    return render_template('testing.html',stuff=stuff )