from os import getenv
from dotenv import load_dotenv, find_dotenv

# these expect to find a .env file at the directory above the lesson.                                                                                                                     # the format for that file is (without the comment)                                                                                                                                       #API_KEYNAME=AStringThatIsTheLongAPIKeyFromSomeService
def _load_env():
    _ = load_dotenv(find_dotenv())

def get_backend_url():
    _load_env()
    backend_url = f"{getenv('BACKEND_SERVER')}:{getenv('BACKEND_PORT')}"
    return backend_url