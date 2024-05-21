# Add your utilities or helper functions to this file.

import os
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from urllib.parse import quote_plus
from pymongo.server_api import ServerApi

# these expect to find a .env file at the directory above the lesson.                                                                                                                     # the format for that file is (without the comment)                                                                                                                                       #API_KEYNAME=AStringThatIsTheLongAPIKeyFromSomeService
def load_env():
    _ = load_dotenv(find_dotenv())

def get_openai_api_key():
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key

def get_serper_api_key():
    load_env()
    openai_api_key = os.getenv("SERPER_API_KEY")
    return openai_api_key


# break line every 80 characters if line is longer than 80 characters
# don't break in the middle of a word
def pretty_print_result(result):
  parsed_result = []
  for line in result.split('\n'):
      if len(line) > 80:
          words = line.split(' ')
          new_line = ''
          for word in words:
              if len(new_line) + len(word) + 1 > 80:
                  parsed_result.append(new_line)
                  new_line = word
              else:
                  if new_line == '':
                      new_line = word
                  else:
                      new_line += ' ' + word
          parsed_result.append(new_line)
      else:
          parsed_result.append(line)
  return "\n".join(parsed_result)

def get_mongo_uri():
    load_env()
    username = quote_plus(os.getenv("MONGO_USER"))
    password = quote_plus(os.getenv("MONGO_PASSWORD"))
    host = os.getenv("MONGO_HOST")
    dbname = os.getenv("MONGO_DBNAME")
    return f"mongodb+srv://{username}:{password}@{host}/{dbname}" 

def get_mongo_client():
    uri = get_mongo_uri()
    return MongoClient(uri, server_api=ServerApi('1'))

def get_mongo_db():
    client = get_mongo_client()
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    return client[os.getenv("MONGO_DBNAME")]  # Nome do seu banco de dados
