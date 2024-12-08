import streamlit as st
import pandas as pd
from openai import OpenAI

st.title("😆 Punbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses using puns. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    client = OpenAI(api_key=openai_api_key)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"


    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question and the bot will respond with a pun!"):

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Punbot, a chatbot that always responds with a witty and humorous pun, regardless of the user's input."}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    if st.session_state.messages:
        df = pd.DataFrame(st.session_state.messages)
        st.write('### Conversation History')
        st.dataframe(df)

        csv = df.to_csv(index=False)
        st.download_button(
            label = "Download Conversation History as CSV",
            data = csv,
            file_name = "punbot_conversation_history.csv",
            mime = "text/csv"
        )
