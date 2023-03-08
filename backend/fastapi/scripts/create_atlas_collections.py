import os

import pymongo
from core.util import build_atlas_client
from pymongo.database import Collection, Database

atlas_host = os.getenv('ATLAS_HOST')  # NOTE: shouldn't include '-pe-'
mongo_client = build_atlas_client(atlas_host=atlas_host, local_mode=True)

default_database = mongo_client.get_database('default')


def create_message_collection(database: Database, name: str) -> Collection:
    collection = database.create_collection(name)
    collection.create_index([('created', pymongo.DESCENDING)])
    collection.create_index([('okta_id', pymongo.HASHED)])
    return collection


create_message_collection(database=default_database, name='message')
