from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader 
from langchain_core.documents import Document

from app.models.audio_bot.model import transcriber_model
    
from bson import ObjectId, Binary
import tempfile


def load_from_file(file_bytes: bytes, file_name: str) -> Document:
    file_data = Binary(file_bytes)
    file_extension = file_name.split('.')[-1]
    
    with tempfile.NamedTemporaryFile(suffix=f'.{file_extension}', delete=False) as temp_file:
        temp_path = temp_file.name
        temp_file.write(file_data)
    
    match file_extension:
        case 'pdf':
            loader_function = PyPDFLoader
        case 'docx' | 'doc':
            loader_function = Docx2txtLoader
        case 'txt':
            loader_function = TextLoader
        case _:
            raise Exception('File not supported.')
            
    document = loader_function(temp_path).load()
    return document


def load_from_audio(file_bytes: bytes, file_name: str):
    file_data = Binary(file_bytes)
    file_extension = file_name.split('.')[-1]
    
    with tempfile.NamedTemporaryFile(suffix=f'.{file_extension}', delete=False) as temp_file:
        temp_path = temp_file.name
        temp_file.write(file_data)
    
    
    match file_extension:
        case 'mp3' | 'ogg':
            text = transcriber_model.audio_to_text(temp_path)
        case _:
            raise Exception('File not supported.')
    
    return text

    
def split_text(document: Document) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, 
        chunk_overlap=500, 
        separators=[''],
        add_start_index=True
    )
    
    if type(document) is str:
        chunks = text_splitter.split_text(document)
    else:
        chunks = text_splitter.split_documents(document)
    
    return chunks
    