#!/bin/bash -e

export owner=606319127842.dkr.ecr.ap-southeast-2.amazonaws.com

echo "Create local python environment"
python3 -m venv venv || python -m venv venv
source venv/bin/activate
pip install pytest pyyaml jinja2 requests

cd ..
bash build.sh
cd -

# echo "============================================="
# echo "== Test with pre-configured hub and agents =="
# echo "============================================="

cd ../docker-compose
docker compose -f docker-compose-preconf.yaml up -d
cd -

cd ..
pip install .
echo "Wait for HammerDB to finish and database becoming available"
while ! docker exec pyhvrhub nc postgres-source 5432 ; do sleep 5; done;
while ! docker exec pyhvragent-1 nc localhost 4343 ; do sleep 1; done;
while ! docker exec pyhvragent-2 nc localhost 4343 ; do sleep 1; done;
pytest --ignore tests/test_clean_install.py
cd -

cd ../docker-compose
docker compose -f docker-compose-preconf.yaml down -v
cd -

echo "==============================================="
echo "== Test with clean install of hub and agents =="
echo "==============================================="

cd ../docker-compose
docker compose -f docker-compose-clean-inst.yaml up --build -d
cd -

echo "Wait for hubserver to come up"
while ! docker exec pyhvrhub nc localhost 4340 ; do sleep 1; done;
while ! docker exec pyhvragent-1 nc localhost 4343 ; do sleep 1; done;
while ! docker exec pyhvragent-2 nc localhost 4343 ; do sleep 1; done;
docker cp pyhvrhub:/install/hvr.lic ../tests/hvr.lic
cd ..
pytest tests/test_clean_install.py
cd -

cd ../docker-compose
docker compose -f docker-compose-clean-inst.yaml down -v
cd -

echo "Cleanup temp python environment"
deactivate
rm -rf venv

echo "Flake8"
cd ..
flake8 --config .flake8