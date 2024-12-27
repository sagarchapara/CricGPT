import aiohttp

class CricApiResponse:
    summary: str
    urls: list[str]
    queries: list[str]

class CricApi:

    def __init__(self):
        self.url = "https://api.cricstatsai.com/stats"

    async def response(self, query: str, correlationId: str) -> CricApiResponse:
        body = {
            "query": query
        }

        headers = {
            "X-Correlation-ID": str(correlationId),
            "Content-Type": "application/json",
            "X-Client-Id": "twitter-bot"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=headers, json=body) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch data: {response.status}")
                data = await response.json()
                return CricApiResponse(
                    summary=data.get("summary"),
                    urls=data.get("urls", []),
                    queries=data.get("queries", [])
                )