from fastapi import FastAPI
from openai_handler import OpenAIHandler
from pydantic import BaseModel


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hola mundo, api desplegada"}


class UserMessage(BaseModel):
    user_message: str
    language: str


@app.get("/health/")
def health():
    return {"message": "DONE"}


@app.post("/translation/")
def translation(message: UserMessage):
    handler = OpenAIHandler()
    answer = handler.translate(message.user_message,  message.language )
    return {"response": answer, "version": "0.0.3"}


class UserComplete(BaseModel):
    user_message: str
    rol: str

@app.post("/complete_text/")
def complete_text(message: UserComplete):
    handler = OpenAIHandler()
    answer = handler.complete_text(message.user_message,  message.rol )
    return {"response": answer, "version": "0.0.3"}