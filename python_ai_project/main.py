from contextlib import asynccontextmanager

from fastapi import FastAPI, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware

from db import Base, engine, get_user_request, add_request_data
from gemini_client import  get_answer_from_gemini

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы")
    yield

app = FastAPI(lifespan=lifespan)

# Разрешить запросы с локального фронтенда (порт 5500)
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/request")
async def get_my_request(request: Request):
    user_ip = request.client.host
    print(f'{user_ip}')
    user_request = get_user_request(ip_address=user_ip)
    return {"user_request": user_request}

@app.post("/request")
def send_prompt(
        request: Request,
        prompt: str = Body(embed=True),
):
    user_ip = request.client.host
    answer = get_answer_from_gemini(prompt)
    add_request_data(
        ip_address=user_ip,
        prompt=prompt,
        response=answer,
    )
    return {"answer": answer}