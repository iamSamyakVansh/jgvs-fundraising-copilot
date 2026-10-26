# JGVS Fundraising Copilot

A local Streamlit prototype for organizing funding research, eligibility evidence, proposal drafts, donor follow-ups, and human approval. All sample records are clearly illustrative; no JGVS facts are asserted as verified.

## Run locally

Use Python 3.11 and a virtual environment:

```powershell
cd jgvs_fundraising_demo
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
streamlit run app.py
```

Run the tests and lint checks with `pytest` and `ruff check .`.

## Deploy

This is a Streamlit app, so GitHub stores the source code but does not run the app itself. To publish a live version:

1. Push this project to a GitHub repository.
2. Sign in at [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub and choose **Create app**.
3. Select the repository and branch, set **Main file path** to `app.py`, then deploy.

The project includes `.streamlit/config.toml` for its light palette. No secrets are needed for the current demo. If integrations are added later, store credentials in Streamlit's app secrets and never commit `secrets.toml`.

The app has no sign-in or access control. Anyone who can access a deployed app may use it, so deploy only synthetic/demo data until authentication and production data protections are added. Session data is not a durable shared database and may reset when the app restarts.

## Structure

```text
app.py                  Streamlit entry point and grouped navigation
.streamlit/config.toml  Light Streamlit palette, UTF-8 without BOM
config.py               Enums, page names, feature flags, design tokens
theme.py                Theme injection and scoped Streamlit selectors
models.py               Typed domain dataclasses
state.py                Session initialization and typed state accessors
data/                   Illustrative seed data and SQLite repository adapter
services/               Eligibility, budget, drafts, IDs, validation, export
ui/                     Reusable escaped view components
pages/                  Overview and the seven workflow pages
tests/                  Service-level unit tests
```

## Design tokens

The palette is intentionally limited to ink `#1d1d1f`, muted `#515154`, accent `#0071e3` (hover `#0062c4`), paper `#f5f5f7`, line `#d2d2d7`, and white surfaces. Semantic state is stated in text and uses small accents only.

## Safety principles

- Emails are never sent automatically. Proposal and follow-up drafts enter the human approval queue.
- Unknown organisation facts stay marked **Information Required** until a person supplies and verifies them.
- Every opportunity retains its source URL and verification status. Seed opportunities and donors are illustrative examples, not real leads.
- Do not upload beneficiary personal data to this demo. Uploaded file previews remain session-only.
- Session-only storage is the default. Set `PERSISTENCE_ENABLED = True` in `config.py` to use the optional local SQLite adapter. This is a local demo store, not a production database.
- Use the sidebar JSON backup controls to export or restore a session.

## Replacing demo data

Update `data/seed.py` only with records reviewed against their source pages. Preserve the direct source URL, retrieval status, deadline, and verification notes. Replace each organisation `Information Required` value only after an authorized person checks the supporting JGVS document. Never infer eligibility, beneficiary totals, or outcomes from thematic similarity.

This prototype does not include authentication, durable audit controls, automated web research, cloud integrations, or production security review.
