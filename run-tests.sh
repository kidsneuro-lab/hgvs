
#!/bin/bash
set -e

echo "##########################################"
echo "Building unit tests"
echo "##########################################"
docker compose -f docker-compose-unit-tests.yml build

echo "##########################################"
echo "Running unit tests"
echo "##########################################"
docker compose -f docker-compose-unit-tests.yml up \
  --force-recreate \
  --remove-orphans \
  --no-log-prefix \
  --abort-on-container-exit \
  --exit-code-from tests

echo "##########################################"
echo "Building API tests"
echo "##########################################"
docker compose -f docker-compose-api-tests.yml build

echo "##########################################"
echo "Running API tests"
echo "##########################################"
docker compose -f docker-compose-api-tests.yml up \
  --detach \
  --force-recreate \
  --remove-orphans \
  --no-log-prefix \
  --exit-code-from hgvs

# Wait for 5 seconds
sleep 5s

echo "##########################################"
echo "Calling API"
echo "##########################################"
curl --fail -X "POST" "http://127.0.0.1:8002/translate" \
     -H 'Content-Type: application/json; charset=utf-8' \
     -d $'{
  "indels_start_with_same_base": false,
  "ignore_version": true,
  "input": "NM_173495.3:c.1835_1839delinsGAA",
  "normalise": true
}'
