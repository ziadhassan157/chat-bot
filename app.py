import streamlit as st
import requests
import uuid

st.title("Chatbot")

url = "http://127.0.0.1:8000/chat/"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "userid" not in st.session_state:
    st.session_state.userid = str(uuid.uuid4())  
if "input_value" not in st.session_state:
    st.session_state.input_value = ""  

query = st.text_input("Enter Ur Query", value=st.session_state.input_value, key="query_input")

if st.button("Submit") and query:
    payload = {
        "userid": st.session_state.userid,
        "message": query
    }

    with requests.post(url, json=payload, stream=False) as r:
        r.raise_for_status()
        response_data = r.json()
        bot_response = response_data.get("answer", "No response found.")

        st.session_state.chat_history.append(("User", query))
        st.session_state.chat_history.append(("Bot", bot_response))
        
        st.session_state.input_value = ""

for role, message in st.session_state.chat_history:
    if role == "User":
        st.text(f"User :{message}")
    if role == "Bot":
        st.text(f"Bot :{message}")