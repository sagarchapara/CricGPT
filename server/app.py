from typing import Optional
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
import logging
from cache import PersistentCache
from store import LocalSessionStore, SessionStore, Session, SessionCronJob
from datetime import datetime, timedelta, timezone
from utils.utils import datetime_to_epoch

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

cache = PersistentCache()
cricinfo_client = CricInfoClient(cache=cache)
id_mapper = IdMapper(cricinfo_client, cache=cache)
openai_client = OpenAIClient(model="gpt4o")
localstore = LocalSessionStore()
# sessionstore = SessionStore()
# sessioncronjob = SessionCronJob(localstore, sessionstore)

class Message(BaseModel):
    role: str
    content: str
    timestamp: int
    isliked: Optional[bool] = None
    isdisliked: Optional[bool] = None


class Query(BaseModel):
    query: str
    history: list[dict]

class Response(BaseModel):
    response: str
    urls: list[str]
    queries: list[str]

class ShareLinkParams(BaseModel):
    sessionId: str
    messages: list[Message]

class ShareLinkResponse(BaseModel):
    sharedLink: str

class LikeUnlikeParams(BaseModel):
    sessionId: str
    messages: list[Message]    

@app.post("/stats")
async def process_data(data: Query):
    cricgpt = CricGPT(openai_client=openai_client, cricinfo_client=cricinfo_client, id_mapper=id_mapper)
    response = await cricgpt.execute(data.query, data.history)
    return response

@app.post("/sharelink")
async def share_link(data: ShareLinkParams):    
    share_link = "https://cricstatsai.com/id/" + data.sessionId

    #calculate the number of messages, likes and dislikes
    num_messages = 0
    num_likes = 0
    num_dislikes = 0

    for message in data.messages:
        if message.role == "assistant":
            num_messages += 1
        if message.isliked:
            num_likes += 1
        if message.isdisliked:
            num_dislikes += 1
    
    session = Session(
        id=data.sessionId,
        messages=[message.model_dump() for message in data.messages],
        sharedLink=share_link,
        lastUpdated=datetime_to_epoch(datetime.now(timezone.utc)),
        numMessages=num_messages,
        numLikes=num_likes,
        numDislikes=num_dislikes
    )

    localstore.upsert(session)

    return ShareLinkResponse(sharedLink=share_link)

@app.post("/like")
async def like_message(data: LikeUnlikeParams):
    session = localstore.get(data.sessionId)

    if session is None:
        session = Session(
            id=data.sessionId,
            messages=[message.model_dump() for message in data.messages],
            sharedLink=""
        )

    likes = 0
    dislikes = 0
    num_messages = 0

    for message in data.messages:
        if message.isliked:
            likes += 1
        if message.isdisliked:
            dislikes += 1
        if message.role == "assistant":
            num_messages += 1
    
    session.numLikes = likes
    session.numDislikes = dislikes
    session.numMessages = num_messages
    session.lastUpdated = datetime_to_epoch(datetime.now(timezone.utc))


    localstore.upsert(session)

    return

@app.get("/session/{session_id}")
async def get_session(session_id: str):
    session = localstore.get(session_id)

    if session is None:
        return {"error": "Session not found"}, 404
        

    return {
        "sessionId": session.id,
        "messages": session.messages,
        "sharedLink": session.sharedLink,
        "lastUpdated": session.lastUpdated,
        "numMessages": session.numMessages,
        "numLikes": session.numLikes,
        "numDislikes": session.numDislikes
    }
    
    

# Run the FastAPI server
if __name__ == "__main__":

    #add file logger
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler('fastapi.log')
    logger.addHandler(file_handler)

    #get the port from args
    parser = argparse.ArgumentParser(description="Run the FastAPI server.")
    parser.add_argument("--port", type=int, default=5000, help="Port to run the server on")
    args = parser.parse_args()

    uvicorn.run("app:app", host="0.0.0.0", port=args.port)