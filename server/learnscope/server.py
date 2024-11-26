import uvicorn 
from fastapi  import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from code import (
    load_document, clean, sentencizer, chunker, join_sentences, embedding,
    list_converter, db, search_result, chat, prompt, join_text, prompt2 )
import os
import time

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print('Loading')
    

def create_collection(file_path,collection_name):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist")
        return None
    data  = load_document(file_path)
    if data is None:
        print(f"Warning: Failed to load document: {file_path}")
        return None
    print(f"Creating collection for: {collection_name}")
    final_data = clean(data)
    sentencizer(final_data)
    chunker(final_data,12)
    final_chunked_data = join_sentences(final_data)
    embedding(final_chunked_data)
    documents, embeddings, ids = list_converter(final_chunked_data)
    return db(documents,embeddings,ids,collection_name)

def get_text(file_path):
    data  = load_document(file_path)
    final_data = clean(data)
    sentencizer(final_data)
    text = join_text(final_data)
    return text


@app.post("/query")
async def get_response(request:QueryRequest):
    query = request.query
    context_str = await search_result(query,collection,3)
    response = chat(prompt.format(query=query,context_str = context_str['documents']))
    return {"response":response['response']}


@app.post("/summary")
async def get_summary():
    global collection
    time.sleep(5)
    collection = create_collection(r'D:\Coding\React\Project UI\LearnScope\VerdictIQ\public\uploaded_file.pdf' , 'File')
    text = get_text(r'D:\Coding\React\Project UI\LearnScope\VerdictIQ\public\uploaded_file.pdf')
    response = chat(prompt2.format(content= text))
    return {"response":response['response']}


if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8005)