import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.conf.config import config
from src.database.db import get_db
from src.routes import contacts, users

app = FastAPI()
origins = [
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Session(get_db())


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=config.REDIS_DOMAIN, port=config.REDIS_PORT, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
