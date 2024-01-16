# Update version ONLY here
VERSION := 0.1
SHELL := /bin/bash
# Makefile for project
VENV := venv

# Detect the operating system
ifeq ($(OS),Windows_NT)
    detected_OS := Windows
    PYTHON := python
    VENV_BIN := $(VENV)/Scripts
else
    detected_OS := $(shell uname)
    PYTHON := python3
    VENV_BIN := $(VENV)/bin
endif

# Create a virtual environment
venv: $(VENV_BIN)/activate

# Virtual environment creation
$(VENV_BIN)/activate:
	$(PYTHON) -m venv $(VENV)


.PHONY: all clean pdf
clean:
	rm -rf _build/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf coverage.xml

install: venv
	$(VENV_BIN)/pip install -e .[test]

db-create-tables: venv
	$(VENV_BIN)/python db.py

run: venv db-create-tables
	$(VENV_BIN)/uvicorn api:app --reload

test: venv
	$(VENV_BIN)/python -m unittest test_api

pytest: venv
	$(VENV_BIN)/python -m pytest

# Format code using Black
black:
	$(VENV_BIN)/black .

# Sort imports using isort
isort:
	$(VENV_BIN)/isort . --overwrite-in-place

doc8:
	$(VENV_BIN)/doc8

# Run ruff on the codebase
ruff:
	$(VENV_BIN)/ruff .
