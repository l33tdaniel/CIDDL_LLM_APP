import ollama, sys, chromadb, os
from dotenv import load_dotenv
import json
load_dotenv()

def generate_response(query=""):
    embed_model = os.getenv('EMBED_MODEL')
    main_model = os.getenv('MAIN_MODEL')

    chroma = chromadb.HttpClient(host="localhost", port=8000)
    collection = chroma.get_or_create_collection("ciddl_stuff")

    queryembed = ollama.embeddings(model=embed_model, prompt=query)['embedding']

    relevantdocs = collection.query(query_embeddings=[queryembed], 
                                    n_results=3,
                                    include=["documents", 'metadatas']
                                    )
    end_text = ""
    for index, doc in enumerate(relevantdocs['documents']):
        end_text += "ORIGINAL SOURCE LINK: " + str(relevantdocs['metadatas'][index]) + str(doc) + "\n\n"

    modelquery = f"{query} - Answer that question in a personable and conversationable manner using the following text as a resource: {end_text}"

    stream = ollama.generate(model='llama3.1:latest', prompt=modelquery, stream=True)
    output = ""
    for chunk in stream:
        if chunk["response"]:
            #print(chunk['response'], end='', flush=True)
            output += chunk['response']
    links = ''
    for index, link in enumerate(relevantdocs['metadatas'][0]):
        links += link['source'] + ' '
    output += f"\n\nReference Links: {links}\n\n"
    return output