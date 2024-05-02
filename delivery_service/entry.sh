#!/bin/bash

sleep 25
uvicorn app.main:app --host 0.0.0.0 --port 80