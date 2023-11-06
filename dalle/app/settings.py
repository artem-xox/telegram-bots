import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv(), override=True)

OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
BOT_API_KEY=os.getenv('BOT_API_KEY')
WHITELIST=os.getenv('WHITELIST').split(',')

DALLE_2_MODEL="dall-e-2"
DALLE_3_MODEL="dall-e-3"

RESOLUTION_HIGH = "1792x1024"
RESOLUTION_MEDIUM = "1024x1792"
RESOLUTION_LOW = "1024x1024"
