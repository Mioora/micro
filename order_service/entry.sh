#!/bin/bash

sleep 15
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8080