#!/bin/bash

RUN_PORT=${PORT:-5000}

source .venv/bin/activate
uvicorn src.main:app --port ${RUN_PORT} --reload