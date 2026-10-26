"""Opportunity search, source review, and CRM capture."""
from datetime import date
import pandas as pd
import streamlit as st

from config import OpportunityStatus
from models import Opportunity
from services.ids import new_id
from services.validation import valid_date, valid_url
from state import add_donor_if_missing, add_opportunity, get_opportunities
from ui.components import deadline_chip, empty_state, opportunity_card, page_header, segmented_choice, status_pill


@st.cache_data(ttl=300)
def _filtered_opportunities(records: list[dict], query: str, theme: str, geography: str, status: str, window: str, sort: str, today_iso: str) -> list[dict]:
    """Cache deterministic filtering and sorting of the opportunity register."""
    today = date.fromisoformat(today_iso)
    rows = [row for row in records if not query or query.casefold() in " ".join(str(row.get(k, "")) for k in ("donor", "theme", "title", "geography")).casefold()]
    if theme != "All themes": rows = [row for row in rows if row["theme"] == theme]
    if geography != "All locations": rows = [row for row in rows if row["geography"] == geography]
    if status != "All statuses": rows = [row for row in rows if row["status"] == status]
    if window == "Next 30 days": rows = [row for row in rows if valid_date(row.get("deadline", "")) and 0 <= (date.fromisoformat(row["deadline"]) - today).days <= 30]
    if window == "Next 90 days": rows = [row for row in rows if valid_date(row.get("deadline", "")) and 0 <= (date.fromisoformat(row["deadline"]) - today).days <= 90]
    if window == "Overdue": rows = [row for row in rows if valid_date(row.get("deadline", "")) and date.fromisoformat(row["deadline"]) < today]
    sort_keys = {"Deadline: soonest": lambda r: r["deadline"], "Donor A–Z": lambda r: r["donor"].casefold(), "Title A–Z": lambda r: r["title"].casefold()}
    return sorted(rows, key=sort_keys[sort])


def render() -> None:
    """Render filterable source-linked opportunity register."""
    page_header("Opportunity Finder", "Search the illustrative register, check its source, then add a lead to the pipeline.")
    records = get_opportunities()
    col1, col2, col3 = st.columns([2, 1, 1])
    query = col1.text_input("Search opportunities", placeholder="Donor, theme, title, or location")
    themes = ["All themes"] + sorted({row["theme"] for row in records})
    theme = col2.selectbox("Theme", themes)
    geography = col3.selectbox("Geography", ["All locations"] + sorted({row["geography"] for row in records}))
    col4, col5, col6 = st.columns(3)
    status = col4.selectbox("Verification", ["All statuses", "Needs verification", "Research complete"])
    window = col5.selectbox("Deadline", ["Any time", "Next 30 days", "Next 90 days", "Overdue"])
    sort = col6.selectbox("Sort", ["Deadline: soonest", "Donor A–Z", "Title A–Z"])
    rows = _filtered_opportunities(records, query, theme, geography, status, window, sort, date.today().isoformat())
    view = segmented_choice("View", ["Cards", "Table"], "Cards", "opportunity_view")
    left, right = st.columns([1, 4])
    with left:
        st.download_button("Export filtered CSV", pd.DataFrame(rows).to_csv(index=False), "opportunities.csv", "text/csv")
    with right:
        st.caption(f"{len(rows)} opportunity record(s). Samples remain illustrative and unverified.")

    if not rows:
        empty_state("No matches", "Adjust the search or filters to see more opportunities.")
    elif view == "Table":
        table_rows = [{**row, "source": row["source"] if valid_url(row.get("source", "")) else "Invalid source URL — verify"} for row in rows]
        st.dataframe(pd.DataFrame(table_rows), width="stretch", hide_index=True, column_config={"source": st.column_config.LinkColumn("Source URL"), "illustrative": st.column_config.CheckboxColumn("Illustrative")})
    else:
        for record in rows:
            with st.container():
                top, action = st.columns([4, 1])
                with top:
                    opportunity_card(record)
                    status_pill(deadline_chip(record["deadline"]))
                    if valid_url(record.get("source", "")):
                        st.link_button("Open source URL", record["source"])
                    else:
                        st.error("Source URL is invalid. Verify and update it before use.")
                    status_pill(f"{record['status']} · {'Illustrative' if record.get('illustrative') else 'User added'}")
                with action:
                    if st.button("Add to CRM", key="crm_" + record["id"]):
                        if add_donor_if_missing(record): st.toast("Added to donor pipeline.")
                        else: st.toast("This donor is already in the pipeline.")

    with st.expander("Add opportunity"):
        with st.form("new_opportunity"):
            donor = st.text_input("Donor name")
            title = st.text_input("Opportunity title")
            theme_new = st.text_input("Theme")
            geography_new = st.text_input("Geography")
            amount = st.text_input("Indicative amount", "Information Required")
            deadline = st.text_input("Deadline (YYYY-MM-DD)")
            eligibility = st.text_area("Eligibility notes", "Information Required")
            source = st.text_input("Source URL")
            if st.form_submit_button("Save opportunity", type="primary"):
                if not donor.strip() or not title.strip() or not valid_date(deadline) or not valid_url(source):
                    st.error("Enter donor and title, an ISO date, and a complete http(s) source URL.")
                else:
                    add_opportunity(Opportunity(donor.strip(), title.strip(), theme_new.strip() or "Information Required", geography_new.strip() or "Information Required", amount.strip() or "Information Required", deadline, eligibility.strip() or "Information Required", source.strip(), OpportunityStatus.NEEDS_VERIFICATION, id=new_id()))
                    st.toast("Opportunity saved with Needs verification status.")
                    st.rerun()
