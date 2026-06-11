#!/bin/sh
set -e

until curl -s http://lakefs:8000/_health | grep -q '"status":"ok"'; do
  echo "Waiting for LakeFS..."; sleep 2;
done

if [ ! -f /home/lakefs/.lakefs_setup_complete ]; then
  lakefs setup \
    --user-name admin \
    --access-key-id "${LAKEFS_ADMIN_ACCESS_KEY_ID:-AKIAIOSFODNN7EXAMPLE}" \
    --secret-access-key "${LAKEFS_ADMIN_SECRET_ACCESS_KEY:-wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY}" \
    --local-settings
  touch /home/lakefs/.lakefs_setup_complete
fi

export LAKECTL_SERVER_ENDPOINT_URL=http://lakefs:8000
export LAKECTL_CREDENTIALS_ACCESS_KEY_ID="${LAKEFS_ADMIN_ACCESS_KEY_ID:-AKIAIOSFODNN7EXAMPLE}"
export LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY="${LAKEFS_ADMIN_SECRET_ACCESS_KEY:-wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY}"

if ! lakectl repo list | grep -q "bike-rentals"; then
  lakectl repo create lakefs://bike-rentals --storage-namespace local://data
fi

for f in /data/*.csv; do
  filename=$(basename "$f")
  lakectl fs upload "lakefs://bike-rentals/main/data/$filename" --source "$f" --overwrite
  echo "Uploaded $filename"
done

echo "LakeFS setup completed."