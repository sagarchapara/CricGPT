from api_clients.cricinfo_client import CricInfoClient
from api_clients.llm import OpenAIClient
from data_models.cricinfo import CricInfoAllRound, get_class_description, populate_ids
from id_mapper import IdMapper
from utils.utils import load_json, filter_results
from utils.prompts import get_summary_promt
import json

class AllRound:
    def __init__(self, openai_client: OpenAIClient, cricinfo_client: CricInfoClient, id_mapper: IdMapper):
        self.openai_client = openai_client
        self.cricinfo_client = cricinfo_client
        self.id_mapper = id_mapper

    async def get_summary(self, query, result: list) -> str:
        system_prompt = get_summary_promt()

        user_query = f"User query: {query}\n"

        user_query += "\n".join([f"Result: {res}" for res in result])

        summary = await self.openai_client.get_response(system_prompt=system_prompt, query=user_query)

        return summary

    async def execute(self, input_data: dict):
        system_prompt = get_stats_prompt()

        query = input_data["query"]

        response = await self.openai_client.get_response(system_prompt=system_prompt, query=query)

        #load the response to json
        response = load_json(response)

        print(response)

        #now go through any string fields and convert them to id's
        if response is None or response == "":
            return {
                "result": "No response from the model",
                "query": query,
                "url": None
            }

        #now get the order by, groupby and result qualification fields
        type = response.get("type", "allround")
        view = response.get("view", "default")

        view_prompt = get_view_fields_prompt(type, view)

        view_results = await self.openai_client.get_response(system_prompt=view_prompt, query=query)

        view = load_json(view_results)

        #now override the view field
        for key, value in view.items():
            response[key] = value

        response = await populate_ids(response, self.id_mapper)

        if response.get("view") == "default":
            response["view"] = None # set it to None
        
        if response.get("groupby") == "default":
            response["groupby"] = None

        #load the cricinfo batting
        batting = CricInfoAllRound.model_validate(response)

        #now get the url
        query_url = batting.get_query_url()

        print(query_url)

        #query the cricinfo site

        result = await self.cricinfo_client.get_search_data(query_url)

        result = filter_results(result)

        summary = await self.get_summary(query, result)

        return {
            "result": summary,
            "query": query,
            "url": query_url
        }

@staticmethod
def get_view_fields_prompt(type: str, view: str) -> str:

    if view is None or view == "":
        view = "default"

    #depending on the type and view, provide the prompt
    type_view = f"orderbyselect_{type}_{view}"

    having_select = f"havingselect_{type}_{view}"

    groupby_fields_select = f"groupby_{type}"

    groupby_fields = {}

    if view == "default":
        # then we need to provide groupby fields
        if type != "aggregate":
            try:
                with open(f"static/mappings/{groupby_fields_select}.json", "r") as f:
                    groupby_fields = json.load(f)
            except FileNotFoundError:
                print(f"File not found for {groupby_fields_select}")
            
            

    with open(f"static/mappings/{having_select}.json", "r") as f:
        having_select = json.load(f)

    with open(f"static/mappings/{type_view}.json", "r") as f:
        orderby_fields = json.load(f)

    return f'''

    You are an intelligent AI agent, whose reponsibilty is to provide a json structure that can be used to query the cricinfo website for player stats.
    Specially you are responsible for the view orderby fields which are high importance for the query and earth can be in danger if you don't provide them correctly.

    You have selected the type as {type} and view as {view}.

    If the view is default, then you need to provide the groupby fields for the query, if the view is not default, you should not pick the groupby fields and return None for the groupby fields.

    Group by fields:

    Field: groupby: str

    These are the possible options that you can choose from:
        {groupby_fields}
    
    You need to provide the field that you want to group the results on, Carefully choose the field that you want to group the results based on the query given. Think through the query and provide the correct field.

    If it is by players you need to output "players", if it is by team you need to output "team" and so on.

    {{
        "groupby": "<groupby>" # only provide the values given in the fields list if view is default
    }}
    
    Now, you need to specify result qualifications field on which you want to base your query. 
    
    This field will be used to filter the results according to the minimum and maximum values you define

    These are the possible options that you can choose from:

    Field : Result Qualification

    {having_select}

    You need to provide the field that you want to filter the results on.

    and you need to give min and max values for the field in [from, to] format, if you only have one value, only from or only to, then provide the -1 for the other value

    {{
        "result_qualifications": "<result_qualification>" # only provide the values given in the fields list,
        "qual_value": [from, to]
    }}

    Next, you need to provide the orderby fields for the query.


    Order by fields:

    {orderby_fields}

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

    Finally combine the result qualifications and orderby fields in the json structure.

    {{
        "groupby": "<groupby>", # only provide the values given in the fields list if view is default
        "result_qualifications": "<result_qualification>", # only provide the values given in the fields list, empty if not required
        "qual_value": [from, to] of the result_qualification field, empty if not required
        "orderby": "<order by>",
        "orderbyad": <orderbyad> # optional field if you want to reverse the order
    }}

    Please provide the json structure in the above format, with the correct values for the type, view and orderby fields.
    Don't add any comments in the json format, make sure it is a valid json format and all the fields are in the correct format.

    Reason and breakdown your thought process before providing the json format, Only provide the final json structure with the correct values.

    Do good and save the earth from the danger.
    '''

@staticmethod
def get_stats_prompt():
    return f'''
    You are an intelligent AI agent, whose reponsibilty is to provide a json structure that can be used to query the cricinfo website for batting stats.
    These are the follwing fields that you need to provide depending on the query:

    {get_class_description(CricInfoAllRound)}

    All the fields are optional unless explicity mentioned it's not, so only fill the fields that are required from the query. Only fill, if the it is absolutely necessary.

    Field output type is also mentioned, so if multiple values are asked then you need to provide a list of values.

    If attribute type is list always provide the values in list format, even if it is a single value.

    If attribute type is [from, to], but you only have one value, only from or only to, then provide the -1 for the other value, '-1' if it's a string and -1 if it's a number.

    Fields like countries, players, captains etc are in Integer format, which you don't have the id's for, so you need to provide the names of the countries, players, captains... I will convert them to id's before querying the cricinfo website.

    You need to provide output in json format.

    ```json
    {{
        "type": "team",
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
        type = batting,
        class_ = 2,
        orderby=high_score
    }}

    Reasoning: We need to find the highest individual score in ODIs, so we need to provide the class as 2 as it is ODIs and orderby as high_score as it is per inning high score stats and type as batting as we are looking for batting stats

    2. Most Runs in a Calendar Year
    {{
        'type': batting,
        'view': year,
        'orderby': runs
    }}

    Reasoning: We need to find the most runs in a calendar year, so we need to provide the view as year and orderby as runs and type as batting as we are looking for batting stats

    3. India stats in 2021
    {{
        'type': 'team',
        'team': ['India'], 
        'span': ['01-01-2021', '31-12-2021']
    }}

    Reasoning: We need to find the stats of India in 2021, so we need to provide the team as India and span as the year 2021 and type as team as we are looking for team stats

    4. Sachin stats when he scored 100s
    {{
        'type': 'batting',
        'player': ['Sachin Tendulkar'],
        'runs_scored': [100, -1]
    }}

    Reasoning: We need to find the stats of Sachin when he scored 100s, so we need to provide the player as Sachin Tendulkar and runs_scored as 100 and -1 as we are looking for the stats when he scored 100s per innings and type as batting as we are looking for batting stats

    5. Indian players in 2021 with min 1000 runs
    {{
        'type': 'batting',
        'team': ['India'],
        'span': ['01-01-2021', '31-12-2021'],
    }}

    Reasoning: We need to find the Indian players in 2021 with min 1000 runs, so we need to provide the team as India and span as the year 2021 and type as batting as we are looking for batting stats, here we are not providing the runs_scored as it is inninig wise stats not the overall stats.

    6. India stats in MCG
    {{
        'type': 'team',
        'team': ['India'],
        'ground': ["AUS: Melbourne Cricket Ground, Melbourne"]
    }}

    Reasoning: We need to find the India stats in MCG, so we need to provide the team as India and ground as MCG, Format for grounds is "Country: Ground, City"

    7. India stats in ODI World Cup
    {{
        'type': 'team',
        'team': ['India'],
        'trophy': ['World Cup']
    }}

    Reasoning: We need to find the India stats in ODI World Cup, so we need to provide the team as India and trophy as World Cup, as World Cup is a trophy.

    Don't fill per inning stats in the overall stats, these will be taken care in another query.

    Carefully read the query and provide the required fields in the json format. If you do the query correctly, you will be rewarded with 100$ in your account. So make sure you do it correctly.

    Reason and breakdown your thought process before providing the json format.

    Return a valid json format, don't add comments in the json format, make sure it is a valid json format and all the fields are in the correct format.

    '''
