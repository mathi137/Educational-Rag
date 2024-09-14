from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import Union 

# from app.models.chat_bot.invoice_prompt import system_message
# from app.database import search_by_similar

load_dotenv() # take environment variables from .env


# embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
model = ChatOpenAI(model='gpt-4o-mini', temperature=0.1)

prompt_template = PromptTemplate(
    input_variables=['context'],
    template="""
Com base no contexto a seguir: 
{context}

Faça um resumo
"""
)

def summarize(document_id, context) -> dict:
    prompt = prompt_template.format(context=context)
    response = model.invoke(prompt)
    
    return {'document_id': document_id, 'response': dict(response)['content']} 