import streamlit as st

zurich_avatar = "./zurich-logo.png"

st.title("Your personal agent")
st.caption("Making insurance easy")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "avatar": zurich_avatar, "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"], avatar=msg["avatar"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "avatar": None, "content": prompt})
    st.chat_message("user").write(prompt)

    msg = {"role": "assistant", "avatar": zurich_avatar, "content": "I don't know... Do you have another question?"}
    st.session_state.messages.append(msg)
    st.chat_message(msg["role"], avatar=msg["avatar"]).write(msg["content"])
