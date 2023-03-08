import os

from pymongo import MongoClient


def build_atlas_client(atlas_host: str, local_mode: bool = False) -> MongoClient:
    # https://www.mongodb.com/docs/atlas/manage-connections-aws-lambda/
    # https://www.mongodb.com/docs/manual/reference/connection-string/#mongodb-atlas-cluster
    mongo_client_url = f'mongodb+srv://{atlas_host}/?authSource=%24external&authMechanism=MONGODB-AWS&retryWrites=true&w=majority'
    if local_mode:
        assert 'AWS_PROFILE' in os.environ
    return MongoClient(mongo_client_url, connect=True)
