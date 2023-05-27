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
    collection.create_index([('user_id', pymongo.HASHED)])
    return collection


def create_collections(database: Database):
    collection_names = set(database.list_collection_names())
    mapping = {
        'message': create_message_collection
    }
    for name, fn in mapping.items():
        if name not in collection_names:
            print(f'creating {name} collection')
            fn(database=default_database, name=name)


if __name__ == '__main__':
    create_collections(database=default_database)
