import json
import os

from sagemaker.huggingface import HuggingFaceModel

from hack_zurich_app.provision.aws import iam, dlc

# sagemaker config
instance_type = "ml.g5.4xlarge"
number_of_gpu = 1
health_check_timeout = 300

# Define Model and Endpoint configuration parameter
config = {
    "HF_MODEL_ID": "meta-llama/Llama-2-7b-chat-hf",  # model_id from hf.co/models
    "SM_NUM_GPUS": json.dumps(number_of_gpu),  # Number of GPU used per replica
    "MAX_INPUT_LENGTH": json.dumps(2048),  # Max length of input text
    "MAX_TOTAL_TOKENS": json.dumps(
        4096
    ),  # Max length of the generation (including input text)
    "MAX_BATCH_TOTAL_TOKENS": json.dumps(
        8192
    ),  # Limits the number of tokens that can be processed in parallel during the generation
    "HUGGING_FACE_HUB_TOKEN": os.environ["HUGGING_FACE_HUB_TOKEN"]
    # ,'HF_MODEL_QUANTIZE': "bitsandbytes", # comment in to quantize
}

# check if token is set
assert (
    config["HUGGING_FACE_HUB_TOKEN"] != "<REPLACE WITH YOUR TOKEN>"
), "Please set your Hugging Face Hub token"


if __name__ == "__main__":
    # create HuggingFaceModel with the image uri
    print(config)
    llm_model = HuggingFaceModel(
        role=iam.get_sagemaker_role(), image_uri=dlc.llm_image(), env=config
    )

    # Deploy model to an endpoint
    # https://sagemaker.readthedocs.io/en/stable/api/inference/model.html#sagemaker.model.Model.deploy
    llm = llm_model.deploy(
        initial_instance_count=1,
        instance_type=instance_type,
        container_startup_health_check_timeout=health_check_timeout,  # 10 minutes to be able to load the model
    )
