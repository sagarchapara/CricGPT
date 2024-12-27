import tweepy
import time
from cricapi import CricApiResponse, CricApi
import logging
import os
from dotenv import load_dotenv
import uuid

logger = logging.getLogger()

class TwitterBot:
    def __init__(self):
        self.api : tweepy.API = None
        self.cricapi: CricApi = CricApi()
        self.last_seen_id_file: str = "last_seen_id.txt"
        self.init_env()
        self.authenticate()

    def init_env(self):
        load_dotenv()
        self.api_key: str = os.getenv("API_KEY")
        self.api_key_secret: str = os.getenv("API_KEY_SECRET")
        self.access_token: str = os.getenv("ACCESS_TOKEN")
        self.access_token_secret: str = os.getenv("ACCESS_TOKEN_SECRET")

    def authenticate(self):
        auth = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)

    def get_last_seen_id(self):
        try:
            with open(self.last_seen_id_file, "r") as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return None

    def save_last_seen_id(self, last_seen_id):
        with open(self.last_seen_id_file, "w") as file:
            file.write(str(last_seen_id))

    async def process_mentions(self):
        last_seen_id = self.get_last_seen_id()
        mentions = self.api.mentions_timeline(since_id=last_seen_id, tweet_mode='extended')
        for mention in reversed(mentions):  # Process oldest to newest
            last_seen_id = mention.id
            correlation_id = str(uuid.uuid4())

            try:
                logger.info(f"Processing mention from @{mention.user.screen_name}: {mention.full_text}, correlationId: {correlation_id}")
                
                # Get the response from the CricApi
                reply = await self.get_tweet_response(mention.full_text, correlation_id)

                try:
                    # Reply to the mention
                    self.api.update_status(status=reply, in_reply_to_status_id=mention.id)
                    logger.info(f"Replied to @{mention.user.screen_name}, correlationId: {correlation_id}")
                except Exception as e:
                    logger.error(f"Error replying to @{mention.user.screen_name}: {e}, correlationId: {correlation_id}")
            except Exception as e:
                logger.error(f"Error processing mention from @{mention.user.screen_name}: {e}, correlationId: {correlation_id}")

            finally:
                self.save_last_seen_id(last_seen_id)

    async def get_tweet_response(self, tweet: str, correlationId: str) -> str:
        try:
            response = await self.cricapi.response(tweet, correlationId)

            return response.summary
        
        except Exception as e:
            return f"Error: {e}"

    async def run(self):
        while True:
            try:
                await self.process_mentions()
                time.sleep(30)  # Wait 30 seconds before checking again
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(30)