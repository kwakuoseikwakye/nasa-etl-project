#  NASA ETL Pipeline

This project implements a complete ETL (Extract, Transform, Load) pipeline that integrates data from multiple NASA APIs, processes and enriches the data, and loads it into an AWS RDS database. The pipeline uses AWS Glue for orchestration and a FastAPI microservice hosted on AWS Lightsail for image analysis.

---

##  Features

-  Extract data from:
  - Astronomy Picture of the Day (APOD)
  - Near Earth Object Web Service (NeoWs)
  - Mars Rover Photo API
-  Normalize and clean all datasets
-  Merge datasets using date as the key
-  Enrich image records via a custom microservice
-  Load data into PostgreSQL on AWS RDS
-  Schedule and automate with AWS Glue
-  Secure, production-grade deployment

---

##  Architecture Diagram

![ETL Architecture](arch.png)

---

##  Tech Stack

- **Python** (FastAPI, requests, pandas, SQLAlchemy)
- **AWS Glue** (Python Shell jobs)
- **AWS RDS** (PostgreSQL)
- **AWS Lightsail** (Ubuntu VM for FastAPI)
- **Pillow** for basic image analysis

---

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/nasa-etl-pipeline.git
cd nasa-etl-pipeline
```

### 2. Set up Environment Variables
Create a .env file with the following:
```bash
NASA_API_KEY=nasa-api-key
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
LIGHTSAIL_SERVICE_URL=http://lightsail-ip:8000
```

### 4. Deploy Lightsail Microservice
Launch Ubuntu instance on Lightsail.
SSH into instance, clone the lightsail-image-service.
Set up Python environment and run FastAPI app with Gunicorn.
Expose port 8000 in the Lightsail firewall.