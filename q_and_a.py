import os
import re
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import streamlit as st


path_to_transcripts = "./subtitles"

os.environ["GOOGLE_API_KEY"] = st.secrets["google_genai_api_key"]


def extract_timestamp(string):
    pattern = r"\[(\d+)\.\d+ sec\]"
    match = re.search(pattern, string)
    if match:
        return int(match.group(1))
    return None


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def load_documents(folder_path):
    # Initialize an empty dictionary to store documents
    documents_dict = {}

    # Iterate over each file in the directory
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # Ensure only text files are considered
            file_path = os.path.join(folder_path, filename)
            loader = TextLoader(
                file_path
            )  # Assuming TextLoader is correctly implemented
            document = loader.load()  # Load the document
            # Remove the .txt extension from filename for dictionary key
            key = filename[:-4] if filename.endswith(".txt") else filename
            documents_dict[
                key
            ] = document  # Store document in dictionary with filename as key

    return documents_dict


def create_vectorstores(documents_dict):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1, chunk_overlap=0)

    # Initialize an empty dictionary to store processed texts
    texts_dict = {}

    # Iterate over each document in documents_dict
    for filename, document in documents_dict.items():
        # Assuming text_splitter.split_documents splits the document into texts
        texts = text_splitter.split_documents(document)
        texts_dict[filename] = texts  # Store texts in texts_dict with filename as key

    # Now texts_dict contains processed texts from each document in documents_dict

    vectorstores_dict = {}

    for filename, texts in texts_dict.items():
        # Create vector store for each set of texts
        vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
        )

        # Convert vectorstore to retriever
        retriever = vectorstore.as_retriever()

        # Store retriever in vectorstores_dict with filename as key
        vectorstores_dict[filename] = retriever

    return vectorstores_dict


def unique_items(lst):
    unique = []
    for item in lst:
        if item not in unique:
            unique.append(item)
    return unique


def retrieve_relevant(question, vid_option, vectorstores_dict):
    retrieved = vectorstores_dict[vid_option].invoke(question)
    retrieved = vectorstores_dict["Class 11_Biology_nervous-system"].invoke(
        "What is the central nervous system?"
    )
    retrieved_unique = unique_items(retrieved)
    return retrieved_unique


def get_timestamps(retrieved_relevant):
    timestamps = [extract_timestamp(doc.page_content) for doc in retrieved_relevant]
    return timestamps


def generate_response(question, retrieved_relevant):
    template = """You are an assistant for question-answering tasks. You are expected to generate an answer based on the context and to find out a timestep in the context.

    Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.\nQuestion: {question} \nContext: {context}."""

    prompt = ChatPromptTemplate(
        input_variables=["context", "question"],
        messages=[
            HumanMessagePromptTemplate(
                prompt=PromptTemplate(
                    input_variables=["context", "question"], template=template
                )
            )
        ],
    )
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7, top_p=0.85)
    formatted_retrieved_unique = format_docs(retrieved_relevant)

    # Chain
    rag_chain = (
        {
            "context": lambda x: formatted_retrieved_unique,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    # Question
    return rag_chain.invoke(question)


def ask_question(question, vid_option, path=path_to_transcripts):
    documents_dict = load_documents(path)
    vectorstores_dict = create_vectorstores(documents_dict)
    retrieved_relevant = retrieve_relevant(question, vid_option, vectorstores_dict)
    timestamps = get_timestamps(retrieved_relevant)
    response = generate_response(question, retrieved_relevant)
    return response, timestamps
