# Project title

*DAT 342 Data Engineering, Fall 2026. Replace this line with your name.*

One or two sentences describing what your pipeline does and what question(s) its Gold layer answers.

## Data sources

| Source | Type | Ingestion method | Link |
|--------|------|------------------|------|
| *e.g. Open-Meteo forecast API* | API | `requests`, paginated JSON | *link* |
| *e.g. County parcel records* | File (CSV) | Batch read from a Volume | *link* |
| *e.g. Inventory table in Supabase* | Database (SQL) | JDBC | *link* |

## Architecture

Describe (or diagram) how data flows from each source through Bronze, Silver, and Gold. Keep this section current as your pipeline grows: by the end of the semester it should describe the finished pipeline.

## Repository layout

```
setup_catalog.py       Creates the final_project catalog, schemas, and landing Volume
bronze/                One script per source, landing raw data into bronze
silver/                Cleaning, validation, and conformed tables
  quality_rules.yml    Your data quality rules, one section per Silver table
  quality.py           Loads and applies quality_rules.yml (no need to edit)
gold/                  Dimensional model and summary tables
eda/                   Exploratory notebook(s) on your Silver tables (Sprint 03)
PROPOSAL.md            Your Sprint 01 project proposal
```

Add folders as you need them (for example, `jobs/` for Workflow definitions in Sprint 04).

## How to run

1. Run `setup_catalog.py` once.
2. Run the Bronze scripts, then Silver, then Gold.

Update these steps as your pipeline changes. Someone who has never seen your project should be able to rebuild it from these instructions, given access to your credentials.

## Data quality

Data quality rules live in `silver/quality_rules.yml`, not in code. Each Silver script loads its table's rules and applies them with `silver/quality.py`, sending rows that fail a rule to a quarantine table. To add or change a rule, edit the YAML file. Summarize here what your rules check for and where quarantined rows end up.

## Dashboard

Add a screenshot of your Gold-layer dashboard here in Sprint 05.

## Credentials

This repository must never contain passwords, API keys, or connection strings. All credentials live in Databricks Secrets (scope `dat342`, the same scope you created in Lesson 05). List the secret *keys* your code expects here, but never their values:

| Secret key | Used by |
|------------|---------|
| *e.g. `project-api-key`* | `bronze/bronze_api.py` |
