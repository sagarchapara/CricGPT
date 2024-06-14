import json

class IdMapper:
    def __init__(self):
        #TODO: use elasticsearch to store the data
        with open('static/teams.json') as f:
            self.teams = json.load(f)

        with open('static/players.json') as f:
            self.players = json.load(f)

        with open('static/stadiums.json') as f:
            self.countries = json.load(f)

    def get_id(self, field: str, value: str):
        if field == 'country':
            return self.get_team_id(value)
        elif field == 'player':
            return self.get_player_id(value)
        else:
            raise ValueError(f"Field {field} not found")
    
    def get_team_id(self, team: str):
        return self.teams.get(team)
    
    def get_player_id(self, player: str):
        return self.players.get(player, 1)