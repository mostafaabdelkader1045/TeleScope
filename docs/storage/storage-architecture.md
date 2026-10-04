\# TeleScope Storage Architecture



\## 1. Overview



TeleScope uses SeaweedFS as the shared object storage layer for the project.



SeaweedFS provides an S3-compatible API, allowing the team to interact with shared project data using AWS CLI and other S3-compatible tools.



Team members should access the storage through the S3 API and should not access SeaweedFS internal storage directly.



\---



\## 2. Storage Configuration



\*\*S3 Endpoint:\*\*



```text

http://192.168.1.10:8333

````



\*\*Bucket:\*\*



```text

telecom-data

```



\---



\## 3. Bucket Structure



```text

telecom-data/

│

├── raw/

│   ├── reviews/

│   │   ├── my\_we/

│   │   │   ├── ar/

│   │   │   └── en/

│   │   ├── vodafone/

│   │   │   ├── ar/

│   │   │   └── en/

│   │   ├── orange/

│   │   │   ├── ar/

│   │   │   └── en/

│   │   └── etisalat/

│   │       ├── ar/

│   │       └── en/

│   │

│   ├── surveys/

│   └── offers/

│

├── processed/

│   ├── reviews/

│   ├── surveys/

│   └── offers/

│

└── curated/

&#x20;   ├── reviews/

&#x20;   ├── features/

&#x20;   └── ml/

```



\---



\## 4. Data Layers



\### Raw



The `raw/` layer contains the original data collected from external sources.



Examples:



\* Google Play reviews

\* Survey responses

\* Telecom offers



Raw data should remain as close as possible to the original collected format.



\---



\### Processed



The `processed/` layer contains cleaned and transformed data.



Typical operations include:



\* Removing duplicates

\* Handling missing values

\* Data type conversion

\* Data cleaning

\* Normalization

\* Text preprocessing



\---



\### Curated



The `curated/` layer contains data prepared for analytics and Machine Learning.



Examples:



\* Aggregated datasets

\* Feature datasets

\* ML-ready datasets

\* Final datasets used by models



\---



\## 5. Reviews Organization



Reviews are organized by company and language.



```text

raw/reviews/

├── my\_we/

│   ├── ar/

│   └── en/

├── vodafone/

│   ├── ar/

│   └── en/

├── orange/

│   ├── ar/

│   └── en/

└── etisalat/

&#x20;   ├── ar/

&#x20;   └── en/

```



Example:



```text

raw/reviews/my\_we/ar/my\_we\_reviews\_ar.csv

```



\---



\## 6. Naming Convention



Use descriptive and consistent file names.



Recommended format:



```text

<company>\_<dataset>\_<language>.<extension>

```



Examples:



```text

my\_we\_reviews\_ar.csv

my\_we\_reviews\_en.csv

vodafone\_reviews\_ar.csv

vodafone\_reviews\_en.csv

orange\_reviews\_ar.csv

orange\_reviews\_en.csv

etisalat\_reviews\_ar.csv

etisalat\_reviews\_en.csv

```



\---



\## 7. Data Pipeline



The general data flow is:



```text

External Sources

&#x20;      |

&#x20;      v

Data Collection

&#x20;      |

&#x20;      v

&#x20;    RAW

&#x20;      |

&#x20;      v

Data Cleaning \& Processing

&#x20;      |

&#x20;      v

&#x20; PROCESSED

&#x20;      |

&#x20;      v

Feature Engineering

&#x20;      |

&#x20;      v

&#x20;  CURATED

&#x20;      |

&#x20;      v

Analytics / Machine Learning

```



The original collected data should remain available in `raw/` so that the processing pipeline can be reproduced when necessary.



\---



\## 8. Access Model



Team members access SeaweedFS through the S3-compatible API.



The project bucket is:



```text

telecom-data

```



Team members should use their assigned S3 credentials.



The administrator is responsible for:



\* Creating team accounts

\* Managing permissions

\* Managing SeaweedFS configuration

\* Server maintenance

\* Storage management



\---



\## 9. Server Access vs Storage Access



These are two different types of access.



\### Server Access



SSH provides access to the Ubuntu Server itself.



```text

Team Member

&#x20;    |

&#x20;    | SSH

&#x20;    v

Ubuntu Server

```



SSH access should only be given to authorized administrators.



\### Storage Access



S3 credentials provide access to project data.



```text

Team Member

&#x20;    |

&#x20;    | AWS CLI / S3 API

&#x20;    v

SeaweedFS

&#x20;    |

&#x20;    v

telecom-data

```



Normal team members should use S3 access instead of SSH.



\---



\## 10. Team Access



Team members should configure AWS CLI using their assigned profile.



Example:



```cmd

aws configure --profile telecom-team

```



Test access:



```cmd

aws s3 ls s3://telecom-data --endpoint-url http://192.168.1.10:8333 --profile telecom-team

```



Upload example:



```cmd

aws s3 cp my\_we\_reviews\_ar.csv s3://telecom-data/raw/reviews/my\_we/ar/my\_we\_reviews\_ar.csv --endpoint-url http://192.168.1.10:8333 --profile telecom-team

```



Download example:



```cmd

aws s3 cp s3://telecom-data/raw/reviews/my\_we/ar/my\_we\_reviews\_ar.csv . --endpoint-url http://192.168.1.10:8333 --profile telecom-team

```



List files:



```cmd

aws s3 ls s3://telecom-data/raw/reviews/ --recursive --endpoint-url http://192.168.1.10:8333 --profile telecom-team

```



\---



\## 11. Security Rules



\### Never commit credentials



Do not commit any of the following to GitHub:



```text

Access Keys

Secret Keys

Passwords

.env files

s3.json

```



\### Do not share credentials



Each team member should use their own assigned credentials.



\### Do not modify SeaweedFS internal storage



Do not directly modify:



```text

/data

```



or SeaweedFS internal files.



All data operations should be performed through the S3 API.



\### Do not delete shared data without permission



Do not use recursive delete commands on shared project data unless explicitly authorized.



\---



\## 12. Team Workflow



Each team member should follow this general workflow:



1\. Collect or receive data.

2\. Upload the original data to `raw/`.

3\. Clean and process the data.

4\. Store processed data under `processed/`.

5\. Perform feature engineering when required.

6\. Store ML-ready datasets under `curated/`.

7\. Use curated datasets for analytics and Machine Learning.



\---



\## 13. Example Data Flow



For Arabic My WE reviews:



```text

Google Play

&#x20;    |

&#x20;    v

Data Collection

&#x20;    |

&#x20;    v

my\_we\_reviews\_ar.csv

&#x20;    |

&#x20;    v

raw/reviews/my\_we/ar/

&#x20;    |

&#x20;    v

Cleaning \& Preprocessing

&#x20;    |

&#x20;    v

processed/reviews/

&#x20;    |

&#x20;    v

Feature Engineering

&#x20;    |

&#x20;    v

curated/features/

&#x20;    |

&#x20;    v

Machine Learning

```



\---



\## 14. Core Principle



The storage architecture follows:



```text

RAW → PROCESSED → CURATED

```



Each layer has a specific purpose.



Do not mix raw, processed, and curated datasets.



This structure keeps the project organized, reproducible, and easy for the entire team to maintain.



````



