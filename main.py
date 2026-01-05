import uvicorn
from fastapi import FastAPI
import strawberry

from config import db

from Graphql.query import Query
from Graphql.mutation import Mutation

from strawberry.fastapi import GraphQLRouter

def init_app():
    apps = FastAPI(
        title="API",
        description="API description",
        version="0.0.1",
    )

    @apps.on_event("startup")
    async def startup():
        await db.create_all()

    @apps.on_event("shutdown")
    async def shutdown():
        await db.close()

    @apps.get("/")
    def root():
        return {"message": "Hello World"}
    
    schema = strawberry.Schema(query=Query, mutation=Mutation)
    graphql_app = GraphQLRouter(schema)
    
    apps.include_router(graphql_app, prefix="/graphql")

    return apps

app = init_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
