import base64
import os
import sys

import streamlit as st

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)

if parent_dir not in sys.path:
    sys.path.append(parent_dir)


from hack_zurich_app import file_utils
from hack_zurich_app.agents.support_answer import SupportAnswer
from hack_zurich_app.agents.support_center import SupportCenter


zurich_avatar = f"{file_utils.data_dir()}/zurich-logo.png"


def secrets_to_env_var():
    for key, value in st.secrets.aws_credentials.items():
        os.environ[key] = value
    for key, value in st.secrets.llm_credentials.items():
        os.environ[key] = value


@st.cache_resource
def load_support_center():
    print("Initializing policies QA chain...")
    return SupportCenter()


def build_message_from_support_answer(answer: SupportAnswer):
    return {
        "role": "assistant",
        "avatar": zurich_avatar,
        "content": answer.answer,
        "document_path": answer.document_path
    }


def print_message(msg):
    st.chat_message(msg["role"], avatar=msg["avatar"]).write(msg["content"])
    if "document_path" in msg:
        display_pdf(msg["document_path"])


def display_pdf(document_path):
    with open(document_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    pdf_display = (
        f'<iframe src="data:application/pdf;base64,{base64_pdf}" '
        f'width="700" height="1000" type="application/pdf"></iframe>'
    )

    document_name = document_path.split("/")[-1]
    with st.expander(document_name):
        st.markdown(pdf_display, unsafe_allow_html=True)


def refresh():
    support_center = load_support_center()

    st.title("Your personal agent")
    st.caption("We got you covered - Making insurance easy")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "avatar": zurich_avatar,
                "content": "How can I help you?",
            }
        ]

    for msg in st.session_state.messages:
        print_message(msg)

    if prompt := st.chat_input():
        st.session_state.messages.append(
            {"role": "user", "avatar": None, "content": prompt}
        )
        st.chat_message("user").write(prompt)

        support_answer = support_center.ask(prompt)

        msg = build_message_from_support_answer(support_answer)
        st.session_state.messages.append(msg)

        print_message(msg)


secrets_to_env_var()
refresh()
