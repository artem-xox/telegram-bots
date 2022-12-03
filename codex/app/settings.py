import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
BOT_API_KEY=os.getenv('BOT_API_KEY')