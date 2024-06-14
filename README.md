# CricGPT
Advanced Cricket Stats Through Natural Language Queries

## Setup

1. **Install Required Packages:**
   ```sh
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables:**
   - Create a `.env` file based on the provided `.env_sample`.
   - Update the `.env` file with your OpenAI key and endpoints.

## Functionality

CricGPT facilitates advanced cricket statistical analysis using natural language queries, akin to [Statsguru](https://stats.espncricinfo.com/ci/engine/stats/index.html).

### Example Natural Language Queries

1. **Indian Player Stats Against SENA Teams in SENA Countries (2011-2014, Test Matches, Sorted by Batting Average with Minimum 1000 Runs):**
   ```
   Show stats for Indian players against SENA teams in SENA countries from 2011 to 2014 in Test matches, sorted by batting average with at least 1000 runs.
   ```

2. **Left-Handed Batsmen Stats in T20Is Batting in the Lower Order (Minimum 500 Runs, Sorted by Strike Rate):**
   ```
   Provide stats for left-handed batsmen in T20Is batting in the lower order with a minimum of 500 runs, sorted by strike rate.
   ```

3. **Most Runs in a Calendar Year in ODI Cricket (2010-2020):**
   ```
   Show the players with the most runs in ODI cricket for each calendar year from 2010 to 2020.
   ```

4. **Most Runs in Away Test Matches for India (2014-2024, Ordered by Average with Minimum 500 Runs):**
   ```
   Show the players with the most runs in away Test matches for India from 2014 to 2024, ordered by batting average with at least 500 runs.
   ```

5. **Most Man of the Match (MOM) Awards in Away T20I Matches for India (2014-2024):**
   ```
   Show the players with the most Man of the Match awards in away T20I matches for India from 2014 to 2024.
   ```