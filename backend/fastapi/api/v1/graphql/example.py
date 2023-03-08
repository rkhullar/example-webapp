import strawberry


@strawberry.type
class Book:
    title: str
    author: str


@strawberry.type
class Query:

    @strawberry.field()
    def books(self) -> list[Book]:
        return [
            Book(title='The Great Gatsby', author='F. Scott Fitzgerald')
        ]
