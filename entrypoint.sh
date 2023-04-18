#!/bin/bash

RUN_PORT=${PORT:-8000}

gunicorn -k uvicorn.workers.UvicornWorker src.main:app -b '0.0.0.0':${RUN_PORT}