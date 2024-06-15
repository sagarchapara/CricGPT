from logging import warn
import bs4
from bs4 import BeautifulSoup
import aiohttp
import re
import urllib

class CricInfoClient:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
    
    
    async def get_search_data(self, url):

        # Send a GET request to the URL
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                html = await response.text()

        # Parse the HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Find all tables with class 'engineTable'
        tables = soup.find_all('table', class_='engineTable')

        # Find the table that contains rows with class 'data1'
        table = None
        for t in tables:
            if t.find('tr', class_='data1') and t.find('tr', class_='headlinks'):
                table = t
                break

        headers = []
        header_row = table.find('tr', class_='headlinks')
        for th in header_row.find_all('th'):
            header_text = th.get_text(strip=True)
            if header_text:  # Skip empty headers
                headers.append(header_text)

        # Extract player data from the table rows
        results = []
        for row in table.find_all('tr', class_='data1'):
            columns = row.find_all('td')

            if len(columns) == 1 and not columns[0].get_text(strip=True):
                # Skip empty rows
                continue

            row = {headers[i]: columns[i].get_text(strip=True) for i in range(len(headers))}
            results.append(row)

        return results
    

    async def get_cricinfo_player(self, player: str):

        player = player.replace(' ', '+')

        query = f"{player}+cricinfo+stats"

        url = f"https://www.google.com/search?q={query}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                html = await response.text()
        
        soup = BeautifulSoup(html, 'html.parser')

        # Find the first search result with espncricinfo.com in the URL
        for a in soup.find_all('a', href=True):
            if 'espncricinfo.com/cricketers' in a['href']:
                url = a['href']
                break

        if url is None:
            print("No search results found")
            return None
        
        player_name , player_id = CricInfoClient.extract_player_info(url)
        
        return player_name, player_id
    
    async def get_statsguru_player_id(self, player: str):
        player_name, _ = await self.get_cricinfo_player(player)

        search_player_name = player_name.replace(' ', '+')

        #uisng this player name query the statsguru site to get the player id

        url = f"https://stats.espncricinfo.com/ci/engine/stats/index.html?class=11;filter=advanced;type=allround;search_player={search_player_name}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                html = await response.text()

        soup = BeautifulSoup(html, 'html.parser')

        # Find all input elements with name 'player_involve'
        inputs = soup.find_all('input', {'name': 'player_involve'})

        # Iterate through the inputs to find the one with the desired text
        for input_elem in inputs:
            # Check the parent element's text to find the right player
            parent_span = input_elem.find_parent('span')
            if parent_span and player_name in parent_span.get_text().lower():
                player_id = input_elem['value']
                print(player_id)  # Output: 95094
                break
            else:
                print("Span not found")
        
        return player_id


    @staticmethod
    def extract_player_info(url_string):
        """Extracts player name and ID from a URL string with encoded URL.

        Args:
            url_string: The string containing the URL, potentially with search parameters.

        Returns:
            A tuple containing player name and ID, or None if not found.
        """
        parsed_url = urllib.parse.urlparse(url_string)

        # Check if query string exists
        if parsed_url.query:
            # Extract query parameters
            query_params = urllib.parse.parse_qs(parsed_url.query)

            # Look for relevant parameter (e.g., "url")
            if "url" in query_params:
                encoded_url = query_params["url"][0]
            else:
                print("Couldn't find 'url' parameter in the query string")
                return None, None
            

            # Decode the URL
            actual_url = urllib.parse.unquote(encoded_url)

            print(actual_url)

            pattern = r"https://www\.espncricinfo\.com/cricketers/([a-zA-Z\-]+)-(\d+)"

            # Extract player name and ID from the URL
            match = re.match(pattern, actual_url)
            if match is None:
                print("Couldn't extract player name and ID from URL")
                return None, None
            
            player_name = match.group(1)
            player_id = match.group(2)

            # replace the - with a space
            player_name = player_name.replace('-', ' ')

            return player_name, player_id

        else:
            print("Couldn't find 'url' parameter in the query string")

        return None, None # If no information found