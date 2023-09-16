import os

from hack_zurich_app import file_utils


def polices() -> str:
    return os.path.join(file_utils.data_dir(), "policies")
