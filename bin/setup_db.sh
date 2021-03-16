#!/usr/bin/env bash
printf "\e[0;33m Configure My API Dev Application DB ... \033[0m\n"

printf "\e[0;33m Update db ... \033[0m"
export FLASK_APP=app.py
flask db upgrade
printf "\033[0;32m done! \033[0m\n"


