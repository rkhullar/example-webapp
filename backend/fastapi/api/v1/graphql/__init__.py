from strawberry import Schema

from .example import Query

schema = Schema(query=Query)
