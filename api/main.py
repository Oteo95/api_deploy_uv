from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate


class OpenAIHandler:
    def __init__(self):
        self.llm = OpenAI()
        self.prompt = PromptTemplate.from_template("Como decir {input} en {output_language}:\n")
        self.chain = self.prompt | self.llm

    def translate(self, input_text: str, output_language: str) -> str:
        """
        Traducción del texto a otro idioma
        """
        result = self.chain.invoke({
            "output_language": output_language,
            "input": input_text,
        })
        # result may be a string or a dict depending on the LLM's output
        return str(result)


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
    return {"response": answer, "version": "0.0.2"}