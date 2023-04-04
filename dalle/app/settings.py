import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv(), override=True)

OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
BOT_API_KEY=os.getenv('BOT_API_KEY')


MEDIA_SIZE = 9

RESOLUTION_HIGH = "1024x1024"
RESOLUTION_MEDIUM = "512x512"
RESOLUTION_LOW = "256x256"
