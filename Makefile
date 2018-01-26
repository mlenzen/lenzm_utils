venv = ./.venv/bin/

help:
	@echo "  clean       remove unwanted files like .pyc's"
	@echo "  lint        check style with flake8"
	@echo "  tests       run tests (using py.test)"
	@echo "  testall     run tests for all Python versions (using tox)"
	@echo "  coverage    run coverage report"
	@echo "  publish     publish to PyPI"
	@echo "  docs        create HMTL docs (using Sphinx)"

.PHONY: tests
tests:
	$(venv)py.test

.PHONY: testall
testall:
	$(venv)tox

.PHONY: clean
clean:
	rm -rf build
	rm -rf dist
	rm -rf lenzm_utils.egg-info
	find . -name *.pyc -delete
	find . -name *.pyo -delete
	find . -name *~ -delete
	find . -name __pycache__ -delete

.PHONY: lint
lint:
	$(venv)flake8 --statistics --count

.PHONY: coverage
coverage:
	$(venv)coverage run --source lenzm_utils setup.py test
	$(venv)coverage report -m
	$(venv)coverage html
	# open htmlcov/index.html

.PHONY: publish
publish: lint testall
	git push
	git push --tags
	$(venv)python setup.py sdist upload
	$(venv)python setup.py bdist_wheel upload

.PHONY: docs
docs:
	rm -f docs/lenzm_utils.rst
	rm -f docs/modules.rst
	$(venv)sphinx-apidoc -o docs/ lenzm_utils
	make -C docs clean
	make -C docs html
	open docs/_build/html/index.html
