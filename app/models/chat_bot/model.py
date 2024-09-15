from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv
from typing import Union 

from app.models.chat_bot.invoice_prompt import system_message, system_context_message
from app.database import search_by_similar

load_dotenv() # take environment variables from .env


# embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
model = ChatOpenAI(model='gpt-4o-mini', temperature=0.1)

prompt_template = PromptTemplate(
    input_variables=['context', 'question'],
    template=system_message
)

context_prompt_template = PromptTemplate(
    input_variables=['history', 'context', 'question'],
    template=system_context_message
)

def chat_bot(question: str, document_id: str, user_id: Union[int, str] = 0, chat_history: dict = None) -> dict:
    similar_chunks = search_by_similar(question, document_id, user_id)
    similar_text = '\n'.join([chunk['$vectorize'] for chunk in similar_chunks])
    
    if chat_history:
        prompt = context_prompt_template.format(history=str(chat_history), context=similar_text, question=question)
    else:
        prompt = prompt_template.format(context=similar_text, question=question)
    
    # generate response
    response = model.invoke(prompt)
    
    return dict(response)