from sagemaker.huggingface import get_huggingface_llm_image_uri


def llm_image() -> str:
    return get_huggingface_llm_image_uri("huggingface", version="0.9.3")


if __name__ == "__main__":
    # print ecr image uri
    print(f"llm image uri: {llm_image()}")
