#!/bin/bash

root_dir=$1

docker compose -f ${root_dir}/test/docker-compose.yml up -d --force-recreate

python -m pytest ${root_dir}/test/

docker compose -f ${root_dir}/test/docker-compose.yml down 