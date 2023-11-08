Here is a proposal for an ETL process to meet the requirements outlined:

# ETL Process proposal

## 1. Extract data from files

- Use SFTP to connect to remote server (8.8.8.8) and download all files from /home/vinkOS/archivosVisitas that match pattern report_*.txt
- Store downloaded files locally in /tmp/visitas

## 2. Transform data

For each downloaded file:

- Validate file layout
- Validate email and date fields
- Parse data into two objects per row - one for visitor table, one for statistics table
- Enrich data:
  - Calculate total visits, current year visits, current month visits for visitor object
  - Parse date strings into Date objects
  - etc.
- Load visitor and statistics objects into corresonding MySQL tables
- Log any rows that fail validation or load into errors table

## 3. Load data

- Use insert/update logic on visitor table to only have one row per email
- New emails are inserted
- Existing emails are updated with new visit data
- Truncate statistics and errors tables on each run

## 4. Handle errors

- Log any validation or load errors to errors table
- Send email notification for any errors after ETL run
- Retry any failed loads (e.g. due to DB outage)

## 5. Post-processing

- Delete downloaded files from /tmp/visitas
- Zip processed files into dated archive in /home/etl/visitas/bckp
- Schedule ETL job to run daily

Let me know if you would like me to expand on any part of the process! The key points are validating the data, transforming it for the DB models, safely updating the visitor table, and properly handling any errors.

# Plan
Creating an ETL process in a development container with Anaconda and PostgreSQL involves several steps. To simulate the environment closely, you can use a mock SFTP server for testing purposes. Below is a detailed plan structured into phases for implementation:

### Phase 1: Environment Setup
- **Prepare the Development Container:**
  - Ensure your devcontainer is configured with the necessary tools, including Anaconda for Python package management and PostgreSQL for database management.
  - If not already set up, install the `paramiko` library for SFTP operations and `psycopg2` or `sqlalchemy` for PostgreSQL database interactions in your Anaconda environment.
  - Configure PostgreSQL with the required databases and tables (`visitor`, `statistics`, `errors`).

- **Mock SFTP Server Setup:**
  - Install a mock SFTP server within the devcontainer. You can use a lightweight SFTP server package like `pyfakefs` or `pytest-sftpserver` for Python.
  - Configure the mock SFTP server with the required directory structure and permissions.
  - Populate the mock SFTP server with sample data files that match the expected pattern (report_*.txt) for testing.

### Phase 2: ETL Script Development
- **Extract:**
  - Develop a Python script to connect to the SFTP server (mock for testing) and download files.
  - Implement file pattern matching and ensure that only the correct files are downloaded.

- **Transform:**
  - Create functions to validate file layout, email, and date fields.
  - Develop parsing logic to split data into the appropriate `visitor` and `statistics` objects.
  - Implement enrichment logic such as calculating total visits and parsing date strings.

- **Load:**
  - Develop database interaction functions to handle insert/update logic on the `visitor` table and to insert data into the `statistics` table.
  - Ensure idempotence by truncating the `statistics` and `errors` tables before each run.

### Phase 3: Error Handling and Logging
- **Implement Robust Error Handling:**
  - Add try-except blocks around critical sections of code.
  - Write exceptions to the `errors` table and include timestamp and error details.

- **Logging and Notifications:**
  - Implement a logging mechanism to record the ETL process steps and outcomes.
  - Set up an email notification system to alert you of any errors after an ETL run.

### Phase 4: Post-Processing and Cleanup
- **File Management:**
  - After processing, delete files from the working directory.
  - Archive processed files by zipping them and moving them to a backup directory with a dated filename.

### Phase 5: Testing and Validation
- **Unit Testing:**
  - Write unit tests for each component of the ETL process (extract, transform, load).
  - Use the mock SFTP server to validate the extract process.

- **Integration Testing:**
  - Conduct integration testing by running the full ETL process in the devcontainer environment.
  - Verify that the data is correctly processed and loaded into PostgreSQL.

### Phase 6: Scheduling and Automation
- **ETL Job Scheduling:**
  - Use a scheduling tool like `cron` within the devcontainer to run the ETL process at the desired frequency.
  - Ensure that the environment variables and paths are correctly set in the cron job script.

- **Automation Readiness:**
  - Document the process to transition from the mock SFTP server to a production SFTP server.
  - Make sure all configurations can be easily switched from development to production settings.

### Phase 7: Documentation and Knowledge Transfer
- **Create Documentation:**
  - Document the entire setup and ETL process, including environment configuration, dependencies, and the steps each script takes.
  - Include instructions for troubleshooting common issues and errors.

- **Knowledge Transfer:**
  - Prepare to transfer knowledge to other team members by organizing walkthrough sessions or creating detailed guides.

By following this plan, we can ensure that each aspect of the ETL process is carefully addressed, from initial setup and development to testing, automation, and documentation. This structured approach also facilitates easier transition from a development to a production environment when ready.