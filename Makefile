SHELL = /bin/bash
WORKDIR = /vagrant

flask/server:
		python app.py

db/setup: db/create db/seed

db/create:
		@echo "--> setup database if not exists"
		test -f data/tasks.db || mkdir -p data && python manage.py db init && \
python manage.py db migrate && python manage.py db upgrade

db/seed:
		@echo "--> seeding the database"
		python manage.py seed

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

