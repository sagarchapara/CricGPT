from api_clients.cricinfo_client import CricInfoClient
from api_clients.llm import OpenAIClient
from data_models.cricinfo import CricInfoPlayer, get_class_description, populate_ids
from id_mapper import IdMapper
from utils.utils import load_json
import asyncio
import json


class Player:
    def __init__(self, openai_client: OpenAIClient, cricinfo_client: CricInfoClient, id_mapper: IdMapper):
        self.openai_client = openai_client
        self.cricinfo_client = cricinfo_client
        self.id_mapper = id_mapper


    async def execute(self, input_data: dict):
        # extract the player name from the query
        player_name = input_data["player"]

        query = input_data["query"]

        # first fetch the player id
        player_name, player_id = await self.cricinfo_client.get_cricinfo_player(player_name)

        if player_id is None:
            return {
                "result": "No player found",
                "query": query,
                "url": None
            }
        
        # now query llm for the json format
        system_prompt = get_stats_prompt()

        results = await self.openai_client.get_response(system_prompt=system_prompt, query=query)

        response = load_json(results)

        #load the response to json
        if response is None or response == "":
            return {
                "result": "No response from the model",
                "query": query,
                "url": None
            }

        #now get the order by fields
        type = response.get("type", "allround")
        view = response.get("view", "default")

        view_prompt = get_view_fields_prompt(type, view)

        view_results = await self.openai_client.get_response(system_prompt=view_prompt, query=query)

        view = load_json(view_results)

        #now override the view field
        for key, value in view.items():
            response[key] = value

        response["player"] = player_id

        if response.get("view") == "default":
            response["view"] = None # set it to None

        #now go through any string fields and convert them to id's
        response = await populate_ids(response, self.id_mapper)

        #load the cricinfo batting
        player_stats = CricInfoPlayer.model_validate(response)

        #now get the url
        query_url = player_stats.get_query_url()

        print(query_url)

        #query the cricinfo site
        result = await self.cricinfo_client.get_search_data(query_url)

        return {
            "result": result,
            "query": query,
            "url": query_url    
        }

@staticmethod
def get_view_fields_prompt(type: str, view: str) -> str:

    if view is None or view == "":
        view = "default"

    #depending on the type and view, provide the prompt
    type_view = f"orderbyselect_{type}_{view}"

    with open(f"static\\mappings\\{type_view}.json", "r") as f:
        orderby_fields = json.load(f)

        if "player_name" in orderby_fields:
            orderby_fields.remove("player_name") # as we have only one player

    return f'''

    You are an intelligent AI agent, whose reponsibilty is to provide a json structure that can be used to query the cricinfo website for player stats.
    Specially you are responsible for the view orderby fields which are high importance for the query and earth can be in danger if you don't provide them correctly.

    You have selected the type as {type} and view as {view}, so you need to provide the orderby fields for the query.

    These are the following fields that you need to provide:

    Order by fields:

    {orderby_fields}

    Also you need to provide this optional field:

    If you want to reverse the order, you can provide the orderbyad field with the value as reverse.

    All the fields are sorted by highest to lowest, so if you want to reverse the order, you can provide the orderbyad field with the value as reverse.
    
    orderbyad=reverse

    Given these fields, you need to provide the json structure that can be used to query the cricinfo website for the required stats.
    {{
        "orderby": "<order by>", # only provide the values given in the fields list
        "orderbyad": <orderbyad> # optional field if you want to reverse the order
    }}

    Make sure you provide the correct values for the orderby field, if you provide any other value, the earth will be in danger.
    Don't provide any list of values, only provide the single value for the orderby field.
    Optionally provide the orderbyad field with value as reverse if you want to reverse the order.

    Please provide the json structure in the above format, with the correct values for the type, view and orderby fields.
    Don't add any comments in the json format, make sure it is a valid json format and all the fields are in the correct format.

    Reason and breakdown your thought process before providing the json format.

    Do good and save the earth from the danger.
    '''


@staticmethod
def get_stats_prompt():
    return f'''
    You are an intelligent AI agent, whose reponsibilty is to provide a json structure that can be used to query the cricinfo website for player stats.
    These are the follwing fields that you need to provide depending on the query:

    {get_class_description(CricInfoPlayer)}

    For all the [from, to] fields if only from then [from, -1], if only to then [-1, to]

    All the fields are optional unless explicity mentioned it's not, so only fill the fields that are required from the query. Only fill, if the it is absolutely necessary.

    When ever json is mentioned in list of fields possible, always output the values of json, never output the keys of the json

    Field output type is also mentioned, so if multiple values are asked then you need to provide a list of values.

    Fields like countries, players, captains etc are in Integer format, which you don't have the id's for, so you need to provide the names of the countries, players, captains... I will convert them to id's before querying the cricinfo website.
    
    You need to provide output in json format.

    ```json
    {{
        "class_": 11,
        "type": "batting",
        "player": ["Sachin Tendulkar"],
        "captain_involve": ["MS Dhoni", "Virat Kohli"],
        "runs_scored": [100, 200],
        "batting_position": [1, 2],
        "dismissal": [1, 2, 3],
        "dismissed": 1,
        "host": ["India"],
    }}
    ```
    
    Carefully read the query and provide the required fields in the json format. If you do the query correctly, you will be rewarded with 100$ in your account. So make sure you do it correctly.

    Reason and breakdown your thought process before providing the json format.

    Return a valid json format, don't add comments in the json format, make sure it is a valid json format and all the fields are in the correct format.

    '''