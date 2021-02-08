from models import Stat, db
from app import app
from stats import Statistics
import schedule
import time
#Create all tables I want to put this on a daily timer

current_season = 2021
stats = Statistics()

player_stats = stats.populating_player_stats()
player_id = stats.getting_player_ids()
player_sal = stats.getting_an_array_of_salaries()


def update_stats():
    stats.updating_player_stats()
schedule.every().day.at("10:58").do(update_stats)
while True:
    schedule.run_pending()
    time.sleep(1)

