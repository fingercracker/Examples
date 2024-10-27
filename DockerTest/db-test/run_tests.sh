#!/bin/bash

root_dir=${1:-./}/DockerTest/db-test

docker compose -f ${root_dir}/docker-compose.yml up -d --force-recreate

sleep 2

python -m pytest ${root_dir}

docker compose -f ${root_dir}/docker-compose.yml down 