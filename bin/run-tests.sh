#!/usr/bin/env bash

export TESTING="1"

pytest tests/ --cov-report term --cov-report html --cov-config .coveragerc --cov=. --ignore-glob='tests/test_audit_data.py'