\# Chronos AI



\## Intelligent Framework for Predictive System Failure Analytics



Chronos AI is a predictive failure analytics framework designed to analyze machine and system data, predict potential failures, estimate failure probability, classify operational risk, generate maintenance alerts, and store prediction history for further analysis.



The project combines \*\*Machine Learning, Big Data Analytics, FastAPI, Risk Classification, Alert Generation, and MongoDB\*\* into an end-to-end predictive analytics workflow.



\---



\## Problem Statement



Unexpected machine and system failures can lead to production downtime, maintenance costs, equipment damage, and operational interruptions.



Traditional maintenance approaches often depend on fixed schedules or react only after a failure occurs.



Chronos AI focuses on a predictive approach:



\*\*Analyze data → Predict failure → Estimate risk → Generate alert → Store result\*\*



The objective is to provide an intelligent system that can identify potentially risky operating conditions before they develop into major failures.



\---



\## Project Objectives



\* Analyze machine and system data for failure patterns.

\* Clean and preprocess raw datasets.

\* Perform exploratory data analysis.

\* Engineer meaningful predictive features.

\* Develop machine-learning models for failure prediction.

\* Estimate machine failure probability.

\* Classify predictions into operational risk levels.

\* Generate alerts for elevated and critical risk.

\* Provide predictions through a REST API.

\* Store prediction history in MongoDB.

\* Build a foundation for real-time predictive analytics and visualization.



\---



\## End-to-End Workflow



```text

Data Sources

&#x20;    ↓

Data Cleaning \& Preprocessing

&#x20;    ↓

Exploratory Data Analysis

&#x20;    ↓

Feature Engineering

&#x20;    ↓

Feature Selection

&#x20;    ↓

Machine Learning Model

&#x20;    ↓

Failure Prediction

&#x20;    ↓

Failure Probability

&#x20;    ↓

Risk Classification

&#x20;    ↓

Alert Generation

&#x20;    ↓

MongoDB Storage

&#x20;    ↓

API / Dashboard

```



\---



\## Datasets



Chronos AI works with multiple types of data to explore both machine-level and system-level failure analytics.



\### 1. AI4I 2020 Predictive Maintenance Dataset



Used as the primary machine predictive-maintenance dataset.



It contains information such as:



\* Air temperature

\* Process temperature

\* Rotational speed

\* Torque

\* Tool wear

\* Machine failure

\* Failure-related indicators



The dataset contains \*\*10,000 observations\*\*.



\### 2. HDFS Log Dataset



Used for large-scale system log analysis.



The processed HDFS dataset contains more than \*\*11 million log records\*\* and includes fields such as:



\* Date

\* Time

\* Log ID

\* Level

\* Block ID

\* Message

\* Anomaly label



\### 3. HDFS Anomaly Labels



Normal and anomalous system behavior labels were integrated with HDFS logs using block identifiers.



\### 4. Synthetic Big Data Dataset



Used for additional analytics and testing with operational features such as:



\* CPU utilization

\* Memory usage

\* Disk I/O

\* Network latency

\* Process count

\* Thread count

\* Context switches

\* Cache miss rate

\* Temperature

\* Power consumption

\* Uptime

\* Status



> Large raw datasets are intentionally excluded from this repository to keep the repository lightweight.



\---



\## Data Preprocessing



The project includes separate preprocessing scripts for the different data sources.



Major preprocessing operations include:



\* Removing unnecessary identifiers.

\* Checking and handling duplicate records.

\* Checking missing values.

\* Structuring raw HDFS logs.

\* Merging HDFS logs with anomaly labels.

\* Preparing machine-learning-ready datasets.

\* Validating processed data.



\---



\## Feature Engineering



Several derived features were created to improve failure-risk representation.



Important engineered features include:



\* High Torque

\* Power Indicator

\* Temperature Difference

\* High Tool Wear

\* Temperature Stress



These features help represent potentially abnormal operating conditions in a form suitable for machine-learning models.



\---



\## Machine Learning



\### Random Forest



Random Forest was used as the primary classification model for machine failure prediction.



Training configuration:



\* Number of trees: \*\*100\*\*

\* Maximum depth: \*\*8\*\*

\* Random seed: \*\*42\*\*

\* Target: `Machine failure`



Two stages of model development were explored:



1\. PySpark ML Random Forest for big-data-oriented experimentation.

2\. Scikit-learn Random Forest for the prediction API.



\---



\## Model Performance



The Scikit-learn Random Forest model achieved the following results on the evaluated test set:



| Metric    | Result |

| --------- | -----: |

| Accuracy  |  0.999 |

| Precision |  1.000 |

| Recall    | 0.9688 |

| F1 Score  | 0.9841 |

| ROC-AUC   | 0.9778 |



\### Confusion Matrix



```text

True Negative  = 1857

False Positive = 0

False Negative = 2

True Positive   = 62

```



These results describe the evaluated test set used during development and should not be interpreted as a guarantee of performance on unseen real-world environments.



\---



\## FastAPI Prediction Service



The trained model was integrated into a FastAPI REST service.



\### API



```text

http://127.0.0.1:8000

```



\### Swagger Documentation



```text

http://127.0.0.1:8000/docs

```



\### Main Endpoints



| Endpoint          | Purpose                    |

| ----------------- | -------------------------- |

| `GET /`           | API information            |

| `GET /health`     | Service health check       |

| `GET /model-info` | Model information          |

| `POST /predict`   | Machine failure prediction |



The prediction endpoint accepts machine operating parameters and returns prediction and risk information.



\---



\## Risk Classification



Chronos converts failure probability into three operational risk levels.



| Failure Probability | Risk Level |

| ------------------- | ---------- |

| `< 30%`             | NORMAL     |

| `30% – 69.99%`      | WARNING    |

| `≥ 70%`             | CRITICAL   |



This makes the model output easier to interpret than a binary prediction alone.



\---



\## Alert System



Chronos generates alerts based on the calculated risk level.



\### NORMAL



No immediate alert is required.



\### WARNING



The system indicates elevated risk and recommends maintenance inspection.



\### CRITICAL



The system indicates a high probability of failure and recommends immediate maintenance attention.



\---



\## MongoDB Integration



Prediction results are stored in MongoDB for persistence and historical analysis.



\### Database



```text

chronos\_ai

```



\### Collection



```text

predictions

```



\### Connection



```text

mongodb://127.0.0.1:27017/

```



Stored information includes:



\* Timestamp

\* Machine identifier

\* Input request

\* Prediction

\* Failure probability

\* Normal probability

\* Risk level

\* Alert status

\* Alert message



\---



\## API + Database Integration



The current implementation connects the prediction API with MongoDB.



```text

Machine Input

&#x20;    ↓

FastAPI

&#x20;    ↓

Random Forest

&#x20;    ↓

Prediction

&#x20;    ↓

Failure Probability

&#x20;    ↓

Risk Classification

&#x20;    ↓

Alert

&#x20;    ↓

MongoDB

```



During integration testing:



```text

Total MongoDB records: 4



NORMAL   : 1

WARNING  : 1

CRITICAL : 2

```



The integration was successfully validated using normal and high-risk test cases.



\---



\## Testing \& Validation



The API was tested using:



\* Home endpoint

\* Health endpoint

\* Model information endpoint

\* Normal prediction

\* High-risk prediction



\### API Test Result



\*\*5/5 tests passed successfully.\*\*



Database integration was also verified by inserting and retrieving prediction records and checking risk-level counts.



\---



\## Project Development Progress



\### Completed



\* Project foundation

\* Dataset collection

\* Data cleaning

\* Exploratory data analysis

\* Feature engineering

\* Feature selection

\* ML dataset preparation

\* PySpark Random Forest experimentation

\* Scikit-learn Random Forest model

\* Prediction module

\* FastAPI prediction API

\* Risk classification

\* Alert system

\* API testing and validation

\* MongoDB integration

\* FastAPI + MongoDB integration



\### Current Development Stage



The backend prediction pipeline is operational.



The next development stage is focused on strengthening the user-facing dashboard and visualization layer for prediction history, risk distribution, alerts, and analytics.



\---



\## Technology Stack



\### Programming



\* Python

\* JavaScript



\### Machine Learning



\* Scikit-learn

\* PySpark ML



\### Backend



\* FastAPI

\* Uvicorn



\### Database



\* MongoDB

\* PyMongo



\### Frontend



\* React

\* Vite

\* Electron



\### Data Processing



\* Pandas

\* NumPy

\* PySpark



\### Development Tools



\* Git

\* GitHub

\* PowerShell / Windows



\---



\## Repository Structure



```text

Chronos-AI/

│

├── app/

├── backend/

├── frontend/

├── electron/

├── datasets/

├── docs/

├── graphs/

├── models/

├── reports/

│

├── day39\_pyspark\_analysis.py

├── day40\_failure\_pattern\_analysis.py

├── day41\_failure\_visualization.py

├── day42\_feature\_relationship\_analysis.py

├── day43\_feature\_engineering.py

├── day44\_feature\_selection.py

├── day45\_ml\_dataset\_preparation.py

├── day46\_ml\_model\_training.py

├── day47\_prediction\_module.py

├── day48\_prediction\_api.py

├── day49\_alert\_risk\_module.py

├── day50\_alert\_api\_integration.py

├── day51\_prediction\_alert\_api.py

├── day52\_api\_testing.py

├── day53\_database\_integration.py

├── day54\_api\_database\_integration.py

│

├── package.json

├── package-lock.json

├── .gitignore

└── README.md

```



\---



\## Project Highlights



\* End-to-end predictive analytics workflow.

\* Combines machine learning with a REST API.

\* Probability-based risk classification.

\* Automated maintenance alerts.

\* Persistent prediction history using MongoDB.

\* PySpark experimentation for big-data analytics.

\* Multiple data sources for machine and system failure analysis.

\* Modular development with preprocessing, ML, API, and database components.



\---



\## Future Scope



Future development can extend Chronos AI with:



\* Real-time machine-data ingestion.

\* Live monitoring dashboard.

\* Prediction-history visualization.

\* Real-time alert notifications.

\* Advanced anomaly detection.

\* Time-series failure forecasting.

\* Streaming data processing.

\* Model retraining pipelines.

\* Additional machine-learning and deep-learning models.

\* Deployment on cloud infrastructure.



\---



\## Disclaimer



Chronos AI is an academic and experimental predictive analytics project. Model performance depends on the quality, distribution, and representativeness of the training and evaluation data. Predictions should be treated as analytical decision-support information rather than guaranteed failure outcomes.



\---



\## Project Status



\*\*Chronos AI — Active Development\*\*



\*\*Current milestone: Backend Prediction + Risk + Alert + MongoDB Integration Completed\*\*



