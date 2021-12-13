from models import Stat, db
from app import app
from stats import Statistics
import schedule
import time
#Create all tables I want to put this on a daily timer

current_season = 2022
stats = Statistics()

player_stats = stats.populating_player_stats()
player_id = stats.getting_player_ids()
player_sal = stats.getting_an_array_of_salaries()



stats.updating_player_stats()


