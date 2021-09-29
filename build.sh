#!/bin/bash
cd pyhvr-generate
python3 generate.py ../api/openapi.yaml
mv pyhvr*.py ../pyhvr/
cd -
black .
isort .
