from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
# from langchain.schema import AIMessage

from dotenv import load_dotenv
from typing import Union

from app.models.chat_bot.invoice_prompt import system_message, system_context_message
from app.database import search_by_similar
from app.utils import bcolors

load_dotenv() # take environment variables from .env


# embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")    
model = ChatOpenAI(model='gpt-4o', temperature=0.1, streaming=True)

prompt_template = PromptTemplate(
    input_variables=['context', 'question'],
    template=system_message
)

def chat_bot(question: str, document_id: str, user_id: Union[int, str] = 0):
    similar_chunks = search_by_similar(question, document_id, user_id)
    similar_text = '\n'.join([chunk['$vectorize'] for chunk in similar_chunks])
    
    prompt = prompt_template.format(context=similar_text, question=question)
    
    print(f'{bcolors.OKBLUE}Chat -> Genereting chat response{bcolors.ENDC}')
    response = model.invoke(prompt)
    print(f'{bcolors.OKBLUE}\nChat -> Chat response generated{bcolors.ENDC}')
    
    return dict(response)
    

def chat_bot_stream(question: str, document_id: str, user_id: Union[int, str] = 0):
    similar_chunks = search_by_similar(question, document_id, user_id)
    similar_text = '\n'.join([chunk['$vectorize'] for chunk in similar_chunks])
    
    prompt = prompt_template.format(context=similar_text, question=question)
    
    print(f'{bcolors.OKBLUE}Chat -> Genereting chat response{bcolors.ENDC}')
    
    # Generate the response stream
    for chunk in model.stream(prompt):  # Process each streamed chunk
        print(f'{bcolors.OKGREEN}{chunk.content}{bcolors.ENDC}', end='', flush=True)
        yield chunk.content
        
    print(f'{bcolors.OKBLUE}\nChat -> Chat response generated{bcolors.ENDC}')