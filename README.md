# ETL Process Implementation Guide

This guide outlines the steps for implementing an ETL (Extract, Transform, Load) process using SFTP for data extraction, transforming data for database compatibility, and loading it into a PostgreSQL database.

## Extract

- **SFTP Connection**: Establish a connection to the SFTP server (8.8.8.8) to access `/home/vinkOS/archivosVisitas`.
- **File Download**: Target files with the `report_*.txt` pattern. Downloaded files are temporarily stored in `/tmp/visitas`.

## Transform

- **File Processing**: For each file:
  - Validate layout, email, and date fields.
  - Split data into `visitor` and `statistics` objects.
  - Enrich data with calculated metrics and Date object conversion.

## Load

- **Database Interaction**:
  - Update `visitor` table using insert/update logic to handle unique email entries.
  - Populate `statistics` and `errors` tables.
  - Clear `statistics` and `errors` tables before each ETL run.

## Error Handling

- **Logging and Alerts**:
  - Capture and log validation/load errors in the `errors` table.
  - Set up email notifications for post-ETL run issues.
  - Implement retry logic for failed loads, e.g., during DB outages.

## Post-processing

- **Cleanup**:
  - Remove processed files from `/tmp/visitas`.
  - Archive files in `/home/etl/visitas/bckp` using zipping and date-naming.

## Development Plan

### Phase 1: Setup

- **Dev Container**: Configure with Anaconda, PostgreSQL, `paramiko`, `psycopg2`/`sqlalchemy`.
- **Mock SFTP Server**: Install and configure within the dev container. Populate with sample data.

### Phase 2: ETL Scripting

- **Extraction Script**: Implement file downloading and pattern matching.
- **Transformation Logic**: Develop validation, parsing, and enrichment functionalities.
- **Load Functions**: Code database interactions for data insertion and table management.

### Phase 3: Error Handling & Logging

- **Error Handling**: Incorporate try-except blocks; log exceptions to the `errors` table.
- **Logging**: Set up a logging mechanism for ETL steps and outcomes.

### Phase 4: Post-Processing

- **File Management**: Code for file deletion and archiving after processing.

### Phase 5: Testing

- **Unit Testing**: Cover all components.
- **Integration Testing**: Run full ETL in the dev environment; validate data processing and loading.

### Phase 6: Automation

- **Scheduling**: Implement `cron` jobs for automated ETL runs.
- **Production Transition**: Document configuration changes for the shift to production.

### Phase 7: Documentation & Knowledge Transfer

- **Documentation**: Create comprehensive guides covering setup, process flows, and troubleshooting.
- **Knowledge Transfer**: Organize sessions and prepare guides for team members.