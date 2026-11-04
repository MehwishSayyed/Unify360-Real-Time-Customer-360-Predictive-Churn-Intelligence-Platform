# Raw Table Contract (v0.1, DRAFT for review by B and C)

Owner: Person A. Changes to this file need a PR and a tag to B and C.

**Rules for the raw layer**
- Raw = data as it arrived. No cleaning here. Messy keys are intentional.
- Every table has `_loaded_at` (when we loaded it) and `_source_system`.
- Loads are idempotent: rerunning never creates duplicate rows.
- `true_customer_id` is NOT in any raw table. It lives only in `raw.ground_truth` for measuring match quality (B uses it for evaluation only, never as a feature).

## Schema: `raw`

### raw.crm_customers  (system: CRM)
| column | type | notes |
|---|---|---|
| crm_id | TEXT PK | CRM's own ID, e.g. `CRM-000123` |
| full_name | TEXT | may have typos, casing, nicknames |
| email | TEXT | casing varies, some nulls |
| phone | TEXT | mixed formats: `+91 98765 43210`, `098765-43210`, etc. |
| city | TEXT | |
| signup_date | DATE | |
| plan | TEXT | basic / standard / premium |
| created_at | TIMESTAMPTZ | |
| _loaded_at, _source_system | | |

### raw.billing_accounts  (system: Billing)
| column | type | notes |
|---|---|---|
| billing_id | TEXT PK | e.g. `BIL-000456` |
| account_holder_name | TEXT | not always identical to CRM name |
| billing_email | TEXT | may differ from CRM email |
| billing_phone | TEXT | |
| monthly_charge | NUMERIC(10,2) | |
| payment_status | TEXT | paid / failed / refunded |
| payment_date | DATE | |
| _loaded_at, _source_system | | |

*Note: one customer can have many billing rows over time (monthly payments). Duplicate accounts exist on purpose.*

### raw.product_events  (system: Product)
| column | type | notes |
|---|---|---|
| event_id | TEXT PK | unique per event |
| user_email | TEXT | casing varies |
| user_phone | TEXT | often null |
| event_type | TEXT | login / feature_use / export / share |
| event_ts | TIMESTAMPTZ | |
| session_minutes | NUMERIC(6,2) | |
| _loaded_at, _source_system | | |

### raw.support_tickets  (system: Support)
| column | type | notes |
|---|---|---|
| ticket_id | TEXT PK | |
| requester_name | TEXT | |
| requester_email | TEXT | |
| requester_phone | TEXT | |
| category | TEXT | billing / technical / cancellation / other |
| priority | TEXT | low / medium / high |
| status | TEXT | open / resolved |
| opened_at | TIMESTAMPTZ | |
| resolved_at | TIMESTAMPTZ | nullable |
| _loaded_at, _source_system | | |

### raw.ground_truth  (evaluation only)
| column | type | notes |
|---|---|---|
| source_system | TEXT | crm / billing / product / support |
| source_record_id | TEXT | crm_id / billing_id / event_id / ticket_id |
| true_customer_id | TEXT | the real identity |

### raw._load_audit
Created by infra. One row per load: source, table, rows, status, timestamps.

## Contract for B -> C (agreed in week 1, owned by B)
`marts.customer_features` columns are decided by B and C, not by A. A only provides raw data.

## Open questions for B and C
1. Do you need a `churned` label in raw data, or will C derive it (e.g. no activity for 30 days / cancellation ticket)? **A's suggestion:** C derives it from a `cancelled_at` in CRM; tell me and I'll add it.
2. Is the 100K base customer volume OK for fuzzy matching speed on your laptops?
3. Any extra fields you want in raw (e.g. address, device type)?
