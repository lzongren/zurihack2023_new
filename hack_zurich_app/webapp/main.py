import streamlit as st

from hack_zurich_app import file_utils
from hack_zurich_app.rag.chain import policies_qa_chain


@st.cache_resource
def load_qa_chain():
    print("Initializing policies QA chain...")
    return policies_qa_chain()


qa_chain = load_qa_chain()

zurich_avatar = f"{file_utils.data_dir()}/zurich-logo.png"

st.title("Your personal agent")
st.caption("We got you covered - Making insurance easy")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "avatar": zurich_avatar, "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"], avatar=msg["avatar"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "avatar": None, "content": prompt})
    st.chat_message("user").write(prompt)

    result = qa_chain.run(prompt)
    msg = {"role": "assistant", "avatar": zurich_avatar, "content": result}
    st.session_state.messages.append(msg)
    st.chat_message(msg["role"], avatar=msg["avatar"]).write(msg["content"])
