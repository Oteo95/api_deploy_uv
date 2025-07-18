import os
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
