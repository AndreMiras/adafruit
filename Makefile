VENV ?= venv
DEPLOY_PATH=/media/*/CIRCUITPY
PIP=$(VENV)/bin/pip
FLAKE=$(VENV)/bin/flake8
ISORT=$(VENV)/bin/isort


deploy:
	cp *.py $(DEPLOY_PATH)/

$(VENV):
	virtualenv --python=python3.7 $(VENV)
	$(PIP) install -r requirements.txt

virtualenv: $(VENV)

test: virtualenv
	$(FLAKE) *.py
	$(ISORT) -rc -c --diff *.py

shell:
	screen /dev/ttyACM0 115200
