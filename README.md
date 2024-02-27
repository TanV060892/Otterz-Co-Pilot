# Otterz Co-Pilot
REST APIs for a bookkeeping product using FastAPI and MongoDB, integrating third-party services like Plaid and QuickBooks. The APIs included role-based service authorization for secure access control 

# Pre-requisites

- Install [Python] version 3.10.0

# Getting started

- Clone the repository

```
git clone https://github.com/TanV060892/Otterz-Co-Pilot.git
```

- Install dependencies

```
pip install -r requirements.txt
```

- Build and run the project

```
On Windows :
python -m venv venv
.\venv\Scripts\activate
uvicorn main:app --reload
```


- Health Check

  Endpoint : http://localhost:8000/
