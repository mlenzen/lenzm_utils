venv = ./.venv/bin/

help:
	@echo "  clean       remove unwanted files like .pyc's"
	@echo "  lint        check style with flake8"
	@echo "  tests       run tests (using py.test)"
	@echo "  testall     run tests for all Python versions (using tox)"
	@echo "  coverage    run coverage report"
	@echo "  publish     publish to PyPI"

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

.PHONY: mypy
mypy:
	$(venv)mypy --ignore-missing-imports lenzm_utils

.PHONY: coverage
coverage:
	$(venv)coverage run --source lenzm_utils setup.py test
	$(venv)coverage report -m
	$(venv)coverage html
	# open htmlcov/index.html

.PHONY: publish-force
publish-force:
	git push
	git push --tags
	$(venv)python setup.py sdist upload
	$(venv)python setup.py bdist_wheel upload


.PHONY: publish
publish: checks publish-force

.PHONY: checks
checks: lint testall
#checks: lint testall mypy
