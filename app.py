from flask import Flask, render_template, redirect, session, flash
from models import db, connect_db, Stat
from stats import Stat
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///nba'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)
connect_db(app)


current_season = 2021
stats = Stat()



@app.route('/')
def hompe_page():
    
    column_names_clean = stats.get_table_headers(2021)
    all_players = stats.populating_player_stats(2021)
    plid = stats.getting_player_ids(2021)
    FLP = stats.getting_an_array_fantasy_points(all_players)
    return render_template('home.html',th=column_names_clean, all_players=all_players,plid=plid,FLP=FLP)
    
@app.route('/<player_bio>/stat/page')
def player_bio_page(player_bio):
    player=player_bio
    th = stats.get_table_headers_for_logs(player)
    logs = stats.get_player_game_logs(player)
    FLP = stats.getting_fantasy_points(player)

    return render_template('playerBio.html', logs=logs, th=th, player_bio=player, FLP=FLP)


@app.route('/testing/<player_bio>')
def this_my_area_to_see_what_output_looks_like(player_bio):
    """This will go away I'm just using it to see what my data looks like"""
    
    stuff = getting_an_array_fantasy_points(2021)
    return render_template('testing.html',stuff=stuff )