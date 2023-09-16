import json
import os
import logging

from langchain import OpenAI
from langchain.llms.sagemaker_endpoint import LLMContentHandler, SagemakerEndpoint


logger = logging.getLogger(__file__)


class ContentHandler(LLMContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt: str, model_kwargs: dict) -> bytes:
        input_str = json.dumps({"inputs": prompt, **model_kwargs})
        logger.info(input_str)
        return input_str.encode("utf-8")

    def transform_output(self, output: bytes) -> str:
        response_json = json.loads(output.read().decode("utf-8"))
        return response_json[0]["generated_text"]


def llama2_7b_chat_hf_llm():
    return SagemakerEndpoint(
        endpoint_name="huggingface-pytorch-tgi-inference-2023-09-16-09-44-19-779",
        region_name="eu-west-1",
        model_kwargs={
            "do_sample": True,
            "top_p": 0.6,
            "temperature": 0,
            "top_k": 50,
            "max_new_tokens": 512,
            "repetition_penalty": 1.03,
            "stop": ["</s>"],
        },
        content_handler=ContentHandler(),
    )


def openai_llm():
    assert "OPENAI_API_KEY" in os.environ

    return OpenAI(temperature=0.0)


if __name__ == "__main__":
    llama2_7b_chat_hf_llm()
