import streamlit as st
import requests
import uuid
from dotenv import load_dotenv
import os
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
BACKEND_URL = f"{BACKEND_URL}/chat"
st.set_page_config(page_title="HR Policy Assistant", layout="centered")
st.title("🧠 AgiraSoft HR Policy Assistant")

# ----------------------------
# Session handling (in-memory)
# ----------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    print(f"New session started: {st.session_state.session_id}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------
# Display chat history
# ----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------
# Chat input
# ----------------------------
user_input = st.chat_input("Ask a policy-related question")
full_response = None
if user_input:
    # show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    payload = {
        "session_id": st.session_state.session_id,
        "message": user_input
    }

    # Placeholder for assistant streaming text
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        response = requests.post(
            BACKEND_URL,
            json=payload,
            stream=True,
            timeout=60
        )

        content_type = response.headers.get("content-type", "")

        # Case 1: normal JSON response
        if "application/json" in content_type:
            data = response.json()
            full_response = data.get("answer", "")
            placeholder.markdown(full_response)

        # Case 2: streaming text
        else:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    text = chunk.decode("utf-8")
                    full_response += text
                    placeholder.markdown(full_response)

if full_response:
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
