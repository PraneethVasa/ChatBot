import openai
import streamlit as st

st.title("ChatGPT-like clone")

# Replace with your actual API key
api_key = "sk-proj-VCJWvAqhCt4mn8PmqqwdT3BlbkFJh7lT7CYpC14JmZ09hJbI"
openai.api_key = api_key

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_chunks = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        assistant_response = ""
        for chunk in response_chunks:
            chunk_message = chunk['choices'][0]['delta'].get('content', '')
            assistant_response += chunk_message
            st.markdown(chunk_message)

    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
