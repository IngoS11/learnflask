# A Flask API Project on a Vagrant Environment
A project to learn how to build an API server with Python and Flask. It also serves me to learn Vim and get used to writing code with it, write good code and tests, play around with GitHub, CircleCi and other CI/CD tools available as SaaS service on the internet.

## Getting Started
the is easiest set up with [Vagrant](http://www.vagrant.io) and [VirtualBox](https://www.virtualbox.org)


### Prerequisites
* Download and install [Virtual Box](https://www.virtualbox.org)
* Download and install [Vagrant](http://www.vagrant.io)
* Clone the Repository ```git clone https://github.com/IngoS11/learnflask```
* Check that some process on your local machine is not using port 5000, this is mapped into the Virtual Box by Vagrant
* On the command line create the Virtual Box via Vagrant using ```vagrant up```

### Usage
Once the Virtual Box is up and running you can use it as follows:
* Log on to the Virtual Box using ```vagrant ssh``` on the command line
* The project folder is located at ```/vagrant```
* Export the FLASK_APP and FLASK_DEBUG environment variables to be able to make use of the Flask CLI
```
export FLASK_APP=apiserver.py
export FLASK_DEBUG=1
```
then use Flasks CLI to:
* Initialize the database ```flask db init```
* Create the migration scripts ```flask db migrate```
* Create the database ```flask db upgrade```

once the database is created use:
* Start the apiserver binding to all network interfaces ```flask run --host 0.0.0.0```
* Use httpie to query the server ```http :5000/login```

### Built With
* Python
* Flask
* SQLite

### Tools I use
* Vim
* tmux
* httpie
* flake8

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgements
Thank you to anyone who provided code and snippets on the internet for me to learn and use.
