-- Runs once, the first time the warehouse container starts.
-- Layers: raw (as-ingested) -> staging (cleaned) -> marts (dbt models) -> activation (scores, reverse ETL output)

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS marts;
CREATE SCHEMA IF NOT EXISTS activation;

-- Audit table: every load writes one row, so reruns and failures are traceable.
CREATE TABLE IF NOT EXISTS raw._load_audit (
    load_id        BIGSERIAL PRIMARY KEY,
    source_name    TEXT        NOT NULL,
    table_name     TEXT        NOT NULL,
    rows_loaded    BIGINT      NOT NULL,
    started_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    finished_at    TIMESTAMPTZ,
    status         TEXT        NOT NULL DEFAULT 'running'  -- running | success | failed
);
