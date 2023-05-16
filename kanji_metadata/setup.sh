#!/bin/sh
# DISCLAIMER this was run on Debian 10
# run this script from its' folder please
python3 -m venv env
source env/bin/activate

# psycopg2 requirements
sudo apt install postgresql libpq-dev

pip3 install -r requirements.txt
