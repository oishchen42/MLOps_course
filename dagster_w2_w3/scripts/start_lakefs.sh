#!/bin/sh
set -e

# Only run setup if the database is empty
if [ ! -f /home/lakefs/data/.setup_done ]; then
  echo "Running initial LakeFS setup..."
  lakefs setup \
    --user-name admin \
    --access-key-id "$LAKECTL_CREDENTIALS_ACCESS_KEY_ID" \
    --secret-access-key "$LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY"
  
  touch /home/lakefs/data/.setup_done
  echo "LakeFS setup completed."
fi

# Hand over control to start the actual web server
exec lakefs run