from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os, sqlalchemy, ssl, psycopg2

Base = declarative_base()

# Players Table
class Player(Base):
    __tablename__ = 'players'
    player_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    role = Column(String(50))
    batting_style = Column(String(50))
    bowling_style = Column(String(50))
    country = Column(String(50), nullable=False)
    dob = Column(Date)

# Teams Table
class Team(Base):
    __tablename__ = 'teams'
    team_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    country = Column(String(50), nullable=False)
    gender = Column(String(10))

# Stadiums Table
class Stadium(Base):
    __tablename__ = 'stadiums'
    stadium_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    city = Column(String(50))
    country = Column(String(50), nullable=False)
    capacity = Column(Integer)

# Tournaments Table
class Tournament(Base):
    __tablename__ = 'tournaments'
    tournament_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    start_date = Column(Date)
    end_date = Column(Date)
    format = Column(String(20))
    host_country = Column(String(50))
    winner_team_id = Column(Integer, ForeignKey('teams.team_id'))
    runner_up_team_id = Column(Integer, ForeignKey('teams.team_id'))
    shared_winner = Column(Boolean, default=False)
    # add man of the series, highest wicket taker, highest runs

# Matches Table
class Match(Base):
    __tablename__ = 'matches'
    match_id = Column(Integer, primary_key=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.tournament_id'))
    stadium_id = Column(Integer, ForeignKey('stadiums.stadium_id'))
    match_date = Column(Date, nullable=False)
    match_format = Column(String(20))
    team1_id = Column(Integer, ForeignKey('teams.team_id'))
    team2_id = Column(Integer, ForeignKey('teams.team_id'))
    toss_winner_id = Column(Integer, ForeignKey('teams.team_id'))
    toss_decision = Column(String(10))
    winner_team_id = Column(Integer, ForeignKey('teams.team_id'))
    result = Column(String(50))
    man_of_the_match = Column(Integer, ForeignKey('players.player_id'))

# Innings Table
class Innings(Base):
    __tablename__ = 'innings'
    innings_id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.match_id'))
    batting_team_id = Column(Integer, ForeignKey('teams.team_id'))
    bowling_team_id = Column(Integer, ForeignKey('teams.team_id'))
    runs_scored = Column(Integer)
    wickets_lost = Column(Integer)
    overs_played = Column(Float)
    extras = Column(Integer)
    total_score = Column(Integer)
    fall_of_wickets = Column(String(100))
    top_scorer_id = Column(Integer, ForeignKey('players.player_id'))
    top_bowler_id = Column(Integer, ForeignKey('players.player_id'))

# Balls Table
class Ball(Base):
    __tablename__ = 'balls'
    ball_id = Column(Integer, primary_key=True)
    innings_id = Column(Integer, ForeignKey('innings.innings_id'))
    ball_number = Column(Integer)
    batsman_id = Column(Integer, ForeignKey('players.player_id'))
    bowler_id = Column(Integer, ForeignKey('players.player_id'))
    non_striker_id = Column(Integer, ForeignKey('players.player_id'))
    runs_scored = Column(Integer)
    runs_type = Column(String(20))
    extras = Column(Integer)
    wicket = Column(String(20))
    wicket_type = Column(String(20))
    wicket_player_id = Column(Integer, ForeignKey('players.player_id'))
    wicket_fielder_id = Column(Integer, ForeignKey('players.player_id'))
    wicket_keeper_id = Column(Integer, ForeignKey('players.player_id'))

# PlayerStatsInnings Table
class PlayerStatsInnings(Base):
    __tablename__ = 'player_stats_innings'
    player_stats_innings_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.player_id'))
    match_id = Column(Integer, ForeignKey('matches.match_id'))
    innings_id = Column(Integer, ForeignKey('innings.innings_id'))
    runs_scored = Column(Integer)
    balls_faced = Column(Integer)
    fours = Column(Integer)
    sixes = Column(Integer)
    strike_rate = Column(Float)
    overs_bowled = Column(Float)
    runs_conceded = Column(Integer)
    wickets_taken = Column(Integer)
    economy = Column(Float)
    catches = Column(Integer)
    run_outs = Column(Integer)
    stumpings = Column(Integer)

# PlayerVsPlayerInnings Table
class PlayerVsPlayerInnings(Base):
    __tablename__ = 'player_vs_player_innings'
    player_vs_player_innings_id = Column(Integer, primary_key=True)
    batsman_id = Column(Integer, ForeignKey('players.player_id')) # in case of fielding, this will be the fielder, when the other player is out
    bowler_id = Column(Integer, ForeignKey('players.player_id'))
    match_id = Column(Integer, ForeignKey('matches.match_id'))
    innings_id = Column(Integer, ForeignKey('innings.innings_id'))
    runs_scored = Column(Integer)
    balls_faced = Column(Integer)
    fours = Column(Integer)
    sixes = Column(Integer)
    strike_rate = Column(Float)
    overs_bowled = Column(Float)
    runs_conceded = Column(Integer)
    wickets_taken = Column(Integer)
    economy = Column(Float)
    catches = Column(Integer)
    run_outs = Column(Integer)
    stumpings = Column(Integer)

class PlayerStatsOver(Base):
    __tablename__ = 'player_stats_over'
    player_stats_over_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.player_id'))
    match_id = Column(Integer, ForeignKey('matches.match_id'))
    innings_id = Column(Integer, ForeignKey('innings.innings_id'))
    over_number = Column(Integer)
    runs_scored = Column(Integer)
    balls_faced = Column(Integer)
    fours = Column(Integer)
    sixes = Column(Integer)
    strike_rate = Column(Float)
    runs_conceded = Column(Integer)
    wickets_taken = Column(Integer)
    economy = Column(Float)
    catches = Column(Integer)
    run_outs = Column(Integer)
    stumpings = Column(Integer)

# Patnership Table
class Partnership(Base):
    __tablename__ = 'partnerships'
    partnership_id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.match_id'))
    innings_id = Column(Integer, ForeignKey('innings.innings_id'))
    player1_id = Column(Integer, ForeignKey('players.player_id'))
    player2_id = Column(Integer, ForeignKey('players.player_id'))
    runs_scored = Column(Integer)
    balls_faced = Column(Integer)
    fours = Column(Integer)
    sixes = Column(Integer)
    out = Column(String(20))


SQL_SERVER = "34.47.131.52"
SQL_DATABASE = "cricdata"
SQL_USER = "postgres"
SQL_PASSWORD = "sagar12@" 
SQL_PORT = "5432"

host = os.getenv("SQL_HOST") if os.getenv("SQL_HOST") else SQL_SERVER
dbname = os.getenv("SQL_DB") if os.getenv("SQL_DB") else SQL_DATABASE
user = os.getenv("SQL_USER") if os.getenv("SQL_USER") else SQL_USER
password = os.getenv("SQL_PASSWORD") if os.getenv("SQL_PASSWORD") else SQL_PASSWORD
port = os.getenv("SQL_PORT") if os.getenv("SQL_PORT") else SQL_PORT

try:
    engine = sqlalchemy.create_engine(
        # Equivalent URL:
        # postgresql+pg8000://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=user,
            password=password,
            host=host,
            port=port,
            database=dbname,
        ),
    )

    # Test the connection
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT version()")).fetchone()
        version = result[0]
        print(f"PostgreSQL version: {version}")        
except psycopg2.Error as e:
    print(f"Database connection error: {e}")
    raise




