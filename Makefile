.PHONY: create-env install format lint test clean remove-env

CONDA_ENV_NAME := llvim
PYTHON_VERSION := 3.10

create-env:
	conda create --name $(CONDA_ENV_NAME) python=$(PYTHON_VERSION) -y
	conda run -n $(CONDA_ENV_NAME) pip install -r requirements.txt
	@echo "Conda environment '$(CONDA_ENV_NAME)' created and activated. Python version:"
	@conda run -n $(CONDA_ENV_NAME) python --version
	@echo "To activate this environment, use:"
	@echo "conda activate $(CONDA_ENV_NAME)"
	@echo "Please still run 'make install' to ensure installation of the required packages."

install:
	pip install -r requirements.txt
	python -m spacy download en_core_web_sm

format:
	black .
	isort .

lint:
	flake8 .
	pyright

test:
	pytest

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

remove-env:
	conda env remove --name $(CONDA_ENV_NAME) -y

all: create-env format lint test
