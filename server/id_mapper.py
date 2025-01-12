import json
from api_clients.cricinfo_client import CricInfoClient
from cache import PersistentCache
import time
from rapidfuzz import process

class IdMapper:
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

        self.seasons = {
            "last_updated": 0, #unix timestamp
            "data": {}
        }

    async def get_id(self, field: str, value: str):
        if field == 'country':
            return self.get_team_id(value)
        elif field == 'player':
            return await self.get_player_id(value)
        elif field == 'ground':
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
    
    async def get_stadium_id(self, stadium: str) -> int:
        return self.stadiums["data"].get(stadium)
    
    async def get_trophy_id(self, query: str) -> int:
       return self.trophies["data"].get(query)
    
    async def get_series_id(self, query: str) -> int:
        return self.series["data"].get(query)
    
    async def get_season_id(self, season: str):
        return self.seasons["data"].get(season)
            
    async def populate_options(self, entity: str):
        current_time = time.time()
        if entity == 'stadiums':
            if current_time - self.stadiums["last_updated"] > 86400:
                self.stadiums["data"] = await self.cricInfoClient.get_dropdown_options("ground")
                self.stadiums["last_updated"] = current_time
        elif entity == 'trophies':
            if current_time - self.trophies["last_updated"] > 86400:
                self.trophies["data"] = await self.cricInfoClient.get_dropdown_options("trophy")
                self.trophies["last_updated"] = current_time
        elif entity == 'series':
            if current_time - self.series["last_updated"] > 86400:
                self.series["data"] = await self.cricInfoClient.get_dropdown_options("series")
                self.series["last_updated"] = current_time
        elif entity == 'seasons':
            if current_time - self.seasons["last_updated"] > 86400:
                self.seasons["data"] = await self.cricInfoClient.get_dropdown_options("season")
                self.seasons["last_updated"] = current_time
        else:
            raise ValueError(f"Entity {entity} not found")
        
    async def get_probable_matches(self, entity, query: list[str]) -> list[str]:
        #populate cache if not already populated
        await self.populate_options(entity)

        data = getattr(self, entity)["data"]

        matches = set()

        for q in query:
            probable_mactes =  process.extract(q, data.keys(), limit=5)

            for match in probable_mactes:
                if match[1] > 80:
                    matches.add(match[0])

        return list(matches)
        