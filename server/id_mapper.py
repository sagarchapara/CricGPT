import json
from api_clients.cricinfo_client import CricInfoClient
from cache import PersistentCache

class IdMapper:
    def __init__(self, cricInfoClient: CricInfoClient, cache:PersistentCache):
        self.cricInfoClient = cricInfoClient
        self.cache = cache

        #TODO: use elasticsearch to store the data
        with open('static/teams.json') as f:
            self.teams = json.load(f)

        with open('static/stadiums.json') as f:
            self.countries = json.load(f)

    async def get_id(self, field: str, value: str):
        if field == 'country':
            return self.get_team_id(value)
        elif field == 'player':
            return await self.get_player_id(value)
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