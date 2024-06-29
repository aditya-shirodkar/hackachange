# pip install streamlit, langchain-openai

import streamlit as st


def main():
    st.set_page_config(page_title="Hack-a-change", page_icon="📜")
    st.title("Hack-a-change")

    vid_option = st.sidebar.radio(
        "Which video would you like to process?",
        (
            "class 3_contractions-of-words",
            "Class 9_Social Sciences",
            "Class 11_Biology_nervous-system",
        ),
    )
    vid = vid_picker(vid_option)
    load_video(vid)

    question = st.text_input("Question")
    ask_question(question, vid_option)


def vid_picker(vid_option):
    if vid_option == "class 3_contractions-of-words":
        return "https://dl.dropboxusercontent.com/scl/fi/gqrwshvzijg6jew9bmypp/class-3_contractions-of-words.mp4?rlkey=f8om8ln3e6tt20n39ei66kugu&st=c03orq2i&dl=0"
    if vid_option == "Class 9_Social Sciences":
        return "https://dl.dropboxusercontent.com/scl/fi/h33heodx442mmerepmvog/Class-9_Social-Sciences.mp4?rlkey=x4tni5rnn7948nthgd9a8of2y&st=wxw11s5k&dl=0"
    if vid_option == "Class 11_Biology_nervous-system":
        return "https://dl.dropboxusercontent.com/scl/fi/ug8419ue3a8rkm0ey84cz/Class-11_Biology_nervous-system.mp4?rlkey=byk4rx1piopcovwpiyagdc2h3&st=iof5yr53&dl=0"


def load_video(vid):
    data = vid
    vid_placeholder = st.empty()
    vid_placeholder.video(data=data)

    button_90 = st.button("Go to 90 secs")

    if button_90:
        vid_placeholder.empty()
        vid_placeholder.video(data=data, start_time=90)


def ask_question(question, vid_option):
    subtitle_filename = vid_option + ".txt"
    pass


# def load_llm(open_ai_api_key):
#     return ChatOpenAI(
#         model="gpt-4o",
#         temperature=0.5,
#     )


if __name__ == "__main__":
    main()
