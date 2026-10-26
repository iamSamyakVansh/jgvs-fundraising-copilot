"""Overview dashboard."""
from datetime import date
import pandas as pd
import streamlit as st

from config import ApprovalStatus
from state import get_approvals, get_donors, get_opportunities, org
from services.export import escape_html
from services.validation import valid_date
from ui.components import callout, page_header, render_table, stat_card, workflow_stepper


def render() -> None:
    """Render key activity, deadlines, and next steps."""
    opportunities = get_opportunities()
    donors = get_donors()
    approvals = get_approvals()
    upcoming = sorted((row for row in opportunities if row.get("deadline")), key=lambda row: row["deadline"])
    next_deadline = upcoming[0] if upcoming else None
    pending = [item for item in approvals if item["status"] == ApprovalStatus.PENDING]
    profile = org()
    missing = [label.replace("_", " ") for label in ("registration", "tax_status", "csr1", "annual_budget", "beneficiaries") if getattr(profile, label) == "Information Required"]

    st.markdown('<div class="page-eyebrow">JGVS · FUNDING WORKSPACE</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Good work deserves<br>a clear path to funding.</div>', unsafe_allow_html=True)
    st.markdown('<p class="hero-copy">Discover opportunities, shape proposals, and keep donor relationships moving in one considered workspace.</p>', unsafe_allow_html=True)
    actions = st.columns([1.3, 1.35, 2.35])
    with actions[0]:
        if st.button("Explore opportunities →", type="primary", use_container_width=True):
            st.session_state["nav_target"] = "Opportunity Finder"
            st.rerun()
    with actions[1]:
        if st.button("Open donor pipeline →", use_container_width=True):
            st.session_state["nav_target"] = "Donor CRM"
            st.rerun()

    st.write("")
    columns = st.columns(4)
    verified_count = sum(bool(value) for value in profile.facts.values())
    for column, label, value in zip(columns, ["Tracked opportunities", "Donor records", "Awaiting review", "Verified facts"], [len(opportunities), len(donors), len(pending), f"{verified_count} checked"]):
        stat_card(column, label, value)

    st.write("")
    left, right = st.columns([1.4, 1])
    with left:
        st.subheader("Next deadline")
        if next_deadline:
            st.markdown(f'<div class="surface-card"><span class="section-label">{escape_html(next_deadline["deadline"])}</span><h3>{escape_html(next_deadline["title"])}</h3><p>{escape_html(next_deadline["donor"])} · {escape_html(next_deadline["geography"])}</p><span class="status-pill">Illustrative · verify source</span></div>', unsafe_allow_html=True)
        else:
            st.info("No opportunity deadlines are recorded.")
    with right:
        st.subheader("Attention needed")
        st.metric("Pipeline value", "Range-based")
        st.caption("Demo amounts are indicative ranges; the app does not add unverified estimates into a false total.")
        attention = 0
        if pending:
            st.markdown(f"• {len(pending)} draft(s) await human review.")
            attention += len(pending)
        if missing:
            st.markdown(f"• {len(missing)} organisation facts still show Information Required: {', '.join(missing)}.")
            attention += len(missing)
        if next_deadline and valid_date(next_deadline["deadline"]) and (date.fromisoformat(next_deadline["deadline"]) - date.today()).days <= 30:
            st.markdown(f"• Deadline approaching: {next_deadline['title']} on {next_deadline['deadline']}.")
            attention += 1
        if not attention:
            st.success("Nothing is waiting for review.")

    st.subheader("A clear four-step workflow")
    workflow_stepper(["Discover and capture sources", "Assess fit and unknowns", "Prepare proposal and budget", "Human review and follow-up"])
    st.subheader("Current pipeline")
    if donors:
        render_table(pd.DataFrame([{key: row.get(key, "") for key in ["donor", "opportunity", "stage", "amount", "next_action"]} for row in donors]))
    else:
        st.info("No donor records yet. Add one from Opportunity Finder or Donor CRM.")
    callout("Sample opportunities and donor records are illustrative. Verify each source before relying on it.", "Demo data")
