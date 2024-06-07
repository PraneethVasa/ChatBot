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

    with st.spinner("Thinking..."):
        assistant_response = openai.Completion.create(
            engine=st.session_state["openai_model"],
            prompt='\n'.join([f"{m['role']}: {m['content']}" for m in st.session_state.messages]),
            max_tokens=150
        ).choices[0].text.strip()

    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

