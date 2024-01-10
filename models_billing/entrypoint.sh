#!/bin/sh
# entrypoint.sh

# Run migrations


python -m models_billing.core.populate_db

#TODO: add create django superuser command

# Then run the main container command (passed to us as arguments)
exec "$@"