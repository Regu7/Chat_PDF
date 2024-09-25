import argparse
import os
import pickle
import random
import warnings
from dataclasses import dataclass
from datetime import datetime

import streamlit as st
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores.chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from transformers import pipeline

from utils.create_database import Create_Database
from utils.preprocess import finalpreprocess

warnings.filterwarnings("ignore")

abs_path = os.path.dirname(os.path.abspath(__file__))

CHROMA_PATH = os.path.join(abs_path, "chroma")

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def out_of_context(text):
    greet_dict = {
        "patterns": [
            "hello",
            "hi!",
            "good morning!",
            "good evening",
            "good afternoon",
            "hey",
            "whats up",
            "is anyone there?",
            "hi there!",
            "greetings!",
            "good to see you!",
            "hi",
            "hii",
        ],
        "responses": [
            "Hello. Welcome to chat pdf",
            "Welcome",
            "Hi there",
        ],
    }
    if text.lower() in greet_dict["patterns"]:
        return random.choice(greet_dict["responses"])
    else:
        return """Sorry, I'm not trained to answer this specific question.
                Please ask me a different question"""


def chat_response(user_query):
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    chat = ChatOpenAI()
    results = db.similarity_search_with_relevance_scores(user_query, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        return out_of_context(user_query)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=user_query)
    print(prompt)

    conversation = ConversationChain(
        llm=chat,
        memory=ConversationSummaryBufferMemory(llm=ChatOpenAI(), max_token_limit=2048),
        verbose=False,
    )

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    print("Sources :", sources)

    response_text = conversation.invoke(input=prompt)
    return response_text["response"]


def main():
    st.title("PDF Chatbot")
    start_chat = None

    if "doc_create" not in st.session_state or st.session_state.doc_create != 1:
        file_directory = f"data3/{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"

        if not os.path.exists(file_directory):
            os.makedirs(file_directory)
            print("file directory created")

        uploaded_files = st.file_uploader(
            "Choose a CSV file", accept_multiple_files=True
        )

        if uploaded_files:
            for uploaded_file in uploaded_files:
                bytes_data = uploaded_file.read()
                file_path = os.path.join(file_directory, uploaded_file.name)

                with open(file_path, "wb") as file:
                    file.write(bytes_data)
            cd = Create_Database(CHROMA_PATH,file_directory)
            cd.main_func()
            st.write(
                "Files added to the data store. You can proceed with questions now"
            )
            st.session_state.doc_create = 1
            start_chat = "Y"
    else:
        start_chat = "Y"

    st.write("PDF Assistant which provides answers from the PDF file")

    if "history" not in st.session_state:
        st.session_state.history = []

    if start_chat == "Y":
        user_input = st.chat_input("How can I help you?")
        if user_input:
            response = chat_response(user_input)
            st.session_state.history.append((user_input, response))

        for user_input, response in st.session_state.history:
            st.write(f"You: {user_input}")
            st.write(f"Chatbot: {response}")


if __name__ == "__main__":
    main()
