# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


# Khef Dev Environment
# ====================
#
# "Public" entrypoints can be listed by running `make` or `make help` from
# within this directory.


# This macro is shorthand for "Run the following command in the context of the
# python virtual environment located in the `.venv` directory"
venv=. .venv/bin/activate &&


# Public Targets
# --------------

all: help

installcheck: #: Validate an installation of khef
	which khef
	man -w khef

clean: #: Remove any development / testing rubble
	rm -rf \
		.coverage \
		.mypy_cache \
		.pytest_cache \
		__pycache__ \
		tests/__pycache__ \
		htmlcov \
		build \
		*.txt \
		.venv

coverage: .venv/bin/coverage #: Visualize uncovered code
	$(venv) coverage html
	open htmlcov/index.html

help: #: Print this help menu
	@echo "USAGE\n"
	@awk -F': ' '/#:/ && !/awk/ { print $$1,":",$$3 }' $(MAKEFILE_LIST) \
		| column -s ':' -t

install: /usr/local/share/man/man1/khef.1 /usr/local/bin/khef #: Install khef on this host

lint: .venv/bin/flake8 #: Check code for PEP8 compliance (even if nothing has changed)
	$(venv) flake8 khef.py

check: .venv/bin/pytest .venv/bin/coverage  #: Run tests (+ lint + typecheck)
	$(venv) pytest tests/exterior --cov=tests.khef --cov-fail-under=100

test: build/lint build/typecheck .venv/bin/pytest .venv/bin/coverage  #: Run tests (+ lint + typecheck)
	$(venv) pytest tests/interior tests/perimeter --cov=tests.khef

typecheck: .venv/bin/mypy #: Check for static type errors (even if nothing has changed)
	$(venv) mypy khef.py

uninstall: #: Remove khef from this host
	sudo rm -f \
		/usr/local/share/man/man1/khef.1 \
		/usr/local/bin/khef


# Local Build Targets
# -------------------

# Use this to avoid re-typechecking khef every time we test. The typechecking
# will only be performed again if khef has changed since the last successful
# typecheck.
build/typecheck: build/.dir khef.py
	$(MAKE) typecheck
	touch $@

# Use this to avoid re-linting khef.py every time we want to test. Instead, khef
# will only be re-linted if it has changed since the last successful linting.
build/lint: build/.dir khef.py
	$(MAKE) lint
	touch $@

# Create an empty "build/" directory, but use an empty file as a flag so that we
# do not attempt to recreate it in the future -- directories are not good
# targets for Make because they appear to be "modified" whenever a file inside
# them is modified, so we want to rely on an empty file as a proxy for the
# existence of this directory.
build/.dir:
	mkdir -p build
	touch $@


# Global Install Targets
# ----------------------
/usr/local/share/man/man1/khef.1: khef.1
	sudo install -o root -g wheel -m 0644 $< $@

/usr/local/bin/khef: khef.py
	sudo install -o root -g wheel -m 0755 $< $@


# Virtual Environment Targets
# ---------------------------

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
