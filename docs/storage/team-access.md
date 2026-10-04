\# SeaweedFS Team Access Guide



\## 1. Overview



TeleScope uses SeaweedFS as shared object storage for project data.



Team members access the storage through the S3-compatible API using AWS CLI.



\*\*Team members do not need SSH access to the Ubuntu Server.\*\*



\## 2. Requirements



Before accessing the storage, install:



\- AWS CLI

\- Network/LAN access to the TeleScope storage server



\### Storage Endpoint



```text

http://192.168.1.10:8333

````



\### Bucket



```text

telecom-data

```



\## 3. Configure Your AWS CLI Profile



Run:



```cmd

aws configure --profile telecom-team

```



Enter the credentials provided by the project administrator.



\*\*Never commit credentials to GitHub.\*\*



\*\*Never share your credentials with other team members.\*\*



\## 4. Test Your Access



List the project bucket:



```cmd

aws s3 ls s3://telecom-data --endpoint-url http://192.168.1.10:8333 --profile telecom-team

```



If the command works, your connection to SeaweedFS is working correctly.



\## 5. Upload Data



Example:



```cmd

aws s3 cp my\_we\_reviews\_ar.csv s3://telecom-data/raw/reviews/my\_we/ar/my\_we\_reviews\_ar.csv --endpoint-url http://192.168.1.10:8333 --profile telecom-team

```



For English reviews:



```cmd

aws s3 cp my\_we\_reviews\_en.csv s3://telecom-data/raw/reviews/my\_we/en/my\_we\_reviews\_en.csv --endpoint-url http://192.168.1.10:8333 --profile telecom-team

```



\## 6. Download Data



Example:



```cmd

aws s3 cp s3://telecom-data/raw/reviews/my\_we/ar/my\_we\_reviews\_ar.csv . --endpoint-url http://192.168.1.10:8333 --profile telecom-team

```



\## 7. List Files



List everything inside the reviews directory:



```cmd

aws s3 ls s3://telecom-data/raw/reviews/ --recursive --endpoint-url http://192.168.1.10:8333 --profile telecom-team

```



List one application's data:



```cmd

aws s3 ls s3://telecom-data/raw/reviews/my\_we/ --recursive --endpoint-url http://192.168.1.10:8333 --profile telecom-team

```



\## 8. Storage Structure



The main storage structure is:



```text

telecom-data/

├── raw/

│   ├── reviews/

│   ├── surveys/

│   └── offers/

├── processed/

│   ├── reviews/

│   ├── surveys/

│   └── offers/

└── curated/

&#x20;   ├── reviews/

&#x20;   ├── features/

&#x20;   └── ml/

```



\### Raw



Original data collected from external sources.



\### Processed



Cleaned and transformed data.



\### Curated



Data prepared for analytics and Machine Learning.



For more details, see:



`storage-architecture.md`



\## 9. Review Data Structure



Reviews are organized by company and language:



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



\## 10. Security Rules



\### Never Commit Credentials



Never commit the following to GitHub:



```text

Access Keys

Secret Keys

Passwords

.env files

s3.json

```



\### Do Not Share Credentials



Each team member should use their own assigned credentials.



\### Do Not Access Internal SeaweedFS Storage



Team members should not directly modify:



```text

/data

```



or SeaweedFS internal configuration files.



All storage operations should be performed through the S3 API.



\### Do Not Delete Shared Data



Do not delete shared project data unless you are explicitly authorized by the project administrator.



\## 11. Server Access vs Storage Access



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



\## 12. Useful Commands



\### Check AWS CLI



```cmd

aws --version

```



\### List Bucket



```cmd

aws s3 ls s3://telecom-data --endpoint-url http://192.168.1.10:8333 --profile telecom-team

```



\### Upload



```cmd

aws s3 cp FILE s3://telecom-data/PATH --endpoint-url http://192.168.1.10:8333 --profile telecom-team

```



\### Download



```cmd

aws s3 cp s3://telecom-data/PATH FILE --endpoint-url http://192.168.1.10:8333 --profile telecom-team

```



\### List Recursively



```cmd

aws s3 ls s3://telecom-data/PATH --recursive --endpoint-url http://192.168.1.10:8333 --profile telecom-team

```



\## 13. Team Workflow



The general workflow is:



```text

Data Collection

&#x20;      |

&#x20;      v

&#x20;    RAW

&#x20;      |

&#x20;      v

Processing \& Cleaning

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



Follow the storage structure and keep the three data layers separated.



\## 14. Administrator Responsibilities



The project administrator is responsible for:



\* Creating team accounts

\* Managing access permissions

\* Managing SeaweedFS configuration

\* Server maintenance

\* Storage management

\* Managing credentials



Team members should contact the administrator if they have an access or storage problem.



````

