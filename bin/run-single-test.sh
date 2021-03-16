#!/usr/bin/env bash
export TESTING="1"
python -m pytest tests/unit/controllers/test_pings.py -s
