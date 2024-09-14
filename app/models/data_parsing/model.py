from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_community.utils.openai_functions import convert_pydantic_to_openai_function
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
# from langchain_core.utils.function_calling import convert_to_openai_function

from typing import Union

from app.models.data_parsing.invoice_prompt import system_message
from app.models.data_parsing.invoice_schema import InvoiceJson, JsonFixOutputFunctionsParser
from app.database import search_by_similar, search_by_index


model = ChatOpenAI(model='gpt-4o', temperature=0.1)

parser = JsonOutputFunctionsParser()
openai_functions = [convert_pydantic_to_openai_function(InvoiceJson)]


def extract_data_from_documentID(document_id: str, user_id: Union[str, int] = 0) -> dict:
    chunk = search_by_index(index=0, document_id=document_id, user_id=user_id)
    context = chunk[0]['content']
    
    question = "Encontre o objeto do contrato."
    similar_chunks = search_by_similar(question, document_id, user_id, limit=2)
    context += '\n'.join([chunk['content'] for chunk in similar_chunks])
    
    question = "Encontre o valor do contrato."
    similar_chunks = search_by_similar(question, document_id, user_id, limit=1)
    context += '\n'.join([chunk['content'] for chunk in similar_chunks])
    
    question = "Encontre a vigência do contrato."
    similar_chunks = search_by_similar(question, document_id, user_id, limit=1)
    context += '\n'.join([chunk['content'] for chunk in similar_chunks])
    
    question = "Encontre a data do contrato."
    similar_chunks = search_by_similar(question, document_id, user_id, limit=1)
    context += '\n'.join([chunk['content'] for chunk in similar_chunks])
    
    extracted_data_json = call_json_output_parser(context)
    
    return {'document_id': document_id, 'data': extracted_data_json}


def call_json_output_parser(context: str) -> dict:
    prompt = ChatPromptTemplate.from_messages(
        [("system", system_message), ("user", "{input}")]
    )
    chain = prompt | model.bind(functions=openai_functions) | parser
    response = chain.invoke({"input": context})
    return response
        