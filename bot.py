import requests
import json
import streamlit as st

st.title("ChatGPT-like clone")

# Set your OpenAI API key here
api_key = "sk-proj-VCJWvAqhCt4mn8PmqqwdT3BlbkFJh7lT7CYpC14JmZ09hJbI"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "text-davinci-003"  # Update with your preferred model

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": st.session_state["openai_model"],
        "messages": [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        "max_tokens": 150
    }

    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)
    if response.status_code == 200:
        assistant_response = response.json()["choices"][0]["text"].strip()
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    else:
        st.error("Failed to get response from OpenAI. Please try again later.")
