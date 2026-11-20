# NYC Taxi Big Data Platform

## Overview

An end-to-end Data Engineering project built around New York City Yellow Taxi trip data.

The objective is to design and implement a reliable, scalable, and maintainable data platform using modern Data Engineering technologies.

The project follows a **Databricks-first Lakehouse architecture**, combining distributed data processing, transactional storage, data quality, workflow orchestration, and analytics.

Development is incremental, with an emphasis on practical implementation, testing, reproducibility, and documentation.

## Architecture

The target data pipeline follows the Medallion Architecture:

```text
NYC Taxi & Limousine Commission
             |
             v
      RAW / Landing
   Unity Catalog Volume
             |
             v
      BRONZE / Delta
    Raw ingested records
             |
             v
      SILVER / Delta
   Cleaned and validated data
             |
             v
       GOLD / Delta
    Analytics-ready datasets
             |
             v
      Databricks SQL
       AI/BI Dashboard
```

Apache Spark handles data transformations, Delta Lake provides transactional table management, Unity Catalog governs data assets, and Lakeflow Jobs orchestrates the pipeline.

For detailed architecture decisions, see [Architecture V1](docs/architecture/architecture-v1.md).

## Technology Stack

| Category | Technologies |
|---|---|
| Cloud Data Platform | Databricks |
| Processing | Apache Spark, PySpark, Spark SQL |
| Storage | Parquet, Delta Lake |
| Data Governance | Unity Catalog |
| Orchestration | Lakeflow Jobs |
| Analytics | Databricks SQL, AI/BI Dashboards |
| Version Control | Git, GitHub |
| Development | Python, SQL |

### Planned Extensions

- Apache Airflow for external orchestration.
- dbt Core for SQL transformations and data modeling.
- GitHub Actions for CI/CD.
- Automated data quality tests.
- MLflow and Spark MLlib for machine learning experiments.
- Performance benchmarking and optimization.

These components will be integrated progressively after validation.

## Data Source

The project uses publicly available Yellow Taxi trip records from the New York City Taxi and Limousine Commission (TLC).

Official source: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

The initial dataset is `yellow_tripdata_2025-01.parquet`.

The pipeline is designed to support additional monthly datasets.

Large source datasets are not stored in this GitHub repository.

## Data Organization

The initial Databricks resources are:

| Object | Name |
|---|---|
| Unity Catalog Catalog | `workspace` |
| Schema | `nyc_taxi` |
| Managed Volume | `raw_data` |
| Test Delta Table | `smoke_test_delta` |

The Bronze, Silver, and Gold layers will be implemented as Delta tables.

## Implementation Status

### Validated

- Databricks Serverless notebook execution.
- Apache Spark DataFrame operations.
- Unity Catalog schema creation.
- Managed Volume creation and exploration.
- Parquet file writing and reading.
- Delta table creation and SQL querying.
- GitHub integration through Databricks Git folders.

### In Progress

- Repository organization and documentation.
- Data ingestion preparation.

### Planned

- Batch ingestion with file manifests.
- Bronze Delta ingestion and batch traceability.
- Silver transformations and quality validation.
- Gold analytical models and KPIs.
- Interactive SQL dashboards.
- Automated workflows using Lakeflow Jobs.
- Idempotent processing and recovery tests.

## Development Principles

The project follows several engineering principles:

1. Build and validate incrementally.
2. Separate storage, processing, and orchestration responsibilities.
3. Preserve raw data for reproducibility.
4. Implement explicit data quality controls.
5. Track ingestion metadata and pipeline execution.
6. Design repeatable and idempotent data processing.
7. Document architectural decisions and technical limitations.
8. Version code and configuration using Git.

## Project Documentation

- [Architecture V1](docs/architecture/architecture-v1.md)
- [Learning Log](docs/learning-log.md)

Additional documentation, tests, and implementation instructions will be added as development progresses.

## Project Goal

The final objective is to deliver a demonstrable Data Engineering platform with reliable ingestion, validated transformations, business analytics, automated execution, and documented technical decisions.