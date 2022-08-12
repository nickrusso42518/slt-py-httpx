# Author: Nick Russo
# Purpose: Provide simple "make" targets for developers
# See README for details about each target.

# Default goal runs the "all" target
.DEFAULT_GOAL := all

.PHONY: all
all: clean lint run

.PHONY: setup
setup:
	@echo "Starting  setup"
	pip install -r requirements.txt
	mkdir -p resp
	@echo "Completed setup"

.PHONY: lint
lint:
	@echo "Starting  lint"
	find . -name "*.py" | xargs pylint
	find . -name "*.py" | xargs black -l 82 --check
	@echo "Completed lint"

.PHONY: run
run:
	@echo "Starting  run"
	python basic_get.py
	python basic_log.py
	python print_response.py
	python session_test.py
	python cache_control.py
	python redirect_automatic.py
	python redirect_manual.py
	python get_cisco_sdwan_devices.py
	python get_some_pokemon.py
	python get_all_pokemon.py
	@echo "Completed run"

.PHONY: clean
clean:
	@echo "Starting  clean"
	find . -name "*.pyc" | xargs rm
	rm -f resp/*
	@echo "Starting  clean"
