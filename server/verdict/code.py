from dotenv import load_dotenv
load_dotenv()

def load_document(file):
    import os
    name, extension = os.path.splitext(file)
    if extension == '.pdf':
        from langchain.document_loaders import PyPDFLoader
        print(f'Loading {file}')
        loader = PyPDFLoader(file)
    elif extension == '.docx':
        from langchain.document_loaders import Docx2txtLoader
        print(f'Loading {file}')
        loader = Docx2txtLoader(file)
    elif extension == '.txt':
        from langchain.document_loaders import TextLoader
        loader = TextLoader(file)
    else:
        print('Document format is not supported!')
        return None
    data = loader.load()
    return data


import regex as re
def text_formatter(text):
    clean_text = text.replace("\n", " ").strip()
    clean_text = re.sub(r"[^a-zA-Z0-9\s.,;:'\"!?()-]", "", clean_text)
    return clean_text

def clean(data):
    data_cleaned = []
    for i, page in enumerate(data):
        data_cleaned.append({
            "Content": text_formatter(page.page_content),
            "PageNumber": i + 1
        })
    return data_cleaned

from spacy.lang.en import English
def sentencizer(pages_and_texts):
    lang = English()
    lang.add_pipe("sentencizer")
    for item in pages_and_texts:
        item["sentences"] = list(lang(item["Content"]).sents)
        item["sentences"] = [str(sentence) for sentence in item["sentences"]]


def split_list(input_list, slice_size):

    return [input_list[i:i + slice_size] for i in range(0, len(input_list), slice_size)]

def chunker(data,num_sentence_chunk_size):
    for item in data:
        item["sentence_chunks"] = split_list(input_list=item["sentences"],
                                            slice_size=num_sentence_chunk_size)
        item["num_chunks"] = len(item["sentence_chunks"])


import re

def join_sentences(data):
    pages_and_chunks = []
    for item in data:
        for sentence_chunk in item["sentence_chunks"]:
            chunk_dict = {}
            chunk_dict["page_number"] = item["PageNumber"]
            
            joined_sentence_chunk = "".join(sentence_chunk).replace("  ", " ").strip()
            joined_sentence_chunk = re.sub(r'\.([A-Z])', r'. \1', joined_sentence_chunk)
            chunk_dict["sentence_chunk"] = joined_sentence_chunk
            pages_and_chunks.append(chunk_dict)
    return pages_and_chunks



from sentence_transformers import SentenceTransformer
def embedding(final_chunked_data):
    embedding_model = SentenceTransformer(model_name_or_path="all-mpnet-base-v2") 
    for item in final_chunked_data:
        item["embedding"] = embedding_model.encode(item["sentence_chunk"])
        print(item["sentence_chunk"])


def list_converter(final_chunked_data):
    documents = [item["sentence_chunk"] for item in final_chunked_data]
    # pageNumbers = [item["page_number"] for item in final_chunked_data]
    embedding = [item["embedding"].tolist() for item in final_chunked_data]

    id = [f"id{x}" for x,item in enumerate(final_chunked_data)]
    return documents, embedding,id


def db(documents,embeddings,id,name):
    import chromadb

    chroma_client = chromadb.Client()

    existing_collections = chroma_client.list_collections()
    print(existing_collections)
    if name in [col.name for col in existing_collections]:
        collection = chroma_client.get_collection(name=name)
        print(f"Using existing collection: {name}")
    else:
        collection = chroma_client.create_collection(name=name)
        print(f"Created new collection: {name}")
    collection.add(documents=documents,embeddings=embeddings,ids=id)
    return collection



async def search_result(query,collection,n_result):
    embedding_model = SentenceTransformer(model_name_or_path="all-mpnet-base-v2")
    query_embeddings = embedding_model.encode(query).tolist()
    results = collection.query(query_embeddings=query_embeddings, n_results=n_result)
    return results


from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
def convo_template(llm):
    memory = ConversationSummaryBufferMemory(llm=llm,max_token_limit=1000) 
    conversation = ConversationChain(
        llm=llm, 
        verbose=False,
        memory=memory
)
    return conversation



from langchain import PromptTemplate
template = ''' Answer the current question in detail. You may make use of the context to make your response better, but do not solely rely on the context and make that if the question is on laws and regulations, your answers are purely based on only INDIAN laws and regulations. 

    Question: {query}

    Context: {context_str}

    Respond with only the answer and do not add anything else.
    '''
prompt = PromptTemplate(
            input_variables=['query','context'],
            template=template
        )



from langchain_ollama import OllamaLLM
llm = OllamaLLM(model="llama3.1",temperature=0.2)



chat=convo_template(llm)


from transformers import GPT2TokenizerFast
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")