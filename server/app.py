import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from cricgpt import CricGPT
from api_clients.cricinfo_client import CricInfoClient
from api_clients.llm import OpenAIClient
from id_mapper import IdMapper
import sys
import argparse

# Fast api code
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


cricinfo_client = CricInfoClient()
id_mapper = IdMapper(cricinfo_client)
openai_client = OpenAIClient(model="gpt4o")

class Query(BaseModel):
    query: str
    history: list[dict]

class Response(BaseModel):
    response: str
    urls: list[str]
    queries: list[str]
    

@app.post("/stats")
async def process_data(data: Query):
    cricgpt = CricGPT(model="gpt4o", openai_client=openai_client, cricinfo_client=cricinfo_client, id_mapper=id_mapper)
    response = await cricgpt.execute(data.query)
    return response
    

# Run the FastAPI server
if __name__ == "__main__":

    #get the port from args
    parser = argparse.ArgumentParser(description="Run the FastAPI server.")
    parser.add_argument("--port", type=int, default=5000, help="Port to run the server on")
    args = parser.parse_args()

    uvicorn.run("app:app", host="0.0.0.0", port=args.port)