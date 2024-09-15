from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_community.utils.openai_functions import convert_pydantic_to_openai_function
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import Union 

from app.models.audio_bot.invoice_prompt import system_message
from app.models.audio_bot.invoice_schema import InvoiceJson

load_dotenv() # take environment variables from .env


model = ChatOpenAI(model='gpt-4o-mini', temperature=0.1)

parser = JsonOutputFunctionsParser()
openai_functions = [convert_pydantic_to_openai_function(InvoiceJson)]


def summarize(document_id, context: str) -> dict:
    prompt = ChatPromptTemplate.from_messages(
        [("system", system_message), ("user", "{input}")]
    )
    chain = prompt | model.bind(functions=openai_functions) | parser
    response = chain.invoke({"input": context})
    
    return {'document_id': document_id, 'response': response} 