import os

from langchain import OpenAI


def openai_llm():
    assert "OPENAI_API_KEY" in os.environ

    return OpenAI()


if __name__ == "__main__":
    openai_llm()
