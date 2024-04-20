#!/bin/bash

cd tests/bin && uvicorn test_server.server:app --port 44777 & > /dev/null
pwd
cd ../../
pwd
pytest tests/
