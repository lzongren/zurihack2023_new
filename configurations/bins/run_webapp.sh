#!/bin/bash

# Get the current directory
current_dir="$(pwd)"
project_root_dir="$(dirname "$(dirname "$current_dir")")"

webapp_dir=$project_root_dir/hack_zurich_app/webapp

cd $webapp_dir && pipenv run streamlit run main.py