import ollama, sys, chromadb, os
from dotenv import load_dotenv
load_dotenv()

def generate_response(query=""):
    embed_model = os.getenv('EMBED_MODEL')
    main_model = os.getenv('MAIN_MODEL')

    chroma = chromadb.HttpClient(host="localhost", port=8000)
    collection = chroma.get_or_create_collection("ciddl_stuff")

    queryembed = ollama.embeddings(model=embed_model, prompt=query)['embedding']

    relevantdocs = collection.query(query_embeddings=[queryembed], n_results=5)["documents"][0]
    docs = "\n\n".join(relevantdocs)
    modelquery = f"{query} - Answer that question using the following text as a resource: {docs}"

    stream = ollama.generate(model=main_model, prompt=modelquery, stream=True)
    output = ""
    for chunk in stream:
        if chunk["response"]:
            print(chunk['response'], end='', flush=True)
            output += chunk['response']
    return output
