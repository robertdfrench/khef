# khef development kit
# ====================
#
# "Public" entrypoints can be listed by running `make` or `make help` from
# within this directory.

# This macro is shorthand for "Run the following command in the context of the
# python virtual environment located in the `.venv` directory"
venv=. .venv/bin/activate &&


# Public Targets
# ==============

help: #: Print this help menu
	@awk -F': ' '/#:/ && !/awk/ { print $$1,":",$$3 }' $(MAKEFILE_LIST) \
		| column -s ':' -t

coverage: .venv/bin/coverage #: Visualize uncovered code
	$(venv) coverage html
	open htmlcov/index.html

test: lint typecheck .venv/bin/pytest .venv/bin/coverage  #: Run tests
	$(venv) pytest --cov=tests.khef --cov-fail-under=100

lint: .venv/bin/flake8 #: Check code for PEP8 compliance
	$(venv) flake8 khef

typecheck: .venv/bin/mypy #: Check for static type errors
	$(venv) mypy khef

clean: #: Remove any development / testing rubble
	rm -rf \
		.coverage \
		.mypy_cache \
		.pytest_cache \
		__pycache__ \
		tests/__pycache__ \
		htmlcov \
		build \
		.venv

# Install the latest version of 'pytest', which we use in place of the built-in
# test runner.
.venv/bin/pytest: .venv/init
	$(venv) pip install pytest

# Install the latest version of 'pytest-cov', which we use as a rough proxy for
# assessing the value of our unit tests. The khef tool is mostly designed around
# Dependency Injection, as that provides a vehicle for exercising a large
# fraction of the code using only cheap unit tests.
.venv/bin/coverage: .venv/init
	$(venv) pip install pytest-cov

# Install the latest version of 'flake8', which we use as rough proxy for
# measuring the readability (and thus *auditability*) of khef. The flake8 tool
# assures foolishly consistent adherence to the style guide outlined in
# https://peps.python.org/pep-0008/.
.venv/bin/flake8: .venv/init
	$(venv) pip install flake8

# Install a specific version of 'mypy', which we will use for static analysis of
# the type annotations within khef. See https://peps.python.org/pep-0484/ for
# more information on Python's "type hints".
#
# The latest version of mypy has stricter rules about how default types are
# handled, and our code does not meet those expectations yet.
#
# * https://mypy-lang.blogspot.com/2022/11/mypy-0990-released.html
# * https://github.com/robertdfrench/knoxbsd.org/issues/34
.venv/bin/mypy: .venv/init
	$(venv) pip install mypy==0.991

# Update the virtual environment to use the latest version of pip. The virtual
# environment is not really usable before this, as older pips can have security
# problems.
.venv/init: .venv/empty
	$(venv) pip install --upgrade pip
	@touch $@

# Creates a new, empty virtual environment if one does not already exist. No
# packages are available, and the default pip will be out of date.
.venv/empty:
	python3 -m venv .venv
	@touch $@
