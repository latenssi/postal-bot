#!/bin/bash

# Prepare log files and start outputting logs to stdout
touch $POSTAL_BOT_SRVHOME/logs/gunicorn.log
touch $POSTAL_BOT_SRVHOME/logs/access.log
tail -n 0 -f $POSTAL_BOT_SRVHOME/logs/*.log &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn wsgi:application \
    --name postal_bot \
    --bind 0.0.0.0:8000 \
    --workers 1 \
    --log-level=info \
    --log-file=$POSTAL_BOT_SRVHOME/logs/gunicorn.log \
    --access-logfile=$POSTAL_BOT_SRVHOME/logs/access.log \
    "$@"
