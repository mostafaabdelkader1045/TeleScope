# TeleScope.ai 📡

### Egyptian Telecom Reviews, Surveys & Offers Analytics Platform

TeleScope.ai is a data-driven analytics project designed to analyze customer reviews, survey responses, and telecom offers from Egyptian telecommunications providers.

The project aims to transform raw data into structured, reliable, and analytical data that can help users understand customer satisfaction, compare telecom providers, evaluate services, and identify the most suitable providers and offers based on customer preferences.

---

## 📌 Project Overview

The Egyptian telecommunications market includes several providers offering different internet and mobile services. Customers often rely on reviews, ratings, personal experiences, and offers when choosing a provider.

TeleScope.ai collects and processes data from multiple sources, integrates it into a centralized Data Warehouse, and prepares it for analytical insights and future machine learning applications.

The project focuses on building a complete data pipeline, from data collection and storage to data integration, transformation, and analytical modeling.

---

## 🎯 Project Objectives

- Collect customer reviews from telecom applications.
- Gather customer survey responses and telecom offers.
- Store raw data in centralized storage.
- Build an integrated Data Warehouse.
- Improve data quality through cleaning and transformation.
- Analyze customer satisfaction across telecom providers.
- Compare providers based on customer ratings and experiences.
- Analyze telecom offers and customer preferences.
- Prepare analytical datasets for future Machine Learning applications.

---

## 📊 Data Sources

The project focuses on Egyptian telecommunications providers, including:

- WE
- Vodafone
- Orange
- Etisalat

### 1. Application Reviews

Customer reviews collected from telecom provider applications, including information such as:

- Review content
- Rating
- Review date
- App version
- Provider

### 2. Customer Surveys

Survey data collected to understand customers' experiences, satisfaction levels, preferences, and opinions regarding telecom services.

### 3. Telecom Offers

Offers collected from telecom providers, containing information about available packages, prices, benefits, and target customers.

---

## 🏗️ System Architecture

The implemented architecture follows a data engineering workflow:

```text
             Data Sources
       ┌──────────┬──────────┬──────────┐
       │ Reviews  │ Surveys  │  Offers  │
       └────┬─────┴────┬─────┴────┬─────┘
            │          │          │
            ▼          ▼          ▼
       Data Collection & Integration
                  (Python)
                     │
                     ▼
          Azure Blob Storage
             (Raw Data)
                     │
                     ▼
              Bronze Layer
          (PostgreSQL Database)
                     │
                     ▼
              Silver Layer
       (Cleaned & Integrated Data)
                     │
                     ▼
               Gold Layer
         (Analytical Data Models)
                     │
                     ▼
         Analytics & ML Applications
              (Future Work)
```

---

## 🔄 Data Pipeline

The data pipeline consists of the following stages:

### 1. Data Collection

Data is collected from different sources using Python scripts.

Collected datasets include customer reviews, survey responses, and telecom offers.

### 2. Cloud Storage

Raw collected files are stored in Azure Blob Storage to provide centralized storage and facilitate data loading.

### 3. Bronze Layer

The Bronze Layer stores the raw data in the Data Warehouse while preserving the original structure as much as possible.

This layer serves as the initial stage of data ingestion.

### 4. Silver Layer

The Silver Layer contains cleaned, standardized, and integrated data.

Data processing includes preparing data for analytical usage and improving consistency and quality.

### 5. Gold Layer

The Gold Layer provides analytical views organized using a Star Schema.

It includes dimension and fact views designed to support analytical queries and reporting.

---

## 🏛️ Data Warehouse Architecture

The Data Warehouse is implemented using PostgreSQL and follows a three-layer architecture.

### Bronze Layer

Responsible for storing raw ingested data.

### Silver Layer

Responsible for storing cleaned and transformed data.

### Gold Layer

Responsible for providing analytical data models through PostgreSQL Views.

The Gold Layer follows a Star Schema design consisting of Dimension Views and Fact Views.

### Dimension Views

| Dimension | Description |
|---|---|
| `DimCompany` | Telecom providers |
| `DimDate` | Date-related attributes |
| `DimAppVersion` | Application versions |
| `DimTenure` | Customer tenure categories |
| `DimSpending` | Customer spending categories |
| `DimRatingType` | Survey rating categories |
| `DimPreferenceFactor` | Customer preference factors |
| `DimOfferType` | Telecom offer categories |
| `DimTargetCustomer` | Offer target customer categories |
| `DimOffer` | Telecom offers |

### Fact Views

| Fact | Description |
|---|---|
| `FactReviews` | Customer application reviews |
| `FactSurveyResponse` | Survey response records |
| `FactSurveyRating` | Survey ratings |
| `FactSurveyPreference` | Customer preferences |
| `FactOffers` | Telecom offer analytical records |

The Gold Layer currently consists of PostgreSQL Views built on top of the Silver Layer.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data collection and data processing |
| PostgreSQL 17 | Data Warehouse |
| Azure Blob Storage | Cloud object storage |
| SQL | Schema design, transformations, queries, and analytical modeling |
| Docker | Containerization and environment management |
| Docker Compose | Managing project services |
| pgAdmin 4 | PostgreSQL administration and database management |
| Git & GitHub | Version control and collaboration |

### Planned Technologies

The following technologies may be integrated into future development:

- Apache Airflow – Workflow orchestration
- Apache Spark – Distributed data processing
- Machine Learning – Customer analytics and recommendations
- Data Visualization – Analytical dashboards

---

## 📁 Project Structure

```text
TeleScope.ai/
│
├── Docker/
│   └── docker-compose.yml
│
├── docs/
│   ├── data_catalog.md
│   └── images/
│
├── src/
│   ├── data_collection/
│   │   ├── offers/
│   │   ├── reviews/
│   │   │   ├── etisalat_reviews_scraping.py
│   │   │   └── we_reviews_scraping.py
│   │   └── surveys/
│   │
│   ├── data_loading/
│   │   ├── bronze/
│   │   │   ├── bronze_load.py
│   │   │   ├── offers_loader.py
│   │   │   ├── reviews_loader.py
│   │   │   └── survey_loader.py
│   │   │
│   │   ├── silver/
│   │   │   ├── silver_load.py
│   │   │   ├── offers_loader.py
│   │   │   ├── reviews_loader.py
│   │   │   └── survey_loader.py
│   │   │
│   │   └── connections/
│   │       ├── azure_connection.py
│   │       └── database_connection.py
│   │
│   ├── data_transformation/
│   │   └── survey_transformation.py
│   │
│   ├── data_warehouse/
│   │   ├── bronze_layer/
│   │   │   └── Bronze_Layer_Schema.sql
│   │   │
│   │   ├── silver_layer/
│   │   │   └── Silver_layer_Schema.sql
│   │   │
│   │   └── gold_layer/
│   │       ├── create_dimensions.sql
│   │       ├── create_facts.sql
│   │       └── check_*.sql
│   │
│   ├── pipelines/
│   │   ├── airflow/
│   │   │   └── dags/
│   │   └── spark/
│   │       └── jobs/
│   │
│   └── scripts/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites

Make sure the following tools are installed:

- Python 3.12
- Docker Desktop
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/mostafaabdelkader1045/TeleScope.git

cd TeleScope
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment.

**Windows:**

```powershell
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create your `.env` file from the example:

**Windows:**

```powershell
Copy-Item .env.example .env
```

**Linux/macOS:**

```bash
cp .env.example .env
```

Update the environment variables inside `.env` with your own credentials.

---

## 🐳 Running Docker Services

The project uses Docker Compose to manage PostgreSQL and pgAdmin.

Start the services:

```bash
docker compose --env-file .env -f Docker/docker-compose.yml up -d
```

Check service status:

```bash
docker compose --env-file .env -f Docker/docker-compose.yml ps
```

Stop the services:

```bash
docker compose --env-file .env -f Docker/docker-compose.yml stop
```

Start stopped services:

```bash
docker compose --env-file .env -f Docker/docker-compose.yml start
```

### Services

| Service | Port | Description |
|---|---:|---|
| PostgreSQL | `5432` | Data Warehouse Database |
| pgAdmin | `5050` | Database Management Interface |

### Access pgAdmin

Open your browser:

```text
http://localhost:5050
```

Login using the credentials configured in your `.env` file.

---

## 🗄️ Database Configuration

The PostgreSQL database is configured using the following environment variables:

```env
POSTGRES_USER=telescope
POSTGRES_PASSWORD=your_password
POSTGRES_DB=telescope_dw
```

The pgAdmin configuration:

```env
PGADMIN_EMAIL=your_email
PGADMIN_PASSWORD=your_password
```

---

## 👥 Team Database Access

Team members can connect to the shared PostgreSQL database remotely through the configured private network.

Connection parameters:

| Parameter | Value |
|---|---|
| Host | Team Host Tailscale IP |
| Port | `5432` |
| Database | `telescope_dw` |
| Username | `telescope` |
| Password | Provided securely by the project administrator |

Team members should install and connect to the project's Tailscale network before attempting to connect to the database.

No public database port forwarding is required.

---

## 📚 Documentation

Project documentation is maintained inside the `docs/` directory.

- **Data Catalog:** `docs/data_catalog.md`

The Data Catalog documents the Data Warehouse tables, columns, and their descriptions.

---

## 🚧 Project Status

### Implemented

- Data collection scripts for selected telecom applications.
- Azure Blob Storage integration.
- PostgreSQL database infrastructure.
- Docker-based PostgreSQL and pgAdmin deployment.
- Bronze Layer schema and data loading.
- Silver Layer schema and data loading.
- Data transformation processes.
- Gold Layer analytical Views.
- Dimension and Fact modeling.
- Data Catalog documentation.

### In Progress

- Expanding data collection sources.
- Improving data quality and transformations.
- Developing additional analytical capabilities.
- Machine Learning model development.

### Planned

- Automated pipeline orchestration using Apache Airflow.
- Distributed data processing using Apache Spark.
- Customer analytics and recommendation models.
- Interactive dashboards and visualization.

---

## 🔮 Future Work

Future development aims to extend TeleScope.ai with:

- Automated end-to-end data pipelines.
- Advanced customer sentiment analysis.
- Telecom provider recommendation systems.
- Offer comparison and recommendation models.
- Customer satisfaction prediction.
- Interactive analytics dashboards.

---

## 👨‍💻 Team

TeleScope.ai is developed as a graduation project by a team of students specializing in Data Engineering, Data Science, and Machine Learning.

---

## 📄 License

This project was developed for educational and graduation project purposes.