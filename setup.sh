#!/bin/bash

set -e

echo "1. Fetching raw data..."

git clone https://github.com/arkadiahn/LEVEL3-projects temp_mlops

cp -R temp_mlops/mlops ~/mlops_course/.

cd dagster_w2_w3

rm -rf temp_mlops

echo "Data extraction complete."

echo "2. Setting up Python environment..."

if ! command -v uv &> /dev/null
then
    echo "installing uv!..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

uv venv --clear
source .venv/bin/activate

uv pip install -e .
echo "Environment setup complete."

echo "3. Preparing environment variables..."

if [ ! -f .env ]; then
    cat <<EOT >> .env
# lakeFS Credentials
LAKECTL_SERVER_ENDPOINT_URL="http://127.0.0.1:8000"
LAKECTL_CREDENTIALS_ACCESS_KEY_ID=""
LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY=""
EOT
    echo "Created a template .env file. Please open it and paste your lakeFS keys."
else
    echo ".env file already exists. Skipping creation."
fi