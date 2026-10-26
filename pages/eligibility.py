"""Weighted, transparent eligibility preparation checklist."""
import streamlit as st

from services.eligibility import CHECKS, score_eligibility
from state import get_eligibility_checks, get_opportunities, set_eligibility_checks
from ui.components import page_header, status_pill


def render() -> None:
    """Render saved checks and explain the human-review readiness score."""
    page_header("Eligibility Match", "A weighted checklist helps identify evidence to gather. It does not decide donor eligibility.")
    records = get_opportunities()
    if not records:
        st.info("Add an opportunity before starting an eligibility review.")
        return
    labels = [f"{record['id']} · {record['title']}" for record in records]
    selected = st.selectbox("Opportunity", labels)
    record = records[labels.index(selected)]
    st.markdown(f"**{record['donor']}** · {record['theme']} · {record['geography']}")
    st.link_button("Review source URL", record["source"])
    saved = get_eligibility_checks(record["id"])
    checked: set[str] = set()
    for label, weight, helper in CHECKS:
        cols = st.columns([5, 1])
        with cols[0]:
            if st.checkbox(label, value=label in saved, key=f"elig_{record['id']}_{label}"):
                checked.add(label)
            st.caption(helper)
        with cols[1]:
            st.caption(f"{weight}%")
    if checked != set(saved):
        set_eligibility_checks(record["id"], list(checked))
    result = score_eligibility(checked)
    st.progress(result.score / 100, text=f"Evidence checklist · {result.score}% ({result.completed}/{result.total})")
    status_pill(result.readiness)
    st.info("A complete checklist means ready for human review only. It is not a legal or donor eligibility decision.")
