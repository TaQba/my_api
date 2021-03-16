#!/usr/bin/env bash
printf "\e[0;33m Init for My API Application ... \033[0m\n"

printf "\e[0;33m Create config file: core/app.cfg ... \033[0m"
rm core/app.cfg
cp configs/dev.cfg core/app.cfg
printf "\033[0;32m done! \033[0m\n"

printf "\e[0;33m Setup db for DEV environment... \033[0m"
./bin/setup_db.sh
printf "\033[0;32m done! \033[0m\n"

