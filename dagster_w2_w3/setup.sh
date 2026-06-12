#!/bin/bash
set -e

# Force the script to execute inside the directory where it lives
cd "$(dirname "$0")"

echo "1. Fetching raw data..."
mkdir -p data
git clone https://github.com/arkadiahn/LEVEL3-projects temp_mlops
cp temp_mlops/mlops/week-2/data/*.csv ./data/
rm -rf temp_mlops
echo "Data extraction complete. Files are correctly placed in $(pwd)/data"

echo "2. Setting up Python environment..."
if ! command -v uv &> /dev/null
then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

uv venv --clear
source .venv/bin/activate
uv pip install -e .
echo "Environment setup complete."

echo "3. Generating secure lakeFS credentials..."

# Only generate a new .env if one doesn't exist to prevent overwriting keys on a live database
if [ ! -f .env ]; then
    # Generate a 20-character Access Key (uppercase letters and numbers)
    GENERATED_ACCESS_KEY="AKIA$(openssl rand -hex 8 | tr '[:lower:]' '[:upper:]')"
    # Generate a 40-character Secret Key (alphanumeric)
    GENERATED_SECRET_KEY="$(openssl rand -base64 35 | tr -dc 'a-zA-Z0-9' | head -c 40)"

    cat <<EOT >> .env
# lakeFS Credentials (Auto-Generated)
LAKECTL_SERVER_ENDPOINT_URL="http://127.0.0.1:8000"
LAKECTL_CREDENTIALS_ACCESS_KEY_ID="${GENERATED_ACCESS_KEY}"
LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY="${GENERATED_SECRET_KEY}"
EOT
    echo "Successfully generated and injected credentials into .env file."
else
    echo ".env file already exists. Skipping credential generation to preserve existing database."
fi

echo "Setup is fully complete! You can now run: docker compose up --build -d"