# pip install streamlit, langchain-openai

from langchain_openai import ChatOpenAI
import streamlit as st

def main():
    st.set_page_config(page_title="Hack-a-change", page_icon="📜")
    st.title("Hack-a-change")

    open_ai_api_key = st.sidebar.text_input("Input your ChatGPT API key")
    llm = load_llm(open_ai_api_key)

    st.text_input("Question")

def load_llm(open_ai_api_key):
    return ChatOpenAI(
        model="gpt-4o",
        api_key=open_ai_api_key,
        temperature=0.5,
    )

if __name__ == "__main__":
    main()