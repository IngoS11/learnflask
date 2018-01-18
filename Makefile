SHELL = /bin/bash
WORKDIR = /vagrant
FLASK_DEBUG = 1
FLASK_APP = apiserver.py

flask/server:
		flask run

db/setup: db/create db/seed

db/create:
		@echo "--> setup database if not exists"
		test -f data/tasks.db || mkdir -p data && flask db init && \
flask db migrate && flask db upgrade

pip/freeze:
		@echo "--> updating python dependencies to requirements.txt"
		pip freeze > requirements.txt

pip/update:
		@echo "--> updating python dependencies from requirements.txt"
		pip install -r requirements.txt

env/setup: env/setup_virtualenv env/setup_shell

env/setup_shell:
		@echo "--> configuring python environment"
		(test -f ~/.zshrc && grep env/bin/activate ~/.zshrc) || \
		    echo "cd $(WORKDIR) && source env/bin/activate" >> ~/.zshrc

env/setup_virtualenv:
		@echo "--> creating python virtual environment"
		test -d env || virtualenv env

