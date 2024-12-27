import logging
import asyncio
from bot import TwitterBot

logger = logging.getLogger()


    
def init_logging():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('twitter-bot.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def main():
    twitter_bot = TwitterBot()
    asyncio.run(twitter_bot.run())
        
if __name__ == "__main__":
    init_logging()
    main()