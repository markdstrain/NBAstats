from flask import Flask, render_template, redirect, session, flash, g
from models import db, connect_db, Stat, User, Team, TeamPlayers
from stats import Statistics
from flask_debugtoolbar import DebugToolbarExtension
from forms import LoginForm, RegisterForm, DeleteForm, TeamForm
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import IntegrityError
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql:///nba')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)
connect_db(app)


current_season = 2021
stats = Statistics()

@app.before_request
def add_user_to_user():
    """If we're logged in, add curr user to Flask Global."""
    if "username" in session:
        g.user = User.query.get(session["username"])
    else:
        g.user = None

@app.route('/')
def home_page():
    """This is the open in to the website(navigate,signup, signing, checkstuff out)"""
    return render_template('home.html')

@app.route('/about')
def about_page():
    """This page is going to try and describe what's going on with this web app"""
    return render_template('about.html')
@app.route('/all_players_stats')
def get_all():
    """Look at all players stats for the year"""
    pstats=Stat.query.all()

    return render_template('allPlayerStats.html',pstats=pstats)


@app.route('/register', methods=['GET','POST'])
def register():
    """We're gonna Register folks by providing them a form and then we're gonna handle their bizness"""
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            username = form.username.data
            password = form.password.data
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data

            user = User.register(username, password, email, first_name, last_name)

            db.session.commit()

        except IntegrityError:
            form.username.errors =["Username already taken"]
            return render_template('register.html', form=form)
        
        session['username'] = user.username

        return redirect(f'/users/{user.username}')
    
    return render_template('register.html', form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    """We're gonna show a form and handle the business of folks who already registered,"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f'/users/{session["username"]}')
        else:
            form.username.errors = ['Invalid username or passsword.']
            return render_template('login.html',form=form)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Here we're gonna log folks out"""
    session.pop("username")
    return redirect('/')


@app.route('/users/<username>')
def show_user_page(username):
    """This where the action happens"""
    
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    user = User.query.get(username)

    return render_template("users/show.html",user=user)
  

@app.route('/<player_bio>/stat/page')
def player_bio_page(player_bio):

    player = db.session.query(Stat).filter(Stat.plid==player_bio).first()
    player_bio=player_bio
    logs = stats.get_player_game_logs(player_bio)
    FLP = stats.getting_fantasy_points(player_bio)

    return render_template('playerBio.html', logs=logs, player_bio=player_bio, FLP=FLP, player=player)


@app.route('/create_team', methods=['GET','POST'])
def create_new_team():
    """We're gonna show a form and handle the business of folks who already registered,"""
    if not g.user:
        flash("Access unauthorized.","danger")
        return redirect('/')
    user = g.user
    form = TeamForm()
    if form.validate_on_submit():
        try:
            team = Team(name=form.name.data, team_image=form.team_image.data or Team.team_image.default.arg, user_id=user.username)
            db.session.add(team)
            db.session.commit()
        
        except IntegrityError:
            db.session.rollback()
            form.team_name.errors =["Team name already exists"]

            return render_template('users/createTeam.html', form=form)
        
        return redirect(f'/users/{user.username}')
        
    return render_template('users/createTeam.html', form=form)


@app.route('/<username>/<int:team_id>')
def show_team_page(username, team_id):
    """Show the teams page"""
    if not g.user:
        flash("Access unauthorized.","danger")
        return redirect('/')
    team = Team.query.get_or_404(team_id)
    point = db.session.query(TeamPlayers).filter_by(team_id=team_id,position ="PG").first() or None
    shoot = db.session.query(TeamPlayers).filter_by(team_id=team_id,position ="SG").first() or None
    small = db.session.query(TeamPlayers).filter_by(team_id=team_id,position ="SF").first() or None
    power = db.session.query(TeamPlayers).filter_by(team_id=team_id,position ="PF").first() or None
    center = db.session.query(TeamPlayers).filter_by(team_id=team_id,position ="C").first() or None
    guard = db.session.query(TeamPlayers).filter_by(team_id=team_id,position ="G").first() or None
    forward = db.session.query(TeamPlayers).filter_by(team_id=team_id,position ="F").first() or None
    u1 = db.session.query(TeamPlayers).filter_by(team_id=team_id,position ="u1").first() or None
    u2 = db.session.query(TeamPlayers).filter_by(team_id=team_id,position ="u2").first() or None
    u3 = db.session.query(TeamPlayers).filter_by(team_id=team_id,position ="u3").first() or None
    
    return render_template('/users/team.html', team=team, point=point, shoot=shoot, small=small, power=power, center=center, guard=guard, forward=forward, u1=u1, u2=u2,u3=u3)


@app.route('/<username>/<int:team_id>/<po>')
def adding_players_to_team(username, team_id, po):
    """Gonna add a player to the team"""
    if not g.user:
        flash("Access unauthorized.","danger")
        return redirect('/')
    team = Team.query.get_or_404(team_id)
    po = po
    if po == "u1" or po == "u2" or po == "u3":
        players = Stat.query.all()
        return render_template("/users/playerSelect.html", players=players,team=team, po=po)
    else:
        search = "%{}%".format(po)
        players = db.session.query(Stat).filter(Stat.pos.like(search)).all()
        
        return render_template("/users/playerSelect.html", players=players, team=team, po=po)


@app.route('/<int:team_id>/<int:player_id>/<po>', methods=['POST'])
def adding_teammate(team_id, player_id, po):
    """Gonna add a player to the team"""
    if not g.user:
        flash("Access unauthorized.","danger")
        return redirect('/')
    user = g.user
    team = Team.query.get_or_404(team_id)
    player = Stat.query.get_or_404(player_id)
    
    teamplayer = TeamPlayers(team_id= team.id, stats_id=player.id, position=po)
    db.session.add(teamplayer)
    db.session.commit()
        
    return redirect(f"/{user.username}/{team.id}")


@app.route('/<username>/<int:team_id>/<plid>/<int:player_id>')
def showing_individual_player_stats(username,team_id,plid,player_id):
    """This section is going to show stats on individual players on the team"""
    if not g.user:
        flash("Access unauthorized.","danger")
        return redirect('/')
    team = Team.query.get_or_404(team_id)
    player =  Stat.query.get_or_404(player_id)

    return render_template('users/player.html', player=player,team=team )

@app.route('/<int:team_id>/delete', methods =['POST'])
def delete_team(team_id):
    """Gonna Delete a Team From Users Profile"""
    if not g.user:
        flash("Access unauthorized.","danger")
        return redirect('/')
    
    team = Team.query.get(team_id)
    db.session.delete(team)
    db.session.commit()

    return redirect(f"/users/{g.user.username}")

@app.route('/<int:team_id>/edit', methods =['GET','POST'])
def edit_team(team_id):
    """Editing a teams id and photo"""
    if not g.user:
        flash("Access unauthorized.","danger")
        return redirect('/')
    user = g.user
    
    team = Team.query.get(team_id)
    form = TeamForm(obj=team)
    if form.validate_on_submit():
        try:
            team.name = form.name.data
            team.team_image = form.team_image.data or Team.team_image.default.arg

            db.session.commit()
        
        except IntegrityError:
            db.session.rollback()
            form.team_name.errors =["Team name already exists"]

            return render_template('users/createTeam.html', form=form)
        
        return redirect(f'/users/{user.username}')
        
    return render_template('users/editTeam.html', form=form, team=team)


@app.route('/<int:team_id>/<int:stats_id>/delete', methods =['POST'])
def remove_player_from_team(team_id, stats_id):
    """We're gonna remove a player from the team"""
    if not g.user:
        flash("Access unauthorized.","danger")
        return redirect('/')
    player = db.session.query(TeamPlayers).filter_by(team_id=team_id, stats_id=stats_id).first()
    db.session.delete(player)
    db.session.commit()

    return redirect(f"/{g.user.username}/{team_id}")


@app.route('/nba_players_not_acquired')
def this_my_area_to_see_what_output_looks_like():
    """This will go away I'm just using it to see what my data looks like"""
    
    # other_stuff = stats.updating_player_stats()
    other_stuff = stats.finding_missing_players()
    
    return render_template('testing.html', other_stuff=other_stuff)

