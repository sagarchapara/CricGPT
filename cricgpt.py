import re
import json
from api_clients.llm import OpenAIClient
from api_clients.cricinfo_client import CricInfoClient
from data_models.cricinfo import CricInfoAllRound, get_class_description
from id_mapper import IdMapper




class CricGPT:
    def __init__(self, model: str):
        self.openai_client = OpenAIClient(model=model)
        self.cricinfo_client = CricInfoClient()
        self.id_mapper = IdMapper()

    async def get_result(self,  query: str):

        system_prompt = get_batting_stats_prompt()

        response = await self.openai_client.get_response(system_prompt=system_prompt, query=query)

        #load the response to json
        response = load_json(response)

        print(response)

        #now go through any string fields and convert them to id's
        if response:
            response = CricInfoAllRound.populate_ids(response, self.id_mapper)

        print(response)

        #load the cricinfo batting
        batting = CricInfoAllRound.model_validate(response)

        #now get the url
        query_url = batting.get_query_url()

        print(query_url)

        #query the cricinfo site

        result = await self.cricinfo_client.get_data(query_url)

        return result



@staticmethod
def get_batting_stats_prompt():
    return f'''
    You are an intelligent AI agent, whose reponsibilty is to provide a json structure that can be used to query the cricinfo website for batting stats.
    These are the follwing fields that you need to provide depending on the query:

    {get_class_description(CricInfoAllRound)}

    All fields are optional, so you need to only fill the required fields from the query. Only fill, if the it is absolutely necessary.

    Field output type is also mentioned, so if multiple values are asked then you need to provide a list of values.

    Fields like countries, players, captains etc are in Integer format, which you don't have the id's for, so you need to provide the names of the countries, players, captains... I will convert them to id's before querying the cricinfo website.

    You need to provide output in json format.

    ```json
    {{
        "captain_involve": ["MS Dhoni", "Virat Kohli"],
        "runs_scored": [100, 200],
        "batting_position": [1, 2],
        "dismissal": [1, 2, 3],
        "dismissed": 1,
        "host": ["India"],
        ...
    }}
    ```
    Few examples of the queries are:

    1. Highest Individual Score in ODIs 
    {{
        class_ = 2,
        orderby=high_score
    }}

    Reasoning: We need to find the highest individual score in ODIs, so we need to provide the class as 2 as it is ODIs and orderby as high_score as it is per inning high score stats

    2. Most Runs in a Calendar Year
    {{
        view=year,
        orderby=runs
    }}

    Reasoning: We need to find the most runs in a calendar year, so we need to provide the view as year and orderby as runs

    Carefully read the query and provide the required fields in the json format. If you do the query correctly, you will be rewarded with 100$ in your account. So make sure you do it correctly.

    Reason and breakdown your thought process before providing the json format.

    Return a valid json format, don't add comments in the json format, make sure it is a valid json format and all the fields are in the correct format.

    '''

@staticmethod
def load_json(response: str):
    #find the json markdown in reponse
    json_str = re.search(r'```json(.*?)```', response, re.DOTALL)
    if json_str:
        json_str = json_str.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            print("Error in decoding the json")
            return None
