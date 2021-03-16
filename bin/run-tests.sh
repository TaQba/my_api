#!/usr/bin/env bash

export TESTING="1"
pytest tests/ --cov-report term --cov-report html --cov-config .coveragerc --cov=.