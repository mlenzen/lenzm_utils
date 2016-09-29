.PHONY: docs test

help:
	@echo "  clean       remove unwanted files like .pyc's"
	@echo "  lint        check style with flake8"
	@echo "  tests       run tests (using py.test)"
	@echo "  testall     run tests for all Python versions (using tox)"
	@echo "  coverage    run coverage report"
	@echo "  publish     publish to PyPI"
	@echo "  docs        create HMTL docs (using Sphinx)"

tests:
	python setup.py test

testall:
	tox

clean:
	rm -rf build
	rm -rf dist
	rm -rf lenzm_utils.egg-info
	find . -name *.pyc -delete
	find . -name *.pyo -delete
	find . -name *~ -delete
	find . -name __pycache__ -delete

lint:
	flake8 lenzm_utils

coverage:
	coverage run --source lenzm_utils setup.py test
	coverage report -m
	coverage html
	# open htmlcov/index.html

publish:
	python setup.py sdist upload
	python setup.py bdist_wheel upload

docs:
	rm -f docs/lenzm_utils.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ lenzm_utils
	make -C docs clean
	make -C docs html
	open docs/_build/html/index.html
