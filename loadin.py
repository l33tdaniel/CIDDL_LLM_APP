
# from utilities import readtext, getconfig
import pandas as pd
import requests, ollama
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import chromadb, ollama
import gspread
from mattsollamatools import chunker, chunk_text_by_sentences

load_dotenv()

embed_model = os.getenv('EMBED_MODEL')
main_model = os.getenv('MAIN_MODEL')

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
        chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=7, overlap=2)# We chunk the text
        print(f"with {len(chunks)} chunks")
        for index, chunk in enumerate(chunks):
            embed = ollama.embeddings(model=embed_model, prompt=chunk)['embedding'] # We embed the chunks
            print(embed)
            collection.add([URL+str(index)], [embed], documents=[chunk], metadatas={"source": URL})

def import_info_from_sheets():
    service_account = gspread.service_account('creds.json')
    sheet = service_account.open('Links')
    client = chromadb.HttpClient(host="localhost", port=8000)
    collection = client.get_or_create_collection(name="ciddl_stuff")
    worksheet = sheet.worksheet('Sheet1')
    data = worksheet.get_all_values()

    for URL in data:
        text = get_text_from_url(URL[0]) # Get text from URL
        chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=7, overlap=2) # We chunk the text
        print(f"with {len(chunks)} chunks")
        for index, chunk in enumerate(chunks):
            embed = ollama.embeddings(model=embed_model, prompt=chunk)['embedding'] # We embed the chunks
            print(embed)
            collection.add([URL[0]+str(index)], [embed], documents=[chunk], metadatas={"source": URL[0]})
    
def inspect_db():
    client = chromadb.HttpClient(host="localhost", port=8000)
    collection = client.get_or_create_collection(name="ciddl_stuff")
    print(collection.count())
    print(collection.get())


def delete_all():
    client = chromadb.HttpClient(host="localhost", port=8000)
    client.reset()