from typing import Optional, Type
from enum import Enum
from pydantic import BaseModel
from id_mapper import IdMapper


class CricInfoAllRound(BaseModel):
    '''
    class_: Optional[int] = None  # 1 for test, 2 for odi, 3 for t20, 11 for all
    team: Optional[list[int]] = None  # list of countries 
    opposition: Optional[list[int]] = None  # list of opposition countries
    home_or_away: Optional[list[int]] = None  # 1, 2, 3 for home, away, neutral
    host: Optional[list[int]] = None  # list of host countries
    continent: Optional[list[int]] = None  # list of continents {"all continents": 0, "Africa": 1, "Americas": 2, "Asia": 3, "Europe": 4, "Oceania": 5}
    ground: Optional[list[int]] = None  # list of grounds
    starting_date: Optional[list[int]] = None  # from and to date
    season: Optional[list[str]] = None  # list of seasons
    series: Optional[list[int]] = None  # list of series
    trophy: Optional[list[int]] = None  # list of trophies
    tournament_type: Optional[list[int]] = None  # list of tournament types 2 for 2 team, 3 for 3-4 team, 5 for 5+ teams
    match_type: Optional[list[int]] = None  # list of match types {"tournament finals":1,"tournament cons. finals":2,"tournament semi-finals":3,"tournament quarter-finals":4,"preliminary quarter-finals":5,"qualifying final":7,"preliminary matches":0}
    floodlit: Optional[int] = None  # {"day match":1,"day/night match":2,"night match":3}
    result: Optional[int] = None  # {"won match":1,"lost match":2,"tied match":3,"drawn match":4,"no result":5}
    toss: Optional[int] = None  # toss results 1 for win, 2 for loss
    batting_fielding_first: Optional[int] = None  # batting or fielding first 1 for batting, 2 for fielding
    captain: Optional[int] = None  # 1 for captain, 0 for not captain
    keeper: Optional[int] = None  # 1 for keeper, 0 for not keeper
    debut_or_last: Optional[list[int]] = None  {"career debut":1,"last career match":2,"team debut":3,"last match for team":4}
    batting_hand: Optional[list[int]] = None  # 1 for right, 2 for left
    bowling_hand: Optional[int] = None  # 1 for right hand, 2 for left hand
    bowling_pacespin: Optional[int] = None  # 1 for pace, 2 for spin, 3 for mixed
    player_age: Optional[list[int]] = None  # from and to age, [from, to], if only from then [from, -1], if only to then [-1, to]
    innings_number: Optional[list[int]] = None  # list of innings numbers {"1st innings":1,"2nd innings":2,"3rd innings":3,"4th innings":4}
    player_involve: Optional[list[int]] = None  # list of players that are involved in the match
    player_not_involve: Optional[list[int]] = None  # list of players that are not involved in the match
    captain_involve: Optional[list[int]] = None  # list of captains that are involved in the match
    captain_not_involve: Optional[list[int]] = None  # list of captains that are not involved in the match
    runs_scored: Optional[list[int]] = None  # from and to runs scored
    batting_position: Optional[list[int]] = None  # from and to batting position
    dismissal: Optional[list[int]] = None  # list of dismissals {"0":"all types","1":"caught","2":"bowled","3":"leg before wicket","4":"run out","5":"stumped","6":"hit wicket","7":"handled the ball","8":"obstructing the field","9":"retired out","10":"not out","11":"retired not out (hurt)"}
    outs: Optional[int] = None  # {"out":1,"not out/absent/dnb":0}
    balls_bowled: Optional[list[int]] = None  # Balls bowled in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    runs_conceded: Optional[list[int]] = None  # Runs conceded in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    wickets_taken: Optional[list[int]] = None  # Wickets taken in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    bowling_position: Optional[list[int]] = None  # from and to bowling position [from, to] if only from then [from, -1], if only to then [-1, to]
    catches_taken: Optional[list[int]] = None  # Catches taken in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    stumpings_made: Optional[list[int]] = None  # Stumpings made in innings [from, to] if only from then [from, -1], if only to then [-1, to]
    group_by: Optional[int] = None  # Group the stats by for individual players, we need not to use this, {"individual players":"","each team innings":"innings","each match":"match","each series":"series","each tour":"tour","team":"team","opposition team":"opposition","each ground":"ground","host country":"host","host continent":"continent","year of match start":"year","season":"season","decade of match":"decade","overall aggregate":"overall"}
    
    We have this set of fields that we can use to order the results by or filter the results 

    options = {"matches played":"matches","innings batted":"innings","notouts":"notouts","batting dismissals":"outs","runs scored":"runs","minutes batted":"minutes","batting average":"batting_average","balls faced":"balls_faced","batting strike rate":"batting_strike_rate","hundreds scored":"hundreds","scores of fifty or more":"fifty_plus","ducks scored":"ducks","boundary fours":"fours","boundary sixes":"sixes","innings bowled in":"innings_bowled","balls bowled":"balls","maidens earned":"maidens","runs conceded":"conceded","wickets taken":"wickets","bowling average":"bowling_average","economy rate":"economy_rate","bowling strike rate":"bowling_strike_rate","four wickets in an inns":"four_plus_wickets","five wickets in an inns":"five_wickets","ten wickets in a match":"ten_wickets","matches as a keeper":"matches_keeper","matches as a fielder":"matches_fielder","innings fielded":"innings_fielded","fielding dismissals made":"dismissals","catches taken":"caught","stumpings made":"stumped","catches as a keeper":"caught_keeper","catches as a fielder":"caught_fielder","dismissals per innings":"dismissals_per_inns","batting - bowling average":"allround_average"}

    result_qualifications: Optional[str] = None  # We can set min/max values for the results to qualify, we can choose from the options, you should only choose the value like "macthes" or "runs" etc never choose the keys like "matches played" or "runs scored" ...
    qual_value: Optional[list[int]] = None  # The value for the result qualification, [from, to] if only from then [from, -1], if only to then [-1, to]

    orderby: Optional[str] = None  # Order the results by choosing from the above options you should only choose the value like "macthes" or "runs" etc never choose the keys like "matches played" or "runs scored" ...
    '''

    class_: Optional[int] = None  # 1 for test, 2 for odi, 3 for t20, 11 for all
    team: Optional[list[int]] = None  # list of countries
    opposition: Optional[list[int]] = None  # list of opposition countries
    home_or_away: Optional[list[int]] = None  # 0, 1, 2 for home, away, neutral
    host: Optional[list[int]] = None  # list of host countries
    continent: Optional[list[int]] = None  # list of continents
    ground: Optional[list[int]] = None  # list of grounds, need to main cache
    starting_date: Optional[list[int]] = None  # from and to date  #TODO: need to check the format
    season: Optional[list[str]] = None  # list of seasons, need to main cache
    series: Optional[list[int]] = None  # list of series, need to main cache
    trophy: Optional[list[int]] = None  # list of trophies, need to main cache
    tournament_type: Optional[list[int]] = None  # list of tournament types, 0 for 2 team, 1 for 3-4 team, 2 for 5+ teams
    match_type: Optional[list[int]] = None  # list of match types
    floodlit: Optional[int] = None  # {"day match":1,"day/night match":2,"night match":3}
    result: Optional[int] = None  # {"won match":1,"lost match":2,"tied match":3,"drawn match":4,"no result":5}
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
    group_by: Optional[int] = None  # Group the stats by for individual players, we need not to use this, {"individual players":"","each team innings":"innings","each match":"match","each series":"series","each tour":"tour","team":"team","opposition team":"opposition","each ground":"ground","host country":"host","host continent":"continent","year of match start":"year","season":"season","decade of match":"decade","overall aggregate":"overall"}
    result_qualifications: Optional[str] = None  # We can set min/max values for the results to qualify, possible options
    qual_value: Optional[list[int]] = None  # The value for the result qualification, [from, to] if only from then [from, -1], if only to then [-1, to]
    orderby: Optional[str] = None  # Order the results by {"matches":"matches played","innings":"innings batted","notouts":"not outs","outs":"batting dismissals","runs":"runs scored","minutes":"minutes batted","batting_average":"batting average","balls_faced":"balls faced","batting_strike_rate":"batting strike rate","hundreds":"hundreds scored","fifty_plus":"scores of fifty or more","ducks":"ducks scored","fours":"boundary fours","sixes":"boundary sixes","innings_bowled":"innings bowled in","balls":"balls bowled","maidens":"maidens earned","conceded":"runs conceded","wickets":"wickets taken","bowling_average":"bowling average","economy_rate":"economy rate","bowling_strike_rate":"bowling strike rate","four_plus_wickets":"four wickets in an inns","five_wickets":"five wickets in an inns","ten_wickets":"ten wickets in a match","matches_keeper":"matches as a keeper","matches_fielder":"matches as a fielder","innings_fielded":"innings fielded","dismissals":"fielding dismissals made","caught":"catches taken","stumped":"stumpings made","caught_keeper":"catches as a keeper","caught_fielder":"catches as a fielder","dismissals_per_inns":"dismissals per innings","allround_average":"batting - bowling average"}




    def get_query_url(self):
        query_url = "https://stats.espncricinfo.com/ci/engine/stats/index.html?template=results&type=allround"

        for key, value in self.__dict__.items():
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
            elif key == "group_by":
                query_url += "&groupby=" + str(value)
                continue
            elif key == "result_qualifications":
                query_url += "&qualval1=" + str(value)
                continue
            elif key == "qual_value":
                query_url += get_from_to_query(value, "qual", suffix=1)
                continue
            
        
            if value is not None:
                if isinstance(value, list):
                    for v in value:
                        query_url += "&" + str(key) + "=" + str(v)
                else:
                    query_url += "&" + str(key) + "=" + str(value)
        
        return query_url
    
    def populate_ids(json: dict, id_mapper: IdMapper):
        for key, value in json.items():
            if key in ["team", "opposition", "host"]:
                new_val = populate_values(value, lambda val: id_mapper.get_id("country", val))
                json[key] = new_val
            elif key in ["continents"]:
                new_val = populate_values(value, lambda val: id_mapper.get_id("continent", val))
                json[key] = new_val
            elif key in ["ground"]:
                new_val = populate_values(value, lambda val: id_mapper.get_id("ground", val))
                json[key] = new_val
            elif key in ["season"]:
                new_val = populate_values(value, lambda val: id_mapper.get_id("season", val))
                json[key] = new_val
            elif key in ["series"]:
                new_val = populate_values(value, lambda val: id_mapper.get_id("series", val))
                json[key] = new_val
            elif key in ["trophy"]:
                new_val = populate_values(value, lambda val: id_mapper.get_id("trophy", val))
                json[key] = new_val
            elif key in ["player_involve", "player_not_involve", "captain_involve", "captain_not_involve"]:
                new_val = populate_values(value, lambda val: id_mapper.get_id("player", val))
                json[key] = new_val

        return json
            







class ViewFormatResultQualifications(Enum):
    MATCHES_PLAYED = "matches played"
    INNINGS_BATTED = "innings batted"
    NOT_OUTS = "not outs"
    BATTING_DISMISSALS = "batting dismissals"
    RUNS_SCORED = "runs scored"
    MINUTES_BATTED = "minutes batted"
    BALLS_FACED = "balls faced"
    BATTING_AVERAGE = "batting average"
    BATTING_STRIKE_RATE = "batting strike rate"
    HUNDREDS_SCORED = "hundreds scored"
    SCORES_OF_FIFTY_OR_MORE = "scores of fifty or more"
    DUCKS_SCORED = "ducks scored"
    BOUNDARY_FOURS = "boundary fours"
    BOUNDARY_SIXES = "boundary sixes"


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
def populate_values(value, func):
    if isinstance(value, list):
        new_val = []
        for val in value:
            v = func(val)
            new_val.append(v)
    else:
        new_val = func(value)

    return new_val

@staticmethod
def get_from_to_query(value: list, key, suffix= 0):
    fro  = value[0]
    to = value[1]

    query_url = ""

    if fro != -1:
        query_url += "&" + key + "min" + str(suffix) + "="+str(fro)
    if to != -1:
        query_url += "&" + key + "max"+ str(suffix) + "="+str(to)
    return query_url


