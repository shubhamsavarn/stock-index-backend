# Stock Index Backend

Backend service for fetching, ingesting, and building stock index data with optional Redis caching.

---

## **Table of Contents**
1. [Setup Instructions](#setup-instructions)  
2. [Redis Setup (Optional)](#redis-setup-optional)  
3. [Running Data Acquisition Jobs](#running-data-acquisition-jobs)  
4. [API Usage](#api-usage)  
5. [Database Schema](#database-schema)  
6. [Docker Setup (Optional)](#docker-setup-optional)  

---

## **1. Setup Instructions**

### Local Setup

git clone <your-repo-url>
cd stock-index-backend
pip install --upgrade pip
pip install -r requirements.txt
2. Redis Setup (Optional)-for windows
Redis is required for caching. For Windows:
Download Redis Windows release: Redis Windows Release - https://github.com/tporadowski/redis/releases
Extract to C:\Redis
cd C:\Redis
redis-server.exe
Keep Redis running while using the backend. If Redis is not running, caching will be disabled but the API still works.
3. Running Data Acquisition Jobs
Scheduled jobs are in the jobs folder:
Script	Frequency	Description
daily_update.py	Daily at 2:00 AM	Ingest daily stock prices
full_ingest_prices.py	Monthly at 3:00 AM (1st day)	Full stock price ingestion
ingest_data.py	Monthly at 3:00 AM (1st day)	Ingest metadata
uvicorn app.main:app --reload

POST http://127.0.0.1:8000/build-index?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
Example using curl:
curl -X POST "http://127.0.0.1:8000/build-index?start_date=2025-08-21&end_date=2025-09-04

5. Database Schema
SQLite database with tables:

daily_stock_prices: ticker, date, open, close, high, low, volume

index_compositions: index_name, ticker, weight, date

index_performance: index_name, date, performance

stock_metadata: ticker, name, sector, industry

6. Docker Setup (Optional)
Build and run using Docker:

Open Docker Desktop

Search for Docker Desktop in the Start menu and launch it.

Wait for it to fully start. You should see “Docker Desktop is running” in the UI.
docker-compose up 




I can also add **screenshots, badges, and GitHub workflow instructions** if you want this README to look more professional for GitHub.  
