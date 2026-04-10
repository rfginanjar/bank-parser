#!/bin/bash
# Start Celery worker with Redis broker
celery -A tasks worker --loglevel=info --detach
# Start Celery beat for scheduled tasks
celery -A tasks beat --loglevel=info --detach
