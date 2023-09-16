import functools
import os
import pathlib

filepath = pathlib.Path(__file__).resolve()

@functools.lru_cache(maxsize=1)
def project_root() -> str:
    return filepath.parent.parent

@functools.lru_cache(maxsize=1)
def source_dir() -> str:
    return filepath.parent

@functools.lru_cache(maxsize=1)
def configurations_dir() -> str:
    return os.path.join(project_root(), "configurations")

@functools.lru_cache(maxsize=1)
def data_dir() -> str:
    return os.path.join(configurations_dir(), "data")

if __name__ == "__main__":
    print(configurations_dir())