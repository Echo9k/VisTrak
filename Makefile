.PHONY: setup test clean sftp-setup sftp-teardown


setup-postgres:
	sudo apt update
	sudo apt -y install postgresql postgresql-contrib
	sudo service postgresql start


setup-python:
    @echo "Installing requirements..."
    pip install -r requirements.txt

test: sftp-setup
    @echo "Running tests..."
    pytest tests/
    @make sftp-teardown

sftp-setup:
    @echo "Setting up the mock SFTP server..."
	mkdir -p /home/vinkOS/archivosVisitas/
    sudo chmod 777 /home/vinkOS/archivosVisitas/
	cp config/pg-server.config /home/vinkOS/archivosVisitas/config.json
	python3 src/sftp_server.py & echo $$! > sftp.pid


sftp-teardown:
    @echo "Tearing down the mock SFTP server..."

sftp-update:
	@echo "Updating the mock SFTP server..."
	# ask for username
	@echo "Enter username: "
	@read username
	# Constructing full command
	export command=@8.8.8.8:/home/vinkOS/archivosVisitas
	sftp $username$command


clean:
    @echo "Cleaning up..."
    find . -type f -name '*.pyc' -delete
    find . -type d -name '__pycache__' -delete