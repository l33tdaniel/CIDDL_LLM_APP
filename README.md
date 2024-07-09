# Apps Used:

During the process of development, I ended up using **Ollama**, **Llama3**, **nomic-embed-text**, **ChromaDB**, **Python**, and **Google Sheets**. Google sheets is just something that I used as an easy way for a user to be able to add content in that they wanted to have embedded for the LLM, and is in no way necessary. I also left in a CSV file and a way to use manually entry

# Getting Started
If you want to run the following items, I would suggest making a virtual environment in Python and installing the prerequisite libraries from the `requirements.txt` file. Once done with that, you can change the docker-compose.yaml file to make sure the volume where the database will be stored is accurate for your PC and not mine. Finally, ensure that you have Ollama along with whatever LLMs you intend on using installed and ready to go. If you wish to use different models, you can change the .env file. 

# After Installation
Upon loading in the necessary files for embedding in the LLM, you're now able to go and open your browser to `localhost:5000` and use the chatbot as normal.


Sources for portions of code:
Matt Williams’ RAG based implementation: https://www.youtube.com/watch?v=Ml179HQoy9o<br>
UI Chatbot video: https://www.codingnepalweb.com/create-chatbot-html-css-javascript/ 
<br><br>
Feel free to open a PR or submit an issue as you see fit!