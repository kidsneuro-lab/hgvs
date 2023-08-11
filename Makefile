#! /usr/bin/make

PACKAGE_NAME=pyhgvs
SCRIPTS=bin/hgvs
TEST_OUTPUT?=nosetests.xml

VENV_DIR?=.venv
VENV_ACTIVATE=$(VENV_DIR)/bin/activate
WITH_VENV=. $(VENV_ACTIVATE);

default:
	python setup.py check build

.PHONY: setup clean lint test gitlint

clean:
	python setup.py clean
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg*/
	rm -rf __pycache__/
	rm -f MANIFEST
	rm -f $(TEST_OUTPUT)
	find $(PACKAGE_NAME) -type f -name '*.pyc' -delete

lint:
	flake8 --jobs=auto $(PACKAGE_NAME)/ $(SCRIPTS)

test:
	nosetests --verbosity=2 --with-xunit --xunit-file=$(TEST_OUTPUT)

package:
	python setup.py sdist
