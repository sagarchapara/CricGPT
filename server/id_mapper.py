import json
from api_clients.cricinfo_client import CricInfoClient

class IdMapper:
    def __init__(self, cricInfoClient: CricInfoClient):
        self.cricInfoClient = cricInfoClient

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
        player_id = await self.cricInfoClient.get_statsguru_player_id(player)

        return player_id
