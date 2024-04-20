# !/bin/bash

cd tests/bin/test_server
uvicorn test_server.server:app --port 44777 --reload
cd ../../../
