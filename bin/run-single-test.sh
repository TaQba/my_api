#!/usr/bin/env bash
export TESTING="1"
#python -m pytest tests/unit/components/test_parser_raid_state.py -s
#python -m pytest tests/unit/components/test_disk.py -s
#python -m pytest tests/unit/components/test_raid.py -s
#python -m pytest tests/unit/components/test_ram.py -s
#python -m pytest tests/unit/components/test_chassis.py -s
#python -m pytest tests/unit/components/test_part_specification.py -s
python -m pytest tests/unit/controllers/test_server.py -s
#python -m pytest tests/unit/models/test_specification_custom.py -s

