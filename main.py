# pip install streamlit, langchain-openai

from langchain_openai import ChatOpenAI
import streamlit as st


def main():
    st.set_page_config(page_title="Hack-a-change", page_icon="📜")
    st.title("Hack-a-change")

    test = st.sidebar.text_input("Test")
    # llm = load_llm(open_ai_api_key)

    st.text_input("Question")


# def load_llm(open_ai_api_key):
#     return ChatOpenAI(
#         model="gpt-4o",
#         temperature=0.5,
#     )


if __name__ == "__main__":
    main()
