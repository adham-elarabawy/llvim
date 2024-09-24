.PHONY: create-env install format lint test clean remove-env

CONDA_ENV_NAME := myproject
PYTHON_VERSION := 3.9

create-env:
	conda create --name $(CONDA_ENV_NAME) python=$(PYTHON_VERSION) -y
	conda run -n $(CONDA_ENV_NAME) pip install -r requirements.txt
	@echo "Conda environment '$(CONDA_ENV_NAME)' created and activated. Python version:"
	@conda run -n $(CONDA_ENV_NAME) python --version
	@echo "To activate this environment, use:"
	@echo "conda activate $(CONDA_ENV_NAME)"

install:
	pip install -r requirements.txt

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