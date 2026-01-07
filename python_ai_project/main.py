from fastapi import Body, Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud import add_request_data, get_user_request
from database.db import get_async_session
from gemini_client import get_answer_from_gemini
from database.init_db import init

app = FastAPI()

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


@app.on_event("startup")
async def on_startup():
    await init()

@app.get("/request")
async def get_my_request(
    request: Request, session: AsyncSession = Depends(get_async_session)
):
    user_ip = request.client.host
    print(f"User IP: {user_ip}")

    user_request = await get_user_request(ip_address=user_ip, session=session)
    return {"user_request": user_request}


@app.post("/request")
async def send_prompt(
    request: Request,
    prompt: str = Body(embed=True),
    session: AsyncSession = Depends(get_async_session),
):
    user_ip = request.client.host
    answer = get_answer_from_gemini(prompt)
    await add_request_data(
        ip_address=user_ip, prompt=prompt, response=answer, session=session
    )
    return {"answer": answer}