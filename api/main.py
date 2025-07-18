from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate


class OpenAIHandler:
    def __init__(self):
        self.llm = OpenAI()
        self.prompt = PromptTemplate.from_template("Como decir {input} en {output_language}:\n")
        self.prompt_complete = PromptTemplate.from_template("Completa la siguiente frase {input} como si fueras {rol}:\n")
        self.chain = self.prompt | self.llm
        self.chain = self.prompt_complete | self.llm

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
    
    def complete_text(self, input_text: str, rol: str) -> str:
        """
        Traducción del texto a otro idioma
        """
        result = self.chain.invoke({
            "rol": rol,
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
    return {"response": answer, "version": "0.0.3"}


class UserComplete(BaseModel):
    user_message: str
    rol: str

@app.post("/complete_text/")
def complete_text(message: UserComplete):
    handler = OpenAIHandler()
    answer = handler.complete_text(message.user_message,  message.rol )
    return {"response": answer, "version": "0.0.3"}