#!/bin/sh

echo "
[Unit]
Description=Gunicorn serving django app
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$(pwd)/yarl
Environment="PATH=$(pwd)/env/bin"
ExecStart=$(pwd)/env/bin/gunicorn -c $(pwd)/gunicorn_conf.py yarl.wsgi

[Install]
WantedBy=multi-user.target
" > yarl.service

sudo unlink /etc/systemd/system/yarl.service 
sudo ln -s "$(pwd)/yarl.service" /etc/systemd/system/yarl.service 
sudo systemctl daemon-reload
sudo systemctl start yarl.service
sudo systemctl enable yarl.service
