.PHONY: setup-postgres setup-python etl-setup test sftp-setup sftp-teardown sftp-update clean create-directories

# Directory paths from config
DATA_DIR = ./sftp-server/data
RAW_DIR = ./data/raw
TEMP_DIR = ./data/processed/temp
LOG_DIR = ./logs
ARCHIVE_DIR = ./data/processed/archive

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

test: sftp-setup
	@echo "Running tests..."
	pytest tests/
	@make sftp-teardown

sftp-setup:
	@echo "Setting up the mock SFTP server..."
	mkdir -p /home/vinkOS/archivosVisitas/
	sudo chmod 777 /home/vinkOS/archivosVisitas/
	cp config/pg-server.config /home/vinkOS/archivosVisitas/config.json
	python3 sftp-server/sftp-mock.py & echo $$! > sftp.pid

sftp-teardown:
	@echo "Tearing down the mock SFTP server..."
	# Add commands to stop the mock SFTP server
	kill $$(cat sftp.pid) && rm sftp.pid

sftp-update:
	@echo "Updating the mock SFTP server..."
	# Placeholder for update logic

clean:
	@echo "Cleaning up..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	# Add any other cleanup actions as needed