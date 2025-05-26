VERSION="0.0.1"

help:
	@echo "The following make targets are available:\n"
	@echo "   dep          install dependencies (requirements)"
	@echo "   dep-dev      install dependencies for packaging"
	@echo "   test         run automated test suite. Requires device to be connected."
	@echo "   build        build python package"
	@echo "   install      install python package"
	@echo "   pypi         upload package to pypi"
	@echo "   clean        clean up package and cruft"
.PHONEY: help


dep:
	python -m pip install -r requirements.txt
.PHONEY: dep


test:
	@echo "Please follow these steps:\n"
	@echo "    1. Ensure that the settings in 'src/tests/testconfig.py'"
	@echo "       match your device connection/address"
	@echo "    2. Make sure nothing is connected to the device outputs"
	@echo "    3. Turn on the device\n"
	@echo "Hit ENTER to start the test suite"
	@read RESPONSE
	pytest -v src/tests/UDP3305S_test.py
.Phoney: test


dep-dev:
	python -m pip install -r requirements-dev.txt --upgrade
.PHONEY: dep-dev

build: 
	python -m build
.PHONEY: build


install: 
	python -m pip install dist/UDP3305S$(VERSION).tar.gz
.PHONEY: install


pypi:
	twine upload dist/*
.PHONEY: pypi


clean:
	rm -rf dist
	rm -rf src/UDP3305S.egg-info
	rm -rf src/UDP3305S/__pycache__
	rm -rf src/tests/__pycache__
.PHONEY: clean
