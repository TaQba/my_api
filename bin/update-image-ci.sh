#!/usr/bin/env bash
rm -rf logs/*
cp configs/test.cfg core/app.cfg
printf "\e[0;33m Building docker image... \033[0m\n"
docker build -f Dockerfile-ci-live -t git.as29550.net:4567/simplyhosting/simply-auditor/ci .

printf "\033[0;32m Docker image built successfully! \033[0m\n"

printf "\033[0;33m Pushing docker image... \033[0m\n"
docker push git.as29550.net:4567/simplyhosting/simply-auditor/ci
printf "\033[0;32m Docker image pushed successfully! \033[0m"
