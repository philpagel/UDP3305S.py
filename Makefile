help:
	@echo "The following make targets are available:\n"
	@echo "   test         run automated test suite. Requires device to be connected."
	@echo "   build        build python package"
	@echo "   clean        clean up package and cruft"
.PHONEY: help

test:
	pytest -v src/tests/UPD3305S_test.py
.PHONEY: test


build: 
	python3 -m build
.PHONEY: build

clean:
	rm -rf dist
	rm -rf src/UPD3305S.egg-info
	rm -rf src/UDP3305S/__pycache__
	rm -rf src/tests/__pycache__
.PHONEY: clean
