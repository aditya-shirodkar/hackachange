# pip install streamlit, langchain-openai

from langchain_openai import ChatOpenAI
import streamlit as st


def main():
    st.set_page_config(page_title="Hack-a-change", page_icon="📜")
    st.title("Hack-a-change")

    test = st.sidebar.text_input("Test")
    # llm = load_llm(open_ai_api_key)

    st.video(
        data="https://dl.dropboxusercontent.com/scl/fi/ug8419ue3a8rkm0ey84cz/Class-11_Biology_nervous-system.mp4?rlkey=byk4rx1piopcovwpiyagdc2h3&st=iof5yr53&dl=0"
    )

    st.text_input("Question")


# def load_llm(open_ai_api_key):
#     return ChatOpenAI(
#         model="gpt-4o",
#         temperature=0.5,
#     )


if __name__ == "__main__":
    main()
