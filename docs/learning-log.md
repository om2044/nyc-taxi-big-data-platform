# NYC Taxi Data Platform: Learning Log

## Purpose

This document tracks technical progress, challenges, solutions, and lessons learned during the development of the NYC Taxi Data Platform.

Each entry documents:

- Objective
- Implementation
- Issues encountered
- Resolution
- Lessons learned
- Validation evidence

---

## Entry 01: Databricks Environment and Unity Catalog

### Objective

Set up the initial Databricks environment and understand data organization through Unity Catalog.

### Implementation

- Executed a PySpark notebook using Serverless compute.
- Explored available catalogs using `SHOW CATALOGS`.
- Selected the `workspace` catalog.
- Created the `nyc_taxi` schema.
- Created the `raw_data` managed Volume.
- Explored the resources using Catalog Explorer.

### Lessons Learned

- Unity Catalog manages data governance, metadata, and permissions.
- Data assets follow the `catalog.schema.object` naming hierarchy.
- A schema logically groups tables and Volumes.
- Managed Volumes provide governed access to files.
- Logical data organization is different from physical cloud storage.

### Validation

The schema and managed Volume were successfully created and accessed through Databricks.

---

## Entry 02: Delta Lake and Parquet

### Objective

Understand Delta Lake and validate basic data storage operations.

### Implementation

- Created the `smoke_test_delta` table.
- Confirmed that the table uses the Delta format.
- Queried the table using SQL.
- Created a small Spark DataFrame.
- Wrote the DataFrame as Parquet files into the `raw_data` Volume.
- Successfully read the stored Parquet data.

### Lessons Learned

- Parquet is a columnar file format.
- Delta Lake is a transactional table format built on Parquet.
- A Delta table includes Parquet data files and a transaction log named `_delta_log`.
- Delta Lake supports transactions, table history, and schema management.
- A Unity Catalog Volume and a Delta table are different types of data objects.

### Validation

- Delta table creation and SQL reading succeeded.
- The Delta format was confirmed.
- Parquet write and read operations completed successfully.

---

## Entry 03: GitHub Integration with Databricks

### Objective

Connect the project repository to Databricks and establish a version-controlled development environment.

### Implementation

- Imported the existing GitHub repository into Databricks using Git folders.
- Configured GitHub authentication.
- Authorized the Databricks GitHub application to access the repository.
- Created the `feat/databricks-foundation` development branch.

### Issues Encountered

**Issue 1: Missing Git credentials**

Databricks could access the public repository but could not perform authenticated Git operations.

**Resolution:**

Configured GitHub authentication through Databricks account settings.

**Issue 2: Repository access denied**

The GitHub application did not initially have permission to access the selected repository.

**Resolution:**

Updated the GitHub application permissions to authorize repository access.

### Lessons Learned

- Git enables version control and change tracking.
- Branches isolate development work from the main codebase.
- Reading a public repository does not require the same permissions as writing to it.
- Git authentication and repository authorization are separate concerns.

### Validation

The Git folder was successfully connected, and the development branch was created.

---

## Entry 04: Repository Documentation

### Objective

Prepare the repository for structured and reproducible development.

### Work Prepared

- Define repository exclusions in `.gitignore`.
- Document the target architecture in `architecture-v1.md`.
- Introduce the platform in `README.md`.
- Record technical progress in this learning log.

### Lessons Learned

- Documentation is part of Data Engineering.
- Architecture documentation explains technical decisions and responsibilities.
- A README communicates project goals, implementation status, and usage.
- A learning log helps preserve debugging experience and technical reasoning.
- Features should be documented according to their actual implementation status.

### Validation

Pending Git commit, push, and verification of the updated files on GitHub.

---

## Next Milestones

- Finalize repository organization.
- Commit and push the foundation documentation.
- Import the official NYC Taxi Parquet source data.
- Implement the ingestion manifest.
- Build the Bronze Delta ingestion layer.
- Validate batch reprocessing and idempotency.
- Continue with Silver, Gold, analytics, and workflow orchestration.