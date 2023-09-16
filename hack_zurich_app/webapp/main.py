import base64

import streamlit as st

from hack_zurich_app import file_utils
from hack_zurich_app.rag.chain import policies_qa_chain

zurich_avatar = f"{file_utils.data_dir()}/zurich-logo.png"


@st.cache_resource
def load_qa_chain():
    print("Initializing policies QA chain...")
    return policies_qa_chain()


def build_message_from_output(chain_output):
    result = chain_output["result"]

    document_used = chain_output["source_documents"][0].metadata
    document_path = document_used['source']
    document_name = document_path.split("/")[-1]
    result += f"\n\n See {document_name} page {document_used['page']}."

    return {"role": "assistant", "avatar": zurich_avatar, "content": result, "document_path": document_path}


def print_message(msg):
    st.chat_message(msg["role"], avatar=msg["avatar"]).write(msg["content"])
    if "document_path" in msg:
        display_pdf(msg['document_path'])


def display_pdf(document_path):
    with open(document_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" ' \
                  f'width="700" height="1000" type="application/pdf"></iframe>'

    document_name = document_path.split("/")[-1]
    with st.expander(document_name):
        st.markdown(pdf_display, unsafe_allow_html=True)


def refresh():
    qa_chain = load_qa_chain()

    st.title("Your personal agent")
    st.caption("We got you covered - Making insurance easy")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "avatar": zurich_avatar, "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        print_message(msg)

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "avatar": None, "content": prompt})
        st.chat_message("user").write(prompt)

        chain_output = qa_chain(prompt)

        msg = build_message_from_output(chain_output)
        st.session_state.messages.append(msg)

        print_message(msg)


refresh()
