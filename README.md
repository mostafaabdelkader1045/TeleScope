# TeleScope AI Platform

TeleScope is a data and AI platform for analyzing customer feedback and comparing Egyptian telecommunications providers. It brings together app reviews, survey responses, and publicly available offers to support evidence-based insights and recommendations.

> **Project status:** In development. This repository structure and the documented architecture describe the intended design; individual components may not be implemented yet.

## Project Goals

- Collect customer reviews and ratings from Google Play.
- Bring together survey responses and telecom offers from supported sources.
- Store raw data separately from processed and analytics-ready data.
- Build repeatable data-processing and transformation workflows.
- Analyze customer sentiment and recurring feedback themes.
- Compare providers using clearly defined metrics.
- Explore recommendation and ranking approaches.
- Present insights through a Streamlit application.

## Data Sources

The planned data sources are:

- **Google Play:** app reviews, ratings, and available review metadata for the selected telecom applications.
- **Surveys:** responses collected by the project team to compare providers and understand user preferences.
- **Websites and APIs:** publicly available telecom offers and related information, subject to source availability and applicable terms.

Collected data should be validated, documented, and handled according to the project's data-quality and privacy requirements.

## Architecture Overview

The intended end-to-end flow is:

```text
Google Play       Surveys       Websites / APIs
     \               |                /
      +--------------+---------------+
                     |
                     v
              Python Collection
                     |
                     v
            S3-Compatible Object Storage
                  Raw Data
                     |
                     v
           Airflow Orchestration
                     |
                     v
           PySpark Processing Jobs
                     |
                     v
                PostgreSQL
              Data Warehouse
                     |
                     v
                dbt Models
                     |
          +----------+----------+
          |                     |
          v                     v
    Analytics Tables       ML Workflows
                           - Sentiment
                           - Embeddings / NLP
                           - Recommendation / Ranking
          |                     |
          +----------+----------+
                     |
                     v
               Streamlit App
       User Interface + Application Logic
```

This diagram is a target design, not a claim that every component is already deployed. The actual workflow may evolve as implementation and testing progress.

### Technology Stack

| Area | Planned technology | Responsibility |
|---|---|---|
| Data collection | Python | Collect data from supported sources |
| Object storage | SeaweedFS with an S3-compatible API, subject to current environment configuration | Store raw and intermediate files |
| Orchestration | Apache Airflow | Schedule and monitor pipeline tasks |
| Distributed processing | PySpark | Process larger datasets when distributed processing is useful |
| Data transformations | dbt | Build tested SQL data models |
| Data warehouse | PostgreSQL | Store structured analytical data |
| Machine learning | Python NLP/ML components | Sentiment analysis, embeddings, recommendation, and ranking |
| Application | Streamlit | Provide the interactive user interface and application workflows |
| Optional BI | Power BI | Separate management dashboards, if required |

The repository's implementation and configuration files are the source of truth for which services are currently active. Do not assume that a planned tool has already been configured.

## Repository Structure

```text
TeleScope.ai/
├── app/                    # Streamlit pages, components, services, repositories
├── config/                 # Application and environment configuration
├── data_collection/        # Reviews, surveys, offers, shared collection utilities
├── docs/                   # Architecture, storage, data, ML, and setup documentation
├── ml/                     # Sentiment, embeddings, and recommendation modules
├── pipelines/
│   ├── airflow/            # Airflow DAGs
│   └── spark/              # PySpark jobs
├── powerbi/                # Power BI documentation and related project assets
├── scripts/                # Developer and maintenance scripts
├── storage/                # Storage notes and integration helpers
├── tests/                  # Unit, integration, and data-quality tests
├── transformations/        # dbt project and models
├── warehouse/              # Warehouse schemas and SQL assets
├── .env.example            # Names of required environment variables (no secrets)
├── .gitignore
├── requirements.txt         # Python dependencies, when established
└── README.md
```

Some directories may contain only a `.gitkeep` placeholder while their implementation is pending.

## Streamlit Application

Streamlit is planned for both the user interface and the Python application layer; a separate React frontend and FastAPI backend are not required for the initial design.

Planned application areas include:

- **Company Comparison:** compare providers using documented metrics.
- **Reviews Analytics:** explore ratings, review volume, and trends.
- **Sentiment Analysis:** view sentiment results and feedback themes.
- **Recommendations:** display recommendations or rankings produced by the ML layer.
- **Survey Insights:** summarize survey responses.
- **Offers Explorer:** browse and compare collected offers.

Keep UI code separate from business logic. Streamlit pages should call application services, which in turn use repositories or ML modules. Avoid putting database queries, model training, and all business logic directly in page files.

## Storage Principles

- Keep raw collected data separate from processed and curated outputs.
- Store large datasets and generated artifacts in the configured object storage, not in Git.
- Keep credentials and secrets out of source control.
- Document the active storage endpoint, access method, and team setup in `docs/storage/`.
- Do not commit real `.env` files, access keys, passwords, or private endpoints.

Refer to the storage documentation in [`docs/storage/`](docs/storage/) for environment-specific details.

## Getting Started

### Prerequisites

Install only the tools required for the component you intend to work on. Depending on the workflow, these may include:

- Git
- Python and a virtual environment
- Streamlit
- Access to the configured PostgreSQL database
- Access to the configured S3-compatible object storage
- Airflow, PySpark, and dbt for the relevant data-pipeline tasks

Exact versions and service setup should be documented as the environment is finalized.

### Local setup

1. Clone the repository:

   ```bash
   git clone https://github.com/mostafaabdelkader1045/TeleScope.git
   cd TeleScope
   ```

2. Create and activate a virtual environment:

   **Windows PowerShell**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **Linux / macOS**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies if `requirements.txt` has been populated and reviewed:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Create a local `.env` file based on `.env.example` when the required variables have been defined. Fill it with your own authorized environment values; never commit it.

5. Follow the storage, database, and pipeline setup guides in [`docs/`](docs/).

### Running Streamlit

Once the application entry point and its dependencies are implemented, run:

```bash
streamlit run app/Home.py
```

This command is the intended entry point. It will work once `app/Home.py`, the required dependencies, and the relevant configuration are in place.

## Development Guidelines

- Keep each module focused on one responsibility.
- Put shared application logic in services or reusable modules, not directly in Streamlit pages.
- Keep data collection, processing, dbt transformations, and ML workflows separate.
- Add tests for transformations, business rules, and data-quality checks.
- Document required environment variables without including their secret values.
- Use clear, focused commits and descriptive pull requests.
- Never commit raw customer datasets, credentials, local virtual environments, or generated files.

## Contributing

1. Sync your local branch with the team's agreed branch.
2. Create a feature branch for substantial changes when the team workflow calls for one.
3. Keep changes focused on one task.
4. Run relevant tests and checks.
5. Update documentation when behavior, configuration, or architecture changes.
6. Open a pull request and request review before merging when required by the team.

See [`docs/team/`](docs/team/) for team-specific contribution and access instructions as they are added.

## Security and Data Handling

- Do not commit `.env`, credentials, tokens, or private keys.
- Do not upload large datasets to GitHub; use the approved team storage.
- Limit access to data and services to authorized team members.
- Follow the applicable source terms and the team's data-handling requirements.

## Team

TeleScope is developed as a collaborative graduation project. Add the current team members and their responsibilities here once the team has agreed on the final ownership assignments.

## License

A license has not yet been specified. Until the project team selects one, do not assume that the repository is open for unrestricted reuse.
