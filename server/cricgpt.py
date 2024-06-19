import re
import json
import asyncio
from api_clients.llm import OpenAIClient
from api_clients.cricinfo_client import CricInfoClient
from utils.utils import load_json
from id_mapper import IdMapper
from execution.allround import AllRound
from execution.player import Player


class CricGPT:
    def __init__(self, model: str, openai_client: OpenAIClient, cricinfo_client: CricInfoClient, id_mapper: IdMapper):
        self.openai_client = openai_client
        self.cricinfo_client = cricinfo_client
        self.id_mapper = id_mapper
        self.model = model

    async def execute(self, query, history= None):
        # get the breakdown parts of the query
        planning_prompt = get_planner_prompt()

        breakdown_parts = await self.openai_client.get_response(system_prompt=planning_prompt, query=query, history=history)

        print(breakdown_parts)

        #load the response to json
        breakdown_parts = load_json(breakdown_parts)

        print(breakdown_parts)

        if breakdown_parts is None or len(breakdown_parts) == 0:
            return {
                "summary": "I'm sorry, I can't help you with that query",
                "urls": [],
                "queries": [query]
            }

        # now go through each breakdown part and get the result
        results = []
        tasks = []
        for breakdown_part in breakdown_parts:
            tasks.append(self.process_breakdown_part(breakdown_part))

        results = await asyncio.gather(*tasks)

        #finally summarize the results
        summary_prompt = get_summary_prompt()
        summary_query = self.build_summary_query(query, results)

        summary = await self.openai_client.get_response(system_prompt=summary_prompt, query=summary_query)

        return {
            "summary": summary,
            "urls": [result["url"] for result in results],
            "queries": breakdown_parts
        }
    
    async def process_breakdown_part(self, breakdown_part):
        if breakdown_part["type"] == "player":
            player_stats = Player(self.openai_client, self.cricinfo_client, self.id_mapper)
            result = await player_stats.execute(breakdown_part)
        else:
            stats = AllRound(self.openai_client, self.cricinfo_client, self.id_mapper)
            result = await stats.execute(breakdown_part)
        return result

    def build_summary_query(self, query, results):
        summary_query = f'''Here is the user query: {query}\n'''

        for result in results:
            summary_query += f'''Here is the breakdown part: {result["query"]}\n'''

            #take one first 5 results
            summary_query += f'''Here is the result: {result["result"]}\n'''

            summary_query += f'''Here is the url: {result["url"]}\n'''

        
        return summary_query


@staticmethod
def get_planner_prompt():
    return f''' 
    You are an intelligent AI agent, whose responsibilty is to identify the user query from the conversation and break the given query into smaller parts and provide the json structure that can be used to query the cricinfo website for the required stats.

    You'll will be provided with the user query + user query history, you need to carefully, use the history to understand the context of the query.

    After understanding the query, if it's related to cricket stats, then you need to breakdown the query into smaller parts, so that we can query the cricinfo website for the required stats.

    If it's not related to cricket stats, Simply reply with "I'm sorry, I can't help you with that query" and return an empty list.

    If the query is related to cricket stats, then you need to breakdown the query into smaller parts, so that we can query the cricinfo website for the required stats.

    Currently we can handle one - many queries, so breakdown the many - many queries into multiple one - many queries.

    examples of many - many queries are:

    1. Compare Sachin Tendulkar and Ricky Ponting stats in ODIs and Highest Individual Score in ODIs
    2. India vs Australia vs England stats in ODIs
    3. Sachin Tendulkar vs Ricky Ponting vs Brian Lara stats in ODIs
    4. India vs Pakistan stats from 2000 - 2014 and 2015 - 2024


    But these type of queries need not to be broken down:

    1. Sachin stats in multiple formats
    2. Sachin vs multiple bowlers
    3. India vs multiple countries
    4. Sachin in multiple grounds ...

    Each breakdown part is either one of the following:

    1. If it's about a particular player we are interested in, then the breakdown part is about the player stats
    2. If it's about a particular team we are interested in, then the breakdown part is about the team stats
    3. If it's about batting stats of multiple players in some countries, or opponents, or formats so on then the breakdown part is about the batting stats
    4. Similarly for bowling stats, allround stats, fielding stats


    1. Player Stats:
        If the query is related to player stats, then you need to provide the json structure that can be used to query the cricinfo website for player stats.
        These are the follwing fields that you need to provide depending on the query:
        ```json
        {{
            "type": "player"
            "player": "Sachin Tendulkar", # Always provide a single player name
            "query": "Sachin Tendulkar stats in ODIs sorted by runs"
        }}
        ```
    2. Batting/Bowling/AllRound/Team Stats:
        If the query is related to batting/bowling/allround/fielding for related stats, then you need to provide the json structure that can be used to query the cricinfo website for the required stats.
        These are the following fields that you need to provide depending on the query:
        ```json
        {{
            "type": "other",
            "query": "Highest Individual Score in ODIs sorted by runs",
        }}
        ```
    
    It's best to choose player stats, if we intrerested in a particular player and comparing him with other players, grounds, formats, countries, opponents, so on.
    
    Finally you output the breakdown parts json structure that can be used to query the cricinfo website for the required stats in a list
    
    For example:

    Here is the output for the query "Compare Sachin Tendulkar and Ricky Ponting stats in ODIs and Highest Individual Score in ODIs":
    
    ```json
    [
        {{ "type": "player", "player": "Sachin Tendulkar", "query": "Sachin Tendulkar stats in ODIs sorted by batting average" }},
        {{ "type": "player", "player": "Ricky Ponting", "query": "Sachin Tendulkar stats in ODIs sorted by batting average" }}
    ]

    Another Example:

    Here is the output for the query  "India vs Pakistan stats from 2000 - 2014 and 2015 - 2024"

    ```json
    [
        {{ "type": "other", "query": "India stats 2000 - 2014 yearwise" }},
        {{ "type": "other", "query": "India stats 2015 - 2024 yearwise" }},
    ]
    ```

    When you are forming the query, be as much specific as possible like in above examples, so that it's easy to understand and compare the results.
    
    When breaking down the queries, specify clearly in each of them what is the view (innings view or bowler view, or opposition view ...) you are excepting and how to sort the results, so that it's easy to understand and compare the results.

    Player should be a single player name, don't provide multiple players in one query.

    For most of them you don't need to breakdown the query.

    For example for the same above query "India stats from 1990 - 2024 vs pakistan year wise/decade wise", you don't need to breakdown the query as it is already continous time period and you can directly query the cricinfo website for the required stats.

    Other example is one batter/bowler vs multiple other batters/bowlers, you don't need to breakdown the query as we can already handle multiple opponents in the query.

    Same for other likes multiple countries, formats, hosts, we can handle these in one query directly, so no need to breakdown the query.

    So if you understand from above examples, we cannot handle many - many queries directly, but we can handle one - many queries, so breakdown many - many queries to multiple individual one - many queries.

    Please remeber we can one to many query directly, so no need to breakdown the query, it will just increase the complexity of the query.

    When queries are for best batsman/best bowler.., then have some min threshold for the players to qualify, like atleast x matches or y runs or z wickets, so on., don't keep it too high, keep it reasonable, to filter out the players who have high stats with less matches.

    Carefully read the query and provide the required fields in the json format. If you do the query correctly, you will be rewarded with 100$ in your account. So make sure you do it correctly.

    Reason and breakdown your thought process before providing the json format. Don't add any comments in the json format, make sure it is a valid json format and all the fields are in the correct format.

    Always return a list, even if it is a single breakdown part, return it as a list.
'''

@staticmethod
def get_summary_prompt():
    return f'''
    You are an intelligent AI agent, whose reponsibilty is to summarize the results of the queries that you have executed for the given user query
    You carefully read the results of the queries and provide a summary of the results.
    Suppose if the query is expecting a one liner answer then you need to provide a one liner answer, if the query is expecting a detailed answer then you need to provide a detailed answer.
    If the query ouput is table you return the table in the markdown format, but only with the relavent fields, not all fields
    If it's a comparision nicely format it into one table/multiple tables for clear understanding and comparison.
    Please nicely format it in table format for clear understanding and ensure you provide the correct references for the results using the urls given.
    Present the results in a clear and concise manner, so that it's easy to understand and compare the results.
    Make sure you first clearly answer the given query and then include any other relavent information that might be useful for the user, but always answer the query first.
    '''
