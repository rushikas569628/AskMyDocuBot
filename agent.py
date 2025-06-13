import os 
# Provides functionalities for interacting with the operating system.
from dotenv import load_dotenv
#  Loads environment variables from a .env file into the script.
from langchain.embeddings import OpenAIEmbeddings
# Allows embedding text into numerical vectors using OpenAI models.
from langchain.vectorstores import FAISS
# A library for efficient similarity search and clustering of dense vectors.
from langchain.chains import RetrievalQA
# Sets up a question-answering system based on retrieved documents.
from langchain.chat_models import ChatOpenAI
# Interface to interact with OpenAI's chat models.
from Templates.utils import load_pdf_chunks
# Custom utility function to load and split PDF documents into manageable chunks.
# Loads environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def create_pdf_agent(pdf_path):
    docs = load_pdf_chunks(pdf_path)
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    # Creates embeddings (numerical representations) of text using OpenAI models.
    vectorstore = FAISS.from_documents(docs, embeddings)
    #Constructs a vector store using FAISS, which organizes and indexes the text chunks based on their embeddings.
    #Configures the retrieval mechanism to find documents similar to a query, retrieving up to 5 results.
    retriever = vectorstore.as_retriever(search_type="similarity", k=5)

    #Initializes a chat model using OpenAI's GPT-3.5-turbo variant, which can generate human-like responses.
    llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.1, model_name="gpt-3.5-turbo")
    # Constructs a question-answering system that uses the chat model (llm) and document retriever (retriever) to provide answers based on the retrieved documents.
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
    return qa
