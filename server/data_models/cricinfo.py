from typing import Optional, Type
from enum import Enum
from pydantic import BaseModel
from id_mapper import IdMapper
import asyncio

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

class CricInfoAllRound(BaseModel):
    '''
    class_: int # 1 for test, 2 for odi, 3 for t20, 11 for all, choose 11 for any two also, don't give list of values
    team: list[int]   # list of countries
    opposition: list[int]   # list of opposition countries
    home_or_away: list[int]   # 1, 2, 3 for home, away, neutral
    host: list[int]   # list of host countries
    continent: list[int]   # list of continents {"all continents": 0, "Africa": 1, "Americas": 2, "Asia": 3, "Europe": 4, "Oceania": 5}
    ground: list[int]   # list of grounds
    span: list[str]   # from and to date [from, to], should of format dd-mm-yyyy
    season: list[str]   # list of seasons
    series: list[int]   # list of series
    trophy: list[int]   # list of trophies
    tournament_type: list[int]   # list of tournament types 2 for 2 team, 3 for 3-4 team, 5 for 5+ teams
    match_type: list[int]   # list of match types {"tournament finals":1,"tournament cons. finals":2,"tournament semi-finals":3,"tournament quarter-finals":4,"preliminary quarter-finals":5,"qualifying final":7,"preliminary matches":0}
    floodlit: list[int]   # {"day match":1,"day/night match":2,"night match":3}
    result: list[int]   # {"won match":1,"lost match":2,"tied match":3,"drawn match":4,"no result":5}
    toss: int   # toss results 1 for win, 2 for loss
    batting_fielding_first: int   # batting or fielding first 1 for batting, 2 for fielding
    captain: int   # 1 for captain, 0 for not captain
    keeper: int   # 1 for keeper, 0 for not keeper
    debut_or_last: int   {"career debut":1,"last career match":2,"team debut":3,"last match for team":4}
    batting_hand: int   # 1 for right, 2 for left
    bowling_hand: int   # 1 for right hand, 2 for left hand
    bowling_pacespin: int   # 1 for pace, 2 for spin, 3 for mixed
    player_age: list[int]   # from and to age, [from, to], if only from then [from, -1], if only to then [-1, to]
    innings_number: list[int]   # list of innings numbers {"1st innings":1,"2nd innings":2,"3rd innings":3,"4th innings":4}
    player_involve: list[int]   # list of players that are involved in the match
    captain_involve: list[int]   # list of captains that are involved in the match
    runs_scored: list[int]   # Runs scored in innings [from, to], this is not a overall runs scored, should be only used for per innings filter
    batting_position: list[int]   # from and to batting position, should be only used for per innings filter
    dismissal: list[int]   # list of dismissals {"0":"all types","1":"caught","2":"bowled","3":"leg before wicket","4":"run out","5":"stumped","6":"hit wicket","7":"handled the ball","8":"obstructing the field","9":"retired out","10":"not out","11":"retired not out (hurt)"}
    outs: int   # {"out":1,"not out/absent/dnb":0}
    balls_bowled: list[int]   # Balls bowled in innings [from, to]
    runs_conceded: list[int]   # Runs conceded in innings [from, to]
    wickets_taken: list[int]   # Wickets taken in innings [from, to]
    bowling_position: list[int]   # from and to bowling position [from, to]
    catches_taken: list[int]   # Catches taken in innings [from, to] 
    stumpings_made: list[int]   # Stumpings made in innings [from, to]

    The following fields are most important, as they decide how the stats are shown

    First field we need to choose is "type"

    type: str

    Type determines what type of stats we are looking for, the possible values are

    {
        "Batting": "batting", # this is for players batting stats, player runs, average, strike rate etc
        "Bowling": "bowling", # this is for players bowling stats, player wickets, average, economy, strike rate etc
        "Fielding": "fielding", # this is for players fielding stats, player catches, runouts, stumpings etc
        "All Round": "allround", # this is for players all round stats, batting, bowling and fielding combined
        "Team": "team" # this is for team stats, this is team specific stats, like India stats, Australia stats etc
        "Partnership": "fow" # this is for partnership stats, like paternship for a wicket etc
        "Umpire and referee": "official" # this is for umpire and referee stats, like umpire in test, odi etc
        "Aggregate": "aggregate" # this is for aggregated stats, like total matches, total runs, total wickets by a team, country... not a player specific stats
    }

    The second field we need to choose is "view"

    view: str

    View field is the most important field, as it decides how the stats are shown, the possible values are

    These are possible values for each type, I have included only those which are possible for each type, like for umpire, partnership, team, aggregate, we can't show innings wise stats, so I have specically mentioned which are possible and not
    {{
        "Overall figures": "default", # this view by overall figures for a player or like total runs, total wickets or for a team, like total matches, total wins etc 
        "Innings by innings list": "innings", # this is innings by innings list  view --> Not possible for ["patnership", "umpire", "aggregate"] types
        "Match totals": "match", # this is match by match list view, like runs scored in that match, wickets taken in that match by that player for all selected matches and players
        "Series averages": "series", # view by series
        "Ground averages": "ground", # view by ground
        "By host country": "host", # view by host country 
        "By opposition team": "opposition", # view by opposition team --> Not possible for ["aggregate"] types
        "By year of match start": "year", # view by year
        "By season": "season" # view by season
        "Match results": "results", # match by match results view ---> only for ["allround", "team", "aggregate"] types
        "Match and series awards": "awards", # view by match and series awards ---> only for ["allround", "team", "aggregate"] types
        "Patnership list": "partnership", # partnership list ---> only for ["partnership"] types
        "Overall Extras": "extras", # overall extras  ---> only for ["team" and "allround"] types
        "Extras by innings": "extras_innings", # extras by innings ---> only for ["team", "aggregate"] types
    }}
    '''
    type: Optional[str] = "allround" # batting for batting stats, bowling for bowling stats, allround for allround stats, fielding for fielding stats, team for team stats
    class_: Optional[int] = 11  # 1 for test, 2 for odi, 3 for t20, 11 for all
    team: Optional[list[int]] = None  # list of countries
    opposition: Optional[list[int]] = None  # list of opposition countries
    home_or_away: Optional[list[int]] = None  # 0, 1, 2 for home, away, neutral
    host: Optional[list[int]] = None  # list of host countries
    continent: Optional[list[int]] = None  # list of continents
    ground: Optional[list[int]] = None  # list of grounds, need to main cache
    span: Optional[list[str]] = None  # from and to date
    season: Optional[list[str]] = None  # list of seasons, need to main cache
    series: Optional[list[int]] = None  # list of series, need to main cache
    trophy: Optional[list[int]] = None  # list of trophies, need to main cache
    tournament_type: Optional[list[int]] = None  # list of tournament types, 0 for 2 team, 1 for 3-4 team, 2 for 5+ teams
    match_type: Optional[list[int]] = None  # list of match types
    floodlit: Optional[list[int]] = None  # {"day match":1,"day/night match":2,"night match":3}
    result: Optional[list[int]] = None  # {"won match":1,"lost match":2,"tied match":3,"drawn match":4,"no result":5}
    toss: Optional[int] = None  # toss results, 0 for win, 1 for loss
    batting_fielding_first: Optional[int] = None  # batting or fielding first, 0 for batting, 1 for fielding
    captain: Optional[int] = None  # 1 for captain, 0 for not captain
    keeper: Optional[int] = None  # 1 for keeper, 0 for not keeper
    debut_or_last: Optional[list[int]] = None  # 0 career debut  1 last career match  2 team debut  3 last match for team
    batting_hand: Optional[int] = None  # 1 for right hand, 2 for left hand
    bowling_hand: Optional[int] = None  # 1 for right hand, 2 for left hand
    bowling_pacespin: Optional[int] = None  # 1 for pace, 2 for spin, 3 for mixed
    player_age: Optional[list[int]] = None  # from and to age, [from, to], if only from then [from, -1], if only to then [-1, to]
    innings_number: Optional[list[int]] = None  # list of innings numbers {"1st innings":1,"2nd innings":2,"3rd innings":3,"4th innings":4}
    player_involve: Optional[list[int]] = None  # list of players that are involved in the match
    player_not_involve: Optional[list[int]] = None  # list of players that are not involved in the match #TODO: need to check the format
    captain_involve: Optional[list[int]] = None  # list of captains that are involved in the match
    captain_not_involve: Optional[list[int]] = None  # list of captains that are not involved in the match
    runs_scored: Optional[list[int]] = None  # Runs scored in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    batting_position: Optional[list[int]] = None  # from and to batting position [from, to] if only from then [from, -1], if only to then [-1, to]
    dismissal: Optional[list[int]] = None  # list of dismissals, need to main cache
    outs: Optional[int] = None  # {"out":1,"not out/absent/dnb":0}
    balls_bowled: Optional[list[int]] = None  # Balls bowled in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    runs_conceded: Optional[list[int]] = None  # Runs conceded in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    wickets_taken: Optional[list[int]] = None  # Wickets taken in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    bowling_position: Optional[list[int]] = None  # from and to bowling position [from, to] if only from then [from, -1], if only to then [-1, to]
    catches_taken: Optional[list[int]] = None  # Catches taken in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    stumpings_made: Optional[list[int]] = None  # Stumpings made in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    view: Optional[str] = None  # How to show the stats {"Overall figures":"","Innings by innings list":"innings","Match totals":"match","Match results":"results","Match and series awards":"awards","Series averages":"series","Ground averages":"ground","By host country":"host","By opposition team":"opposition","By year of match start":"year","By season":"season"}
    groupby: Optional[str] = None  # Group the stats by for individual players, we need not to use this, {"individual players":"","each team innings":"innings","each match":"match","each series":"series","each tour":"tour","team":"team","opposition team":"opposition","each ground":"ground","host country":"host","host continent":"continent","year of match start":"year","season":"season","decade of match":"decade","overall aggregate":"overall"}
    result_qualifications: Optional[str] = None  # We can set min/max values for the results to qualify, possible options
    qual_value: Optional[list[int]] = None  # The value for the result qualification, [from, to] if only from then [from, -1], if only to then [-1, to]
    orderby: Optional[str] = None  # Order the results by {"matches":"matches played","innings":"innings batted","notouts":"not outs","outs":"batting dismissals","runs":"runs scored","minutes":"minutes batted","batting_average":"batting average","balls_faced":"balls faced","batting_strike_rate":"batting strike rate","hundreds":"hundreds scored","fifty_plus":"scores of fifty or more","ducks":"ducks scored","fours":"boundary fours","sixes":"boundary sixes","innings_bowled":"innings bowled in","balls":"balls bowled","maidens":"maidens earned","conceded":"runs conceded","wickets":"wickets taken","bowling_average":"bowling average","economy_rate":"economy rate","bowling_strike_rate":"bowling strike rate","four_plus_wickets":"four wickets in an inns","five_wickets":"five wickets in an inns","ten_wickets":"ten wickets in a match","matches_keeper":"matches as a keeper","matches_fielder":"matches as a fielder","innings_fielded":"innings fielded","dismissals":"fielding dismissals made","caught":"catches taken","stumped":"stumpings made","caught_keeper":"catches as a keeper","caught_fielder":"catches as a fielder","dismissals_per_inns":"dismissals per innings","allround_average":"batting - bowling average"}

    def get_query_url(self):
        query_url = "https://stats.espncricinfo.com/ci/engine/stats/index.html?template=results"

        query_url += build_url(self.__dict__)

        return query_url


class CricInfoPlayer(BaseModel):
    '''
    player: int # id of the player
    class_: int # 1 for test, 2 for odi, 3 for t20, 11 for all, choose 11 for any two also, don't give list of values, you must always provide this field
    opposition: list[int]   # list of opposition countries
    home_or_away: list[int]  # 0, 1, 2 for home, away, neutral
    host: list[int]  # list of host countries
    continent: list[int]  # list of continents
    ground: list[int]  # list of grounds
    span: list[str]   # from and to date
    season: list[str]   # list of seasons    
    series: list[int]  # list of series
    trophy: list[int]  # list of trophies
    tournament_type: list[int]  # list of tournament types, 0 for 2 team, 1 for 3-4 team, 2 for 5+ teams
    final_type: list[int]  # list of final types {"all types":"","tournament finals":"1","tournament semi-finals":"3","tournament quarter-finals":"4","preliminary quarter-finals":"5","preliminary matches":"0"}
    floodlit: list[int]   # {"day match":1,"day/night match":2,"night match":3}
    result: list[int]  # {"won match":1,"lost match":2,"tied match":3,"drawn match":4,"no result":5}
    toss: int   # toss results, 0 for win, 1 for loss
    batting_fielding_first: int]   # batting or fielding first, 0 for batting, 1 for fielding
    captain: int   # If the current player is captain 1 for captain, 0 for not captain, Only the current query player not the other involved players
    keeper: int   # If the current player is keeper 1 for keeper, 0 for not keeper, Only the current query player not the other involved players
    debut_or_last: list[int]  # 0 career debut  1 last career match  2 team debut  3 last match for team
    player_age: list[int]  # from and to age, [from, to], if only from then [from, -1], if only to then [-1, to]
    innings_number: list[int]  # list of innings numbers {"1st innings":1,"2nd innings":2,"3rd innings":3,"4th innings":4}
    player_involve: list[int]  # list of players that are involved in the match
    captain_involve: list[int]  # list of captains that are involved in the match
    runs_scored: list[int]  # Runs scored in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    batting_position: list[int]  # from and to batting position [from, to] if only from then [from, -1], if only to then [-1, to]
    dismissal: list[int]  # list of dismissals, need to main cache
    outs: int   # {"out":1,"not out/absent/dnb":0}
    balls_bowled: list[int]  # Balls bowled in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    runs_conceded: list[int]  # Runs conceded in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    wickets_taken: list[int]  # Wickets taken in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    bowling_position: list[int]  # from and to bowling position [from, to] if only from then [from, -1], if only to then [-1, to]
    catches_taken: list[int]  # Catches taken in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    stumpings_made: list[int]  # Stumpings made in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    
    Field: "type" : str

    Possible values:
    {{
        "All Round": "allround" # this is for all round stats or all stats, like whole carrer summaries
        "Batting": "batting" # this is for batting stats, like runs, average, strike rate etc
        "Bowling": "bowling" # this is for bowling stats, like wickets, average, economy, strike rate etc
        "Fielding": "fielding" # this is for fielding stats, like catches, runouts, stumpings etc
    }}

    Now once you are able to provide the type of the view, you need to choose how are representing the data, is it all matches combined or is it innings wise or is it year wise or is it series wise, bowler wise etc.
    
    Field: "view" : str

    Now based on the type of the view you selected above, you need to provide the view field, which is the representation of the data.

    For all types few are common fields

    {{
        "Carrer Summary": "default" # this is for all matches combined for the player, like player stats against all oppositions, all grounds etc
        "Innings": "innings" # this is for innings wise stats, used for per innings stats like highest score, best bowling etc
        "Match": "match" # this is for match wise stats, used for match wise stats like runs, wickets etc, innings and matches are different in test, where one match can have 2 innings
        "Series Average": "series" # this is for series wise stats, used for series wise stats like runs, wickets etc
        "Ground Average": "ground" # this is for ground wise stats, used for ground wise stats like runs, wickets etc
        "Cumulative Average": "cumulative" # this is for cumulative stats, used for cumulative stats like runs, wickets , from starting of his carrer, how did his average, strike rate etc changed
        "Reverse Cumulative Average": "reverse_cumulative" # this is for reverse cumulative stats, used for reverse cumulative stats like runs, wickets etc, from the end of his carrer, how did his average, strike rate etc changed
    }}

    For Overall View few more fields are there
    {{
        "Match Result": "results" # this is for match result wise stats, used for match result wise stats like runs in wins, wickets in wins etc
        "Match Awards": "awards_match" # this is for match awards wise stats, used for match awards wise stats
        "Series Awards": "awards_series" # this is for series awards wise stats, used for series awards wise stats
    }}


    For Batting few more fields are there
    {{
        "Bowler Summary": "bowler_summary" # this is for bowler wise stats, used for comparing a player vs a bowler stats
        "Partnership Summary": "fow_summary" # this is view based on partnerships, like 1st wicket partnership, 2nd wicket partnership etc
        "Partnership List": "fow_list" # this is view based on partnerships, all partnerships for the given player
        "Dismissal Summary": "dismissal_summary" # this is view based on dismissals, like caught, bowled, lbw , what type of bowlers, positions where the player got out etc
        "Dismissal List": "dismissal_list" # this is view based on dismissals, all dismissals for the given player
        "Fielder Summary": "fielder_summary" # this is view based on fielding, like catches, runouts, stumpings for the given player by the fielder
    }}

    For Bowling few more fields are there
    {{
        "Wickets Summary": "wickets_summary" # this is view based on wickets, like wickets taken at what position, what type of batsmen etc
        "Batter Dismissed Summary": "batsman_summary" # this is view based on batsmen dismissed, like how many times a player got a batsman out, what was his average, strike rate etc
        "Fielder summary": "fielder_summary" # this is view based on fielding, like catches, runouts, stumpings for the given player by the fielder
        "List of Wickets": "dismissal_list" # this is view based on wickets, all wickets taken by the player
    }}

    For Fielding few more fields are there
    {{
        "dismissal_summary": "dismissal_summary" # this is view based on dismissals, like catches, runouts, stumpings for the given player
        "bowler_summary": "bowler_summary" # this is view based on bowlers, like how many times a player took a catch of a bowler, what was the bowler's average, strike rate etc
        "batsman_summary": "batsman_summary" # this is view based on batsmen, like how many times a player took a catch of a batsman, what was the batsman's average, strike rate etc
        "dismissal_list": "dismissal_list" # this is view based on dismissals, all dismissals for the given player
    }}

    Field: "orderby" : str You can skip this field, there will be another query for this depending on the view you selected above, this is for ordering the results based on the stats you selected
    '''

    player: int # id of the player
    type: Optional[str] = "allround" # batting for batting stats, bowling for bowling stats, allround for allround stats, fielding for fielding stats
    class_: Optional[int] = 11  # 1 for test, 2 for odi, 3 for t20, 11 for all
    opposition: Optional[list[int]] = None  # list of opposition countries
    home_or_away: Optional[list[int]] = None  # 0, 1, 2 for home, away, neutral
    host: Optional[list[int]] = None  # list of host countries
    continent: Optional[list[int]] = None  # list of continents
    ground: Optional[list[int]] = None  # list of grounds, need to main cache
    span: Optional[list[str]] = None  # from and to date
    season: Optional[list[str]] = None  # list of seasons, need to main cache
    series: Optional[list[int]] = None  # list of series, need to main cache
    trophy: Optional[list[int]] = None  # list of trophies, need to main cache
    tournament_type: Optional[list[int]] = None  # list of tournament types, 0 for 2 team, 1 for 3-4 team, 2 for 5+ teams
    final_type: Optional[list[int]] = None  # list of final types {"all types":"","tournament finals":"1","tournament semi-finals":"3","tournament quarter-finals":"4","preliminary quarter-finals":"5","preliminary matches":"0"}
    floodlit: Optional[int] = None  # {"day match":1,"day/night match":2,"night match":3}
    result: Optional[list[int]] = None  # {"won match":1,"lost match":2,"tied match":3,"drawn match":4,"no result":5}
    toss: Optional[int] = None  # toss results, 0 for win, 1 for loss
    batting_fielding_first: Optional[int] = None  # batting or fielding first, 0 for batting, 1 for fielding
    captain: Optional[int] = None  # 1 for captain, 0 for not captain
    keeper: Optional[int] = None  # 1 for keeper, 0 for not keeper
    debut_or_last: Optional[list[int]] = None  # 0 career debut  1 last career match  2 team debut  3 last match for team
    player_age: Optional[list[int]] = None  # from and to age, [from, to], if only from then [from, -1], if only to then [-1, to]
    innings_number: Optional[list[int]] = None  # list of innings numbers {"1st innings":1,"2nd innings":2,"3rd innings":3,"4th innings":4}
    player_involve: Optional[list[int]] = None  # list of players that are involved in the match
    captain_involve: Optional[list[int]] = None  # list of captains that are involved in the match
    runs_scored: Optional[list[int]] = None  # Runs scored in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    batting_position: Optional[list[int]] = None  # from and to batting position [from, to] if only from then [from, -1], if only to then [-1, to]
    dismissal: Optional[list[int]] = None  # list of dismissals, need to main cache
    outs: Optional[int] = None  # {"out":1,"not out/absent/dnb":0}
    balls_bowled: Optional[list[int]] = None  # Balls bowled in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    runs_conceded: Optional[list[int]] = None  # Runs conceded in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    wickets_taken: Optional[list[int]] = None  # Wickets taken in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    bowling_position: Optional[list[int]] = None  # from and to bowling position [from, to] if only from then [from, -1], if only to then [-1, to]
    catches_taken: Optional[list[int]] = None  # Catches taken in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    stumpings_made: Optional[list[int]] = None  # Stumpings made in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    view: Optional[str] = None  # How to show the stats {"Overall figures":"","Innings by innings list":"innings","Match totals":"match","Match results":"results","Match and series awards":"awards","Series averages":"series","Ground averages":"ground","By host country":"host","By opposition team":"opposition","By year of match start":"year","By season":"season"}
    orderby: Optional[str] = None  # Order the results by {"matches":"matches played","innings":"innings batted","notouts":"not outs","outs":"batting dismissals","runs":"runs scored","minutes":"minutes batted","batting_average":"batting average","balls_faced":"balls faced","batting_strike_rate":"batting strike rate","hundreds":"hundreds scored","fifty_plus":"scores of fifty or more","ducks":"ducks scored","fours":"boundary fours","sixes":"boundary sixes","innings_bowled":"innings bowled in","balls":"balls bowled","maidens":"maidens earned","conceded":"runs conceded","wickets":"wickets taken","bowling_average":"bowling average","economy_rate":"economy rate","bowling_strike_rate":"bowling strike rate","four_plus_wickets":"four wickets in an inns","five_wickets":"five wickets in an inns","ten_wickets":"ten wickets in a match","matches_keeper":"matches as a keeper","matches_fielder":"matches as a fielder","innings_fielded":"innings fielded","dismissals":"fielding dismissals made","caught":"catches taken","stumped":"stumpings made","caught_keeper":"catches as a keeper","caught_fielder":"catches as a fielder","dismissals_per_inns":"dismissals per innings","allround_average":"batting - bowling average"}
    orderbyad: Optional[str] = None # reverse if we need to reverse the order of the orderby field

    def get_query_url(self):

        url = f"https://stats.espncricinfo.com/ci/engine/player/{self.player}.html?template=results"

        url += build_url(self.__dict__)

        return url
    
    def get_data(self):
        pass



@staticmethod
def build_url(value_dict: dict) -> str:
    query_url = ""

    for key, value in value_dict.items():
        if value is None:
            continue

        if key == "class_":
            key = "class"
        elif key  == "player_age":
            query_url += get_from_to_query(value, "age")
            continue
        elif key == "runs_scored":
            query_url += get_from_to_query(value, "runs")
            continue
        elif key == "batting_position":
            query_url += get_from_to_query(value, "batting_position")
            continue
        elif key == "balls_bowled":
            query_url += get_from_to_query(value, "balls")
            continue
        elif key == "runs_conceded":
            query_url += get_from_to_query(value, "conceded")
            continue
        elif key == "wickets_taken":
            query_url += get_from_to_query(value, "wickets")
            continue
        elif key == "bowling_position":
            query_url += get_from_to_query(value, "bowling_position")
            continue
        elif key == "catches_taken":
            query_url += get_from_to_query(value, "catches")
            continue
        elif key == "stumpings_made":
            query_url += get_from_to_query(value, "stumped")
            continue
        elif key == "result_qualifications":
            query_url += "&qualval1=" + str(value).lower()
            continue
        elif key == "qual_value":
            query_url += get_from_to_query(value, "qual")
            continue
        elif key == "span":
            query_url += get_from_to_query(value, "span")
            continue
        
    
        if value is not None:
            if isinstance(value, list):
                for v in value:
                    query_url += "&" + str(key) + "=" + str(v).lower()
            else:
                query_url += "&" + str(key) + "=" + str(value).lower()
    
    return query_url
        

    
@staticmethod 
async def populate_ids(json: dict, id_mapper: IdMapper) -> dict:
    for key, value in json.items():
        if key in ["team", "opposition", "host"]:
            new_val = await populate_values(value, lambda val: id_mapper.get_id("country", val))
            json[key] = new_val
        elif key in ["continents"]:
            new_val = await populate_values(value, lambda val: id_mapper.get_id("continent", val))
            json[key] = new_val
        elif key in ["ground"]:
            new_val = await populate_values(value, lambda val: id_mapper.get_id("ground", val))
            json[key] = new_val
        elif key in ["season"]:
            new_val = await populate_values(value, lambda val: id_mapper.get_id("season", val))
            json[key] = new_val
        elif key in ["series"]:
            new_val = await populate_values(value, lambda val: id_mapper.get_id("series", val))
            json[key] = new_val
        elif key in ["trophy"]:
            new_val = await populate_values(value, lambda val: id_mapper.get_id("trophy", val))
            json[key] = new_val
        elif key in ["player_involve", "captain_involve"]:
            new_val = await populate_values(value, lambda val: id_mapper.get_id("player", val))
            json[key] = new_val

    return json
            
@staticmethod
def get_class_description(cls):
    # Get the docstring of the class
    docstring = cls.__doc__
    if not docstring:
        return "No description available."

    # Process the docstring to create a readable description
    lines = docstring.strip().split('\n')
    description = f"Class '{cls.__name__}' attributes:\n"
    for line in lines:
        description += f"{line.strip()}\n"
    
    return description


@staticmethod
async def populate_values(value, func):
    if isinstance(value, list):
        tasks = [asyncio.create_task(func(val)) for val in value]
        new_val = await asyncio.gather(*tasks)
    else:
        new_val = await func(value)

    return new_val

@staticmethod
def get_from_to_query(value: list, key, suffix= 1):
    fro  = value[0]
    to = value[1]

    if key == "span":
        # we need to convert the date to dd+mm+yyyy format
        fro = convert_date(fro)
        to = convert_date(to)
  
    query_url = ""

    if fro != '-1' and fro != -1:
        query_url += "&" + key + "min" + str(suffix) + "="+str(fro).lower()
    if to != '-1' and to != -1:
        query_url += "&" + key + "max"+ str(suffix) + "="+str(to).lower()
    
    if (key != "qual"):
        query_url+= "&" + key + "val" + str(suffix) + "=" + str(key).lower()
    
    return query_url


@staticmethod
def convert_date(date: str) -> str:
    # it is of format dd+mm+yyyy
    if date == '-1' or date == -1:
        return date

    date = date.split("-")

    #mm should be of Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec
    date[1] = months[int(date[1]) - 1]

    date = f"{date[0]}+{date[1]}+{date[2]}"
    return date