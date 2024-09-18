from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Pinecone
#from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone as PineconeClient
from langchain_community.document_loaders import SitemapLoader
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from bs4 import BeautifulSoup as Soup
import asyncio

# Function to fetch data from website
def get_website_data(sitemap_url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loader = RecursiveUrlLoader(
    #loader = SitemapLoader(
        sitemap_url
    )
    docs = loader.load()

    return docs

# Function to split data into smaller chunks
def split_data(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len,
    )
    docs_chunks = text_splitter.split_documents(docs)
    return docs_chunks

# Function to create embeddings instance
def create_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
    #SentenceTransformerEmbeddings(model_name = "all-MiniLM-L6-v2")
    return embeddings

# Function to push data to pinecone
def push_to_pinecone(pinecone_apikey, pinecone_environment, pinecone_index_name, embeddings, docs):

    PineconeClient(
        api_key=pinecone_apikey,
        environment=pinecone_environment
    )
    index_name = pinecone_index_name
    index = Pinecone.from_documents(docs, embeddings, index_name=index_name)
    return index

# Function to pull index data from Pinecone
def pull_from_pinecone(pinecone_apikey, pinecone_environment, pinecone_index_name, embeddings):
    PineconeClient(
        api_key=pinecone_apikey,
        environment=pinecone_environment
    )
    index_name = pinecone_index_name
    index = Pinecone.from_existing_index(index_name, embeddings)
    return index

# Function will fetch the top relevant documents from our vector store - Pinecone Index
def get_similar_docs(index, query, k = 2):
    similar_docs = index.similarity_search(query, k=k)
    return similar_docs