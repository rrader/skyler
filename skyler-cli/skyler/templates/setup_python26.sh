#!/usr/bin/env bash

cd /var/lib/skyler
chmod +x init.d/*.sh

virtualenv venv
source venv/bin/activate

mkdir app
mv app.tgz app/
cd app
tar xf app.tgz

pip install -r requirements.txt
