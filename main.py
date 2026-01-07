import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import strawberry
from sqlalchemy.sql import text

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

    apps.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
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

    @apps.get("/health")
    async def health_check():
        try:
            async with db as session:
                await session.execute(text("SELECT 1"))
            return {"status": "healthy", "database": "online"}
        except Exception as e:
            return JSONResponse(
                status_code=503,
                content={"status": "unhealthy", "database": "offline", "error": str(e)}
            )
    
    schema = strawberry.Schema(query=Query, mutation=Mutation)
    graphql_app = GraphQLRouter(schema)
    
    apps.include_router(graphql_app, prefix="/graphql")

    return apps

app = init_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
