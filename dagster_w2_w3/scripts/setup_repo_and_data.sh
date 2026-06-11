#!/bin/sh
set -e

until curl -s http://lakefs:8000/_health | grep -q "alive"; do
  echo "Waiting for LakeFS API..."
  sleep 2
done

ACCESS_KEY="${LAKEFS_ADMIN_ACCESS_KEY_ID:-AKIAIOSFODNN7EXAMPLE}"
SECRET_KEY="${LAKEFS_ADMIN_SECRET_ACCESS_KEY:-wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY}"

if ! curl -s -u "$ACCESS_KEY:$SECRET_KEY" http://lakefs:8000/api/v1/repositories | grep -q '"name":"bike-rentals"'; then
  echo "Creating repository 'bike-rentals'..."
  curl -X POST http://lakefs:8000/api/v1/repositories \
    -H 'Content-Type: application/json' \
    -u "$ACCESS_KEY:$SECRET_KEY" \
    -d '{"name": "bike-rentals", "storage_namespace": "local://data", "default_branch": "main"}'
else
  echo "Repository already exists."
fi

for f in /data/*.csv; do
  filename=$(basename "$f")
  echo "Uploading $filename..."
  curl -X PUT "http://lakefs:8000/api/v1/repositories/bike-rentals/refs/main/objects/data/$filename" \
    -u "$ACCESS_KEY:$SECRET_KEY" \
    --data-binary "@$f" \
    -H "Content-Type: text/csv"
  echo
done

echo "Data upload complete."