from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from routes.endpoint import router


load_dotenv(".env")


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])
app.include_router(router)


@app.get("/")
async def test():
    return {"messge": "hello world"}
