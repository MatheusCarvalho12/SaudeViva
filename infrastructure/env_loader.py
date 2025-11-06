import os
from dotenv import load_dotenv


def load_environment():
    load_dotenv()


def get_openai_api_key() -> str:
    return os.getenv("OPENAI_API_KEY")

