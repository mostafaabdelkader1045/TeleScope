# TeleScope — System Architecture

## 1. Overview

TeleScope is a data and AI platform designed to analyze customer feedback and compare Egyptian telecommunications providers.

The platform integrates application reviews, survey responses, and publicly available telecom offers to generate analytical insights and support company comparisons and recommendations.

The system is designed around a modular architecture that separates data collection, storage, processing, analytics, machine learning, and user interaction.

> **Implementation status:** This document describes the target architecture. Individual components may still be under development.

## 2. Architecture Goals

The architecture aims to:

* Collect data from multiple sources.
* Preserve raw data separately from processed data.
* Build repeatable and maintainable data pipelines.
* Apply data quality checks before analytical use.
* Store structured analytical data in a data warehouse.
* Generate customer sentiment insights and recommendations.
* Present results through a Streamlit application.
* Keep components modular so they can be developed and tested independently.

## 3. High-Level Architecture

```text
                    DATA SOURCES
          ┌────────────┼────────────┐
          │            │            │
       Google Play   Surveys    Websites / APIs
          │            │            │
          └────────────┼────────────┘
                       │
                       ▼
                DATA COLLECTION
                     Python
                       │
                       ▼
               OBJECT STORAGE
                 Raw Data
                       │
                       ▼
               AIRFLOW ORCHESTRATION
                       │
                       ▼
               PYSPARK PROCESSING
             Cleaning and Validation
                       │
                       ▼
                  POSTGRESQL
                Data Warehouse
                       │
                       ▼
                      dbt
              Analytical Data Models
                       │
                ┌──────┴──────┐
                │             │
                ▼             ▼
             Analytics     ML Workflows
                            ├─ Sentiment
                            ├─ Embeddings / NLP
                            └─ Recommendation
                               and Ranking
                │             │
                └──────┬──────┘
                       │
                       ▼
                 STREAMLIT APP
             UI + Application Logic
                       │
                       ▼
                     USERS
```

This diagram represents the intended logical flow. The exact execution order and integration points will be refined during implementation.

## 4. Data Sources

### 4.1 Google Play Reviews

The platform collects reviews and ratings from the selected telecommunications applications:

* My WE
* My Orange
* Ana Vodafone
* Etisalat

Collected fields may include review text, rating, review date, language, and available application metadata.

### 4.2 Surveys

Survey data supports comparisons between telecommunications providers and helps identify customer preferences and satisfaction patterns.

### 4.3 Telecom Offers

Publicly available offers are collected from supported websites or APIs.

Offer data may include provider, offer name, price, validity, included benefits, and other available attributes.

The final schema depends on the fields that can be collected reliably from each source.

## 5. Data Collection Layer

The data collection layer uses Python to retrieve data from the supported sources.

Responsibilities include:

* Collecting source data.
* Handling pagination and collection errors.
* Validating required fields.
* Identifying duplicate records where appropriate.
* Recording collection metadata.
* Writing raw datasets to the configured object storage.

Collection scripts should remain independent of the Streamlit application.

## 6. Storage Layer

The storage layer separates files according to their processing stage.

### Raw

Contains collected data preserved before the main transformation process.

### Processed

Contains data after cleaning, normalization, and initial validation.

### Curated

Contains datasets prepared for analytics, feature generation, or machine learning.

The project currently has SeaweedFS storage documentation and uses an S3-compatible access pattern in its storage setup. The active endpoint and access configuration must be verified against the current team environment.

Large datasets should be stored in the designated object storage rather than committed to GitHub.

## 7. Data Processing and Orchestration

### Apache Airflow

Airflow is intended to orchestrate pipeline tasks, manage dependencies, and monitor execution.

Potential tasks include:

1. Collect or detect new source data.
2. Validate raw datasets.
3. Run processing jobs.
4. Load structured data into PostgreSQL.
5. Execute dbt transformations.
6. Refresh analytical outputs when required.

### PySpark

PySpark is intended for data-processing tasks that benefit from Spark's distributed processing capabilities.

Potential responsibilities include:

* Data cleaning.
* Schema normalization.
* Duplicate handling.
* Data preparation for downstream analytics and ML.

Python and Pandas may be used for smaller tasks where distributed processing is unnecessary.

## 8. Data Warehouse and Transformations

### PostgreSQL

PostgreSQL serves as the planned relational data warehouse for structured and analytical datasets.

The warehouse may contain data related to:

* Reviews and ratings.
* Telecom providers.
* Surveys and responses.
* Telecom offers.
* Sentiment results.
* Recommendation results.
* Aggregated analytical metrics.

The final schema will be documented as implementation progresses.

### dbt

dbt is intended to transform warehouse data into maintainable analytical models.

The project will use three model layers:

* **Staging:** standardize source tables.
* **Intermediate:** implement reusable transformation logic.
* **Marts:** provide datasets designed for analytics and reporting.

Data tests and model documentation should be added as the models are developed.

## 9. Machine Learning Layer

The ML layer is separate from the Streamlit presentation layer.

### Sentiment Analysis

Classifies customer feedback into sentiment categories according to the selected model and evaluation approach.

### Embeddings and NLP

Creates text representations for supported semantic analysis and text-processing tasks.

### Recommendation and Ranking

Uses defined criteria and available data to produce provider comparisons, offer rankings, or other project recommendations.

Model selection, training procedures, evaluation metrics, and deployment details will be documented in the relevant files under `docs/ml/`.

## 10. Streamlit Application Layer

Streamlit is used for the user interface and Python application layer.

A separate React frontend and FastAPI backend are not required for the initial application design.

The application is organized into the following responsibilities:

* **Pages:** user-facing screens and navigation.
* **Components:** reusable charts, filters, and metrics.
* **Services:** application logic and coordination of analytical or ML operations.
* **Repositories:** data access, including database queries.
* **Utilities:** shared helper functions.

Planned application pages include:

* Company Comparison.
* Reviews Analytics.
* Sentiment Analysis.
* Recommendations.
* Survey Insights.
* Offers Explorer.

Streamlit pages should not contain the entire data-processing or model-training implementation. They should call reusable services and display the resulting data.

## 11. Power BI

Power BI may be used as a separate business intelligence and reporting tool if required by the project.

It should complement the Streamlit application rather than duplicate the same functionality without a clear purpose.

The final responsibilities of Power BI and Streamlit will be defined by the team's reporting requirements.

## 12. Configuration and Security

Application configuration should be managed through environment variables and shared configuration modules.

The repository should include an `.env.example` file containing variable names without secret values.

The following must not be committed:

* Passwords and access keys.
* Private tokens.
* Real `.env` files.
* Large raw datasets.
* Local virtual environments.

Access to shared storage and databases should be limited to authorized team members.

## 13. Testing and Data Quality

Testing should cover the following areas:

* Unit tests for reusable Python functions.
* Data quality tests for processed datasets.
* Integration tests for storage and database access.
* Tests for analytical transformations.
* Evaluation of machine learning models.
* Application checks for critical user workflows.

Data quality rules should be documented and implemented alongside the relevant pipeline components.

## 14. Repository Organization

The main project directories have the following responsibilities:

| Directory            | Responsibility                                  |
| -------------------- | ----------------------------------------------- |
| `app/`               | Streamlit application                           |
| `config/`            | Configuration and logging                       |
| `data_collection/`   | Source data collection                          |
| `docs/`              | Project documentation                           |
| `ml/`                | Machine learning modules                        |
| `pipelines/airflow/` | Airflow DAGs                                    |
| `pipelines/spark/`   | PySpark jobs                                    |
| `storage/`           | Storage documentation and integration utilities |
| `transformations/`   | dbt project and models                          |
| `warehouse/`         | Warehouse SQL and schemas                       |
| `tests/`             | Automated tests                                 |
| `scripts/`           | Setup and maintenance scripts                   |
| `powerbi/`           | Power BI assets and documentation               |

## 15. Implementation Principles

The project follows these principles:

1. Keep each component focused on a clear responsibility.
2. Separate data collection from data processing.
3. Preserve raw data and make transformations repeatable.
4. Keep database access outside Streamlit page files.
5. Separate model logic from presentation logic.
6. Test important transformations and data quality rules.
7. Keep configuration and secrets out of source code.
8. Update documentation when architecture or behavior changes.

## 16. Current and Planned Components

The architecture is a development guide, not a statement that every component is operational.

Before treating a component as complete, verify its implementation, configuration, tests, and integration with the rest of the platform.
