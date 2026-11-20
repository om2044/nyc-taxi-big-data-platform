# NYC Taxi Data Platform: Architecture V1

## 1. Project Overview

The NYC Taxi Data Platform is a personal Data Engineering project designed to ingest, process, validate, and analyze New York City Yellow Taxi trip records.

The platform follows a **Databricks-first Lakehouse architecture** using Apache Spark, Delta Lake, Unity Catalog, and Databricks SQL.

Development follows an incremental approach, with each stage validated through functional tests and documented results.

## 2. Architecture Overview

The target data flow is:

**NYC TLC (Parquet) → RAW Volume → Bronze Delta → Silver Delta → Gold Delta → SQL Dashboard**

The main components have distinct responsibilities:

| Component | Responsibility |
|---|---|
| Databricks | Main development and analytics platform |
| Apache Spark / PySpark | Distributed data processing |
| Unity Catalog | Data governance, metadata and permissions |
| Managed Volume | Raw source file storage |
| Delta Lake | Transactional table format |
| Lakeflow Jobs | Workflow orchestration |
| Databricks SQL | Analytical queries |
| AI/BI Dashboard | Business data visualization |

## 3. Data Organization

The initial Unity Catalog organization is:

- **Catalog:** `workspace`
- **Schema:** `nyc_taxi`
- **Managed Volume:** `raw_data`
- **Test Delta table:** `smoke_test_delta`

The Bronze, Silver and Gold layers will initially be represented by Delta tables inside the `nyc_taxi` schema.

## 4. Medallion Architecture

### RAW: Landing Zone

Stores original source files without business transformations.

Initial dataset: `yellow_tripdata_2025-01.parquet`.

### Bronze: Ingestion Layer

Preserves source records with technical metadata such as source file, ingestion timestamp, batch identifier, and source period.

### Silver: Quality Layer

Applies data validation, cleaning, type normalization, and anomaly handling.

Rejected records will be tracked separately.

### Gold: Analytics Layer

Produces business-ready datasets and KPIs, including trip counts, revenues, trip durations, and demand by zone and period.

## 5. Architecture Decisions

**ADR-001: Databricks as the primary platform**

Databricks is the main environment for analytical processing. The earlier Docker/Spark environment remains historical work and may be recovered later.

**ADR-002: Delta Lake for analytical tables**

Delta tables provide transaction management, schema controls, and table history.

**ADR-003: Separate file storage and analytical tables**

Source Parquet files are stored in a Unity Catalog Volume. Bronze, Silver and Gold are managed as Delta tables.

**ADR-004: Batch-first architecture**

NYC TLC monthly trip files are historical batches. Streaming is not part of the initial pipeline.

## 6. Current Implementation Status

**Validated:**

- PySpark Serverless notebook execution.
- Unity Catalog catalog and schema access.
- Managed Volume creation.
- Parquet write/read test in the Volume.
- Delta test table creation and SQL reading.

**Planned:**

- Real TLC Parquet ingestion and manifest.
- Bronze, Silver and Gold pipelines.
- Data quality checks and batch reprocessing.
- SQL analytics and dashboard.
- Lakeflow Jobs orchestration.
- External integrations, subject to Free Edition limitations.

## 7. Development Approach

The project follows a milestone-based development strategy without fixed deadlines.

Each milestone includes:

- Understanding the underlying concepts.
- Implementing the required components.
- Testing functionality and data quality.
- Documenting technical decisions and results.
- Committing validated changes to GitHub.

Progression depends on successful validation rather than predetermined durations.

## 8. V1 Success Criteria

The first version will be considered complete when:

- The initial monthly source dataset has been ingested and validated.
- Bronze, Silver and Gold tables are queryable.
- Data quality checks and rejected records are documented.
- Reprocessing the same batch does not introduce unintended duplicates.
- Business KPIs are verified.
- A Databricks Job executes the pipeline successfully.
- The implementation and its limitations are documented.
