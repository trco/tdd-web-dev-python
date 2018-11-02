Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3
* virtualenv + pip
* Git

e.g., on Ubuntu:

  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt update
  sudo apt-get install nginx git python3.6 python3.6-venv

## Nginx Virtual Host config

* see nginx.template.conf
* replace DOMAIN with, e.g., staging.my-domain.com

## Systemd service

* see gunicorn-systemd.template.conf
* replace DOMAIN with, e.g. staging.my-domain.com

## Folder structure:

Assume we have a user account at /home/username

/home/username
└── sites
    ├── DOMAIN1
    |    ├── .env
    |    ├── db.sqlite3
    |    ├── manage.py etc
    |    ├── static
    |    └── venv
    └── DOMAIN2
        ├── .env
        ├── db.sqlite3
        ├── manage.py etc
        ├── static
        └── venv
