
# from utilities import readtext, getconfig
import pandas as pd
import requests, magic, ollama
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import chromadb, ollama
from mattsollamatools import chunker, chunk_text_by_sentences

load_dotenv()

embed_model = os.getenv('EMBED_MODEL')
main_model = os.getenv('MAIN_MODEL')

#client = chromadb.HttpClient(host="localhost", port=8000)
#print(client.count_collections())
#print(client.get_collection(collection_name))
#collection = chroma.get_or_create_collection(name=collection_name)

def get_text_from_url(URL):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    URL = URL.rstrip()
    URL = URL.replace(' \n', '')
    URL = URL.replace('%0A', '')
    response = requests.get(URL, headers=headers)
    html_text = BeautifulSoup(response.text, 'html.parser')
    return html_text.get_text()

def put_info_in_db():
    df = pd.read_csv('sourcedocs.csv')
    client = chromadb.HttpClient(host="localhost", port=8000)
    collection = client.get_or_create_collection(name="ciddl_stuff")
    for URL in df['URLs']:
        text = get_text_from_url(URL) # Get text from URL
        chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=9, overlap=2)# We chunk the text
        print(f"with {len(chunks)} chunks")
        for index, chunk in enumerate(chunks):
            embed = ollama.embeddings(model=embed_model, prompt=chunk)['embedding'] # We embed the chunks
            print(embed)
            collection.add([URL+str(index)], [embed], documents=[chunk], metadatas={"source": URL})

put_info_in_db()