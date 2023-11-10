# ETL Process Execution

## Install the requirements

Use the Makefile to install all necessary stuff by running

```bash
make postgres-setup
make sftp-setup
make etl-setup
```

## Start the mock server
This server is passwordless at the moment, so it's only necessary to start it from the root directory using

```bash
python sftp-server/sftp-mock.py
```
> Logs: logs/sftp_mock.log


## ETL process execution

To run a test execution of this we can copy the data from `/sftp-mock/data-backup` to `/sftp-mock/data` using

```bash
make testing
```

To schedule the chron job use
```
2 0 * * * bash etl/etl.sh &
```

### Execution detaills

#### etl.sh

Will sequentially execute:

1. `/etl/extract.py`
2. `/etl/transform.py`
3. `/etl/load.py`


## Implementation
### Extract

- **SFTP Connection**: Establish a connection to the SFTP server (8.8.8.8) to access `/home/vinkOS/archivosVisitas` (For the simulation we actually use `/sftp-mock/data/`).
- **File Download**: Target files with the `report_*.txt` pattern. Downloaded files are temporarily stored in `/tmp/visitas`.

### Transform

- **File Processing**: For each file:
  - Validate layout, email, and date fields.
  - Split data into `visitor` and `statistics` objects.
  - Enrich data with calculated metrics and Date object conversion.

### Load

- **Database Interaction**:
  - Update `visitor` table using insert/update logic to handle unique email entries.
  - Populate `statistics` and `errors` tables.

### Error Handling

- **Logging and Alerts**:
  - [extract.py, transform.py] Capture their logs in `/logs/`
  - [load.py] Capture and log validation/load errors in the `errors` table.
  - To be implemented
    - Set up email notifications for post-ETL run issues.
    - Implement retry logic for failed loads, e.g., during DB outages.
    - Include log rotation and alerting mechanisms for critical failures such as Slack.

### Post-processing

- **Cleanup**:
  - Remove processed files from `/tmp/visitas`.
  - Archive files in `/home/etl/visitas/bckp` using zipping and date-naming.


### Testing and Validation [not implemented]:

To ensure comprehensive testing, I would including unit tests for individual components and integration tests for the entire ETL pipeline.
This can be integrated into a CI/CD pipeline.

### Security Considerations:
As this project involves data handling, we should ensure that all data transfer and storage is secure, especially when moving to a production environment.
However this implementation for the mock server is not using a passowrd for simplicity.