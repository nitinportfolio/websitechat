import streamlit as st
from utils import *
import constants

# Creating Session State Variables

if "HuggingFace_API_Key" not in st.session_state:
    st.session_state["HuggingFace_API_Key"] = ""

if "Pinecone_API_Key" not in st.session_state:
    st.session_state["Pinecone_API_Key"] =""

st.title("🤖 AI Agent for NitinAI.xyz")

# *************Sidebar Functionality ****************
# Sidebar to capture API Keys

st.sidebar.title("🔑")
st.session_state["HuggingFace_API_Key"] = st.sidebar.text_input("What's your HuggingFace API Key?", type="password")
st.session_state["Pinecone_API_Key"] = st.sidebar.text_input("What's your Pinecone API Key?", type="password")

# PINECONE_API_KEY environment variable for Pinecone usage

import os
os.environ["PINECONE_API_KEY"] = st.session_state["Pinecone_API_Key"]

load_button = st.sidebar.button("Load data to Pinecone", key = "load_data")


# If button is clicked, it will push data to Pinecone

if load_button:
    
    # Proceed only if API Keys are provided
    if st.session_state["HuggingFace_API_Key"]!= "" and st.session_state["Pinecone_API_Key"]!="":

        # Fetch data from site
        site_data=get_website_data(constants.WEBSITE_URL)
        st.write("Data pull done ...")
        #st.write(site_data)

        # Split data into chunks
        chunks_data = split_data(site_data)
        st.write("Splitting data done ...")

        # Creating Embeddings instance
        embeddings = create_embeddings()
        st.write("Embeddings instance creation done ...")

        # Push data to Pinecone
        push_to_pinecone(st.session_state["Pinecone_API_Key"], constants.PINECONE_ENVIRONMENT, constants.PINECONE_INDEX, embeddings, chunks_data)
        st.write("Pushing data to Pinecone done")

        st.sidebar.success("Data pushed to Pinecone successfully!!")

    else:
        st.sidebar.error("Ooopssss!!! Please provide the API Keys")



# *******************SIDE BAR FUNCTIONALITY ENDED **************************

# Captures user inputs
prompt = st.text_input("How can I help you with today ?", key="prompt")
document_count = st.slider("No of links to return - (0 LOW || 5 HIGH)", 0,5,2, step = 1)
submit = st.button("Search")


if submit:
    #Proceed only if API keys are provided
    if st.session_state["HuggingFace_API_Key"] !="" and st.session_state["Pinecone_API_Key"] !="":

        # create embeddings instance
        embeddings=create_embeddings()
        st.write("Embeddings instance creation done ...")

        # Pull index data from Pinecone
        index = pull_from_pinecone(st.session_state["Pinecone_API_Key"], constants.PINECONE_ENVIRONMENT, constants.PINECONE_INDEX, embeddings)
        st.write("Pinecone index retrieval done ...")

        # Fetch relavant documents from Pinecone index
        relavant_docs = get_similar_docs(index, prompt, document_count)
        st.write(relavant_docs)

        # Displaying search results
        st.write("Search results list ....")

        for document in relavant_docs:
            st.write("**Result :"+ str(relavant_docs.index(document)+1)+"**")
            st.write("**Info**: "+document.page_content)
            st.write("**Link**: "+ document.metadata["source"])

    else:
        st.sidebar.error("Oooopssss!!! Please provide correct API Keys....")





































































