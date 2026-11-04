# Customer 360 & Churn Platform with Reverse ETL

Unifies customer data from four systems (CRM, billing, product events, support tickets), predicts churn, pushes actions back to business tools, and measures campaign uplift. All data is synthetic.

## Architecture (high level)
```
CRM + Billing + Product events + Support tickets
   -> Airflow loaders -> raw schema
   -> identity resolution -> dbt (staging -> marts)
   -> customer_features -> churn model
   -> activation schema (scores) -> Slack / CRM
```

## Team and ownership
| Person | Area | Folders |
|---|---|---|
| A | Platform, data generation, ingestion, orchestration | `infra/`, `data_gen/`, `ingestion/` |
| B | Identity resolution, dbt models, features | `identity/`, `dbt/` |
| C | Model, reverse ETL, uplift, dashboard | `ml/`, `activation/`, `analytics/` |

## Quick start
```bash
cp .env.example .env
docker compose up -d
# Airflow UI: http://localhost:8080  (admin / admin)
# Warehouse:  localhost:5433  (warehouse / warehouse, db customer360)
```
Then trigger the `smoke_test` DAG in the Airflow UI. It should succeed.

## Warehouse layers
`raw` (as ingested) -> `staging` (cleaned) -> `marts` (dbt models) -> `activation` (scores and reverse ETL output)

## Docs
- [Raw table contract](docs/raw_table_contract.md)

## Status
- [x] Week 1: repo, Docker Compose, smoke-test DAG, raw contract draft
