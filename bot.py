import openai
import streamlit as st

st.title("ChatGPT-like clone")

# Set your OpenAI API key here
api_key = "sk-proj-VCJWvAqhCt4mn8PmqqwdT3BlbkFJh7lT7CYpC14JmZ09hJbI"
openai.api_key = api_key

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "text-davinci-003"  # Default to text-davinci-003

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
        completion = openai.Completion.create(
            engine="text-davinci-003",  # GPT-3.5-turbo model
            prompt='\n'.join([f"{m['role']}: {m['content']}" for m in st.session_state.messages]),
            max_tokens=150,
            temperature=0.7,  # Adjust temperature for creativity
            top_p=1.0,        # Adjust top_p for diversity
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=None         # Can customize stop tokens
        )
        response = completion.choices[0].text.strip()

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
