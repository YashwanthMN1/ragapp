from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
from app.router import router

load_dotenv()

app = FastAPI()

app.include_router(router)


if __name__ =="__main__":
    uvicorn.run(app=app,host="127.0.0.1",port=8000)
