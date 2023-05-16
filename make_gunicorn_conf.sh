#!/bin/bash

grab_ip() {
    IPS=$(ip a | grep -o 'inet.*' | cut -d ' ' -f 2 | cut -d '/' -f 1)
    PS3='select ip to use: '
    select IP in $IPS
    do
        echo $IP
        break
    done
}

echo "command = '$(pwd)/env/bin/gunicorn'
pythonpath = '$(pwd)/yarl'
bind = '$(grab_ip):8000'
workers = 3
" > gunicorn_conf.py

echo run the script as
echo gunicorn -c gunicorn_conf.py yarl.wsgi
