#!/bin/sh
set -e

# Only initialize the database the first time - check for a marker file
if [ ! -f /home/lakefs/.setup_done ]; then
  echo "Running initial LakeFS setup..."
  lakefs setup \
    --user-name admin \
    --access-key-id "${LAKEFS_ADMIN_ACCESS_KEY_ID:-AKIAIOSFODNN7EXAMPLE}" \
    --secret-access-key "${LAKEFS_ADMIN_SECRET_ACCESS_KEY:-wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY}" \
    --local-settings
  touch /home/lakefs/.setup_done
  echo "LakeFS setup completed."
fi

# Now start the actual lakeFS server
exec lakefs run --local-settings