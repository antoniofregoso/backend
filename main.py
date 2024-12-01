import strawberry
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from config import DatabaseSession

from Graphql.query import Query
from Graphql.mutation import Mutation

from strawberry.fastapi import GraphQLRouter


def init_app():
    db = DatabaseSession()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await db.create_all()
        yield 
        await db.close()
    
    apps = FastAPI(
        lifespan=lifespan,
        title="Lemon code 21",
        description="Fast API",
        version="1.0.0"
    )

    @apps.get('/')
    def home():
        return "welcome home!"

    # add graphql endpoint
    schema = strawberry.Schema(query=Query, mutation=Mutation)
    graphql_app = GraphQLRouter(schema)

    apps.include_router(graphql_app, prefix="/graphql")

    return apps


app = init_app()

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8888, reload=True)