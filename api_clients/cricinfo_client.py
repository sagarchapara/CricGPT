import bs4
from bs4 import BeautifulSoup
import aiohttp

class CricInfoClient:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
    
    
    async def get_data(self, url):

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
            if t.find('tr', class_='data1'):
                table = t
                break

        headers = []
        header_row = table.find('tr', class_='headlinks')
        for th in header_row.find_all('th'):
            header_text = th.get_text(strip=True)
            if header_text:  # Skip empty headers
                headers.append(header_text)

        # Extract player data from the table rows
        players = []
        for row in table.find_all('tr', class_='data1'):
            columns = row.find_all('td')
            player_data = {headers[i]: columns[i].get_text(strip=True) for i in range(len(headers))}
            players.append(player_data)

        return players
    