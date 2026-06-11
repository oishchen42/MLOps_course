#!/bin/sh
set -e

echo "Waiting for LakeFS API to be alive..."

export LAKECTL_SERVER_ENDPOINT_URL="http://lakefs:8000"

until lakectl repo list; do
  echo "lakectl connection failed. Retrying in 2 seconds..."
  sleep 2
done
echo "LakeFS is healthy!"

echo "Ensuring 'bike-rentals' repository exists..."
if ! lakectl repo list | grep -q "bike-rentals"; then
  # FIX: local://data is now a positional argument, not a flag
  lakectl repo create lakefs://bike-rentals local://data --default-branch main
else
  echo "Repository already exists."
fi

echo "Uploading CSV files..."
if [ -z "$(ls -A /data/*.csv 2>/dev/null)" ]; then
    echo "ERROR: No CSV files found in the /data/ directory!"
    exit 1
fi

for f in /data/*.csv; do
  if [ -f "$f" ]; then
      filename=$(basename "$f")
      echo "Uploading $filename..."
      lakectl fs upload "lakefs://bike-rentals/main/data/$filename" --source "$f"
  fi
done

echo "Data upload complete."