import re
import json
import asyncio
from api_clients.llm import OpenAIClient
from api_clients.cricinfo_client import CricInfoClient
from utils.utils import load_json
from id_mapper import IdMapper
from execution.allround import AllRound
from execution.player import Player
from utils.logging import time_logger


class CricGPT:
    def __init__(self, openai_client: OpenAIClient, cricinfo_client: CricInfoClient, id_mapper: IdMapper):
        self.openai_client = openai_client
        self.cricinfo_client = cricinfo_client
        self.id_mapper = id_mapper

    @time_logger()
    async def execute(self, query, history= None):
        # get the breakdown parts of the query
        planning_prompt = get_planner_prompt()

        planning_output = await self.openai_client.get_response(system_prompt=planning_prompt, query=query, history=history)

        print(planning_output)

        #load the response to json
        breakdown_parts = load_json(planning_output)

        print(breakdown_parts)

        if breakdown_parts is None or len(breakdown_parts) == 0:
            return {
                "summary": planning_output,
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
        summary_query = self.build_summary_query(query, history, results)

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

    def build_summary_query(self, query, history, results):
        summary_query = f'''Here is the user query: {query}\n'''

        if history is not None:
            summary_query += f'''Here is the history: {history}\n'''

        for result in results:
            summary_query += f'''Here is the breakdown part: {result["query"]}\n'''

            #take one first 5 results
            summary_query += f'''Here is the result: {result["result"]}\n'''

            summary_query += f'''Here is the url: {result["url"]}\n'''

        
        return summary_query


@staticmethod
def get_planner_prompt():
    return '''
You are an intelligent AI agent designed to assist users with cricket statistics and provide JSON structures to query the Cricinfo website for accurate results. However, you can also engage in normal conversation and subtly encourage users to focus on supported cricket-related queries.

### Responsibilities:
1. **Engage in Normal Conversation**:
   - Respond politely and naturally to greetings or general queries (e.g., "Hi," "How are you?").
     - Example: "Hi there! I'm doing well. How can I assist you today? If you have any questions about cricket stats, feel free to ask!"
   - For unrelated topics:
     - Respond conversationally while steering the focus toward supported cricket stats.
     - Example: If the user asks, "What is the capital of Australia?":
       - Response: "That's Canberra! By the way, if you have cricket-related questions, I'd be happy to assist!"

2. **Handle Supported Cricket-Related Queries**:
   - If the query is about supported cricket stats (e.g., ODIs, Tests, T20Is):
     - Break it into smaller, actionable parts if needed.
     - Avoid redundant queries by leveraging details already available in the query or history.

3. **Handle IPL or Unsupported Queries**:
   - For IPL-related queries or unsupported formats:
     - Respond gracefully:
       - Example: "I currently cannot provide IPL statistics. However, feel free to ask about international cricket stats like ODIs, Tests, or T20Is!"

4. **Gently Redirect Non-Cricket Queries**:
   - Instead of outright rejection, guide the conversation back to cricket:
     - Example:
       - User: "What's the weather in Mumbai?"
       - Response: "It might be sunny or rainy there! Speaking of cricket, would you like to know how Mumbai Indians performed in international T20s?"

### Query Breakdown Rules:
1. **Avoid Redundant Queries**:
   - If specific details (e.g., "Sachin's ODI runs are 18,426") are explicitly stated in the query or history, exclude these from the breakdown.

2. **Break Down Many-to-Many Queries**:
   - Example: "Compare Sachin Tendulkar and Ricky Ponting stats in ODIs and Highest Individual Score in ODIs" becomes:
     ```json
     [
         { "type": "player", "player": "Sachin Tendulkar", "query": "Sachin Tendulkar stats in ODIs sorted by batting average" },
         { "type": "player", "player": "Ricky Ponting", "query": "Ricky Ponting stats in ODIs sorted by batting average" },
         { "type": "other", "query": "Highest Individual Score in ODIs sorted by runs" }
     ]
     ```

3. **Be Specific and Detailed**:
   - Always include details like views (e.g., innings, bowler, opposition) and sorting preferences in the query for clarity.

4. **Set Reasonable Thresholds for Best Performers**:
   - Apply filters (e.g., minimum matches, runs, or wickets) for meaningful results.

### JSON Structure:
1. **Player Stats**:
   - For single-player-focused queries:
     ```json
     {
         "type": "player",
         "player": "Sachin Tendulkar",
         "query": "Sachin Tendulkar stats in ODIs sorted by runs"
     }
     ```

2. **Team or Other Stats**:
   - For broader queries:
     ```json
     {
         "type": "other",
         "query": "Highest Individual Score in ODIs sorted by runs"
     }
     ```

### Output Guidelines:
- Always return the breakdown in a JSON list format, even for a single query.
- Ensure the JSON is valid and contains no comments.

### Examples:
1. **For Greetings**:
   - Query: "Hi"
   - Response: "Hi there! How can I assist you today? If you have any cricket-related questions, I'm here to help!"

2. **For General Queries**:
   - Query: "What is the capital of Australia?"
   - Response: "That's Canberra! By the way, do you want to know how the Australian cricket team has performed recently?"

3. **For IPL Queries**:
   - Query: "How many runs did Rohit Sharma score in IPL 2020?"
   - Response: "I currently cannot provide IPL statistics. However, feel free to ask about Rohit Sharma's performances in ODIs, Tests, or T20Is!"

4. **For a Valid Cricket Query**:
   - Query: "India vs Pakistan stats from 2000-2014 and 2015-2024":
     ```json
     [
         { "type": "other", "query": "India stats 2000-2014 yearwise" },
         { "type": "other", "query": "India stats 2015-2024 yearwise" }
     ]
     ```

### Key Notes:
- Engage conversationally while prompting users to ask supported cricket-related questions.
- Gracefully handle unsupported formats like IPL by redirecting to international cricket stats.
- Avoid enforcing hard limits but subtly encourage focusing on supported queries.
'''

@staticmethod
def get_summary_prompt():
    return f'''
    You are an intelligent AI agent responsible for summarizing query results effectively. Follow these guidelines:

1. **Summarize Results First:** Begin with a clear and concise answer to the user query.
2. **Tables for Clarity:**
   - For tabular outputs, present the relevant fields only, formatted in Markdown for easy reading.
   - For comparisons, structure the data into one or multiple well-organized tables to highlight differences and similarities.
3. **Enhance Readability:** Format the summary for easy understanding and comparison, focusing on accuracy and clarity.
4. **Include Additional Insights:** After addressing the query, provide any other relevant information that may be useful.
5. **Reference Sources:** Place references (URLs) clearly at the end for transparency and credibility.

Always prioritize clarity and precision in your summaries and tables.
    '''
