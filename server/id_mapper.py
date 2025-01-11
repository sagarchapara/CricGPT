import json
from api_clients.cricinfo_client import CricInfoClient
from cache import PersistentCache
from Levenshtein import distance
import time

class IdMapper:
    trophy_dist_threshold = 10
    series_dist_threshold = 15
    stadium_dist_threshold = 15

    def __init__(self, cricInfoClient: CricInfoClient, cache:PersistentCache):
        self.cricInfoClient = cricInfoClient
        self.cache = cache

        #TODO: use elasticsearch to store the data
        with open('static/teams.json') as f:
            self.teams = json.load(f)
        
        self.stadiums = {
            "last_updated": 0, #unix timestamp
            "data": {}
        }

        self.trophies = {
            "last_updated": 0, #unix timestamp
            "data": {}
        }

        self.series = {
            "last_updated": 0, #unix timestamp
            "data": {}
        }

        self.season = {
            "last_updated": 0, #unix timestamp
            "data": {}
        }

    async def get_id(self, field: str, value: str):
        if field == 'country':
            return self.get_team_id(value)
        elif field == 'player':
            return await self.get_player_id(value)
        elif field == 'stadium':
            return await self.get_stadium_id(value)
        elif field == 'trophy':
            return await self.get_trophy_id(value)
        elif field == 'series':
            return await self.get_series_id(value)
        elif field == 'season':
            return await self.get_season_id(value)
        else:
            raise ValueError(f"Field {field} not found")
    
    def get_team_id(self, team: str):
        return self.teams.get(team)
    
    async def get_player_id(self, player: str):
        player_cache_id = f"statsguru_player_{player}"

        player_cache_str = await self.cache.get(player_cache_id)

        if player_cache_str is not None:
            player_cache = json.loads(player_cache_str)
            return player_cache["player_id"]

        player_id = await self.cricInfoClient.get_statsguru_player_id(player)

        player_cache_str = json.dumps({
            "player_id": player_id
        })

        await self.cache.set(player_cache_id, player_cache_str)

        return player_id
    
    async def get_stadium_id(self, stadium: str):
        print("last updated", self.stadiums["last_updated"])

        #check if the data is updated
        if time.time() - self.stadiums["last_updated"] > 3600:
            #fetch the data
            self.stadiums["data"] = await self.cricInfoClient.get_dropdown_options("ground")
            self.stadiums["last_updated"] = time.time()

        return self.get_closest_match(stadium, self.stadiums["data"], 15)
    
    async def get_trophy_id(self, query: str) -> int:
        print("last updated", self.trophies["last_updated"])

        #check if the data is updated
        if time.time() - self.trophies["last_updated"] > 3600:
            #fetch the data
            self.trophies["data"] = await self.cricInfoClient.get_dropdown_options("trophy")
            self.trophies["last_updated"] = time.time()

        return self.get_closest_match(query, self.trophies["data"], self.trophy_dist_threshold)
    
    async def get_series_id(self, query: str) -> int:
        print("last updated", self.series["last_updated"])

        #check if the data is updated
        if time.time() - self.series["last_updated"] > 3600:
            #fetch the data
            self.series["data"] = await self.cricInfoClient.get_dropdown_options("series")
            self.series["last_updated"] = time.time()

        return self.get_closest_match(query, self.series["data"], 15)
    
    async def get_season_id(self, season: str):
        print("last updated", self.season["last_updated"])

        if time.time() - self.season["last_updated"] > 3600:
            #fetch the data
            self.season["data"] = await self.cricInfoClient.get_dropdown_options("season")
            self.season["last_updated"] = time.time()

        if season in self.season["data"]:
            return self.season["data"][season]
        else:
            return None
        
    
    def get_closest_match(self, query: str, data: dict, threshold: int) -> int:
        filtered_matches = [
            (k, distance(k.lower(), query.lower()))
            for k in data.keys()
            if distance(k.lower(), query.lower()) <= threshold
        ]

        if filtered_matches:
            closest_match, distance_value = min(filtered_matches, key=lambda x: x[1])
            print(f"Closest match: {closest_match} (Distance: {distance_value}), ID: {data[closest_match]}")

            return data[closest_match]
        else:
            print("No close matches found within the threshold.")
            return None

        