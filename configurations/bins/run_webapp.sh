#!/bin/bash

# Get the current directory
current_dir="$(pwd)"
project_root_dir="$(dirname "$(dirname "$current_dir")")"

webapp_dir=$project_root_dir/hack_zurich_app/webapp

export PYTHONPATH="$project_root_dir"

if [ -z "$OPENAI_API_KEY" ]; then
    echo "The environment variable OPENAI_API_KEY is not set. Exiting."
    exit 1
fi

cd "$webapp_dir" && pipenv run streamlit run main.py
