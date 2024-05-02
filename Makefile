.PHONY: setup-postgres setup-python etl-setup test sftp-setup sftp-teardown sftp-update clean create-directories

# Directory paths from config
DATA_DIR = ./sftp-server/data
RAW_DIR = ./data/raw
TEMP_DIR = ./data/processed/temp
LOG_DIR = ./logs
ARCHIVE_DIR = ./data/processed/archive
BASE_DIR := $(shell pwd)

create-directories:
	@echo "Creating necessary directories..."
	mkdir -p $(DATA_DIR) $(RAW_DIR) $(TEMP_DIR) $(LOG_DIR) $(ARCHIVE_DIR)

setup-postgres:
	@echo "Setting up PostgreSQL..."
	sudo apt update
	sudo apt -y install postgresql postgresql-contrib
	sudo service postgresql start

setup-python:
	@echo "Installing Python requirements..."
	pip install -r requirements.txt

etl-setup: create-directories setup-postgres setup-python
	@echo "Setting up ETL environment..."
	# Add any ETL specific setup here
	# Setup crontab for etl.sh, uncomment if needed
	# (crontab -l 2>/dev/null; echo "2 0 * * * bash etl/etl.sh &") | crontab -

sftp-setup:
	@echo "Setting up the mock SFTP server..."
	mkdir -p ./vinkOS/archivosVisitas/
	sudo chmod 777 ./vinkOS/archivosVisitas/
	cp config/pg-server.config ./vinkOS/archivosVisitas/config.json
	python3 sftp-server/sftp-mock.py & echo $$! > sftp.pid


etl-run:
	@echo "Running ETL process..."
	@echo "Extracting data from SFTP server..."
	@export BASE_DIR=$(BASE_DIR); \
	PYTHONPATH=$(BASE_DIR) python $(BASE_DIR)/etl/extract.py
	@echo "Transformed data..."
	@export BASE_DIR=$(BASE_DIR); \
	PYTHONPATH=$(BASE_DIR) python $(BASE_DIR)/etl/transform.py
	@echo "Loading data..."
	@export BASE_DIR=$(BASE_DIR); \
	PYTHONPATH=$(BASE_DIR) python $(BASE_DIR)/etl/load.py


etl: etl-setup sftp-setup etl-run
	@echo "Running ETL process..."

test: sftp-setup
	@echo "Running tests..."
	pytest tests/
	@make sftp-teardown

sftp-teardown:
	@echo "Tearing down the mock SFTP server..."
	# Add commands to stop the mock SFTP server
	kill $$(cat sftp.pid) && rm sftp.pid

sftp-update:
	@echo "Updating the mock SFTP server..."
	# Placeholder for update logic

clean: sftp-teardow
	@echo "Cleaning up..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	# Add any other cleanup actions as needed