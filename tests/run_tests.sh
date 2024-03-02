#!/bin/bash

cd tests/bin/test_server && uvicorn server:app --port 44777 & > /dev/null
pwd
pytest tests/
