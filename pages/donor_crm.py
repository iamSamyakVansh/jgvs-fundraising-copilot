"""Editable donor pipeline, notes, and interaction history."""
import pandas as pd
import streamlit as st

from config import STAGES
from state import get_donors, set_donors
from ui.components import page_header, render_table, segmented_choice
from services.export import escape_html
from services.validation import valid_email


def render() -> None:
    """Render editable CRM table with search, stage filter, and contact log."""
    page_header("Donor CRM", "Keep donor context, next actions, and pipeline stages current.")
    donors = get_donors()
    search = st.text_input("Search pipeline", placeholder="Donor, opportunity, next action")
    stage_filter = segmented_choice("Stage filter", ["All", *STAGES], "All", "crm_stage_filter")
    visible = [row for row in donors if (not search or search.casefold() in str(row).casefold()) and (stage_filter == "All" or row["stage"] == stage_filter)]
    editor_frame = pd.DataFrame([{key: row.get(key, "") for key in ["donor", "contact", "email", "opportunity", "stage", "amount", "next_action", "notes", "id"]} for row in visible])
    if not editor_frame.empty:
        edited = st.data_editor(editor_frame, use_container_width=True, hide_index=True, num_rows="fixed", key="donor_editor", column_config={
            "stage": st.column_config.SelectboxColumn("Stage", options=STAGES, required=True),
            "id": None,
            "email": st.column_config.TextColumn("Email", help="Use Information Required until verified."),
            "notes": st.column_config.TextColumn("Notes", width="large"),
        })
        if st.button("Save CRM changes", type="primary"):
            edited_rows = edited.to_dict(orient="records")
            invalid_emails = [row["donor"] for row in edited_rows if row.get("email") and row["email"] != "Information Required" and not valid_email(str(row["email"]))]
            if invalid_emails:
                st.error("Enter a valid email or leave it as Information Required for: " + ", ".join(invalid_emails))
                return
            by_id = {row["id"]: row for row in donors}
            for row in edited_rows:
                if row.get("id") in by_id:
                    by_id[row["id"]].update(row)
            set_donors(donors)
            st.toast("CRM changes saved for this session.")
    else:
        st.info("No donor records match this filter.")
    st.subheader("Donor interactions")
    if donors:
        selected = st.selectbox("Donor", [row["donor"] for row in donors], key="interaction_donor")
        donor = next(row for row in donors if row["donor"] == selected)
        with st.form("interaction_form"):
            interaction = st.text_area("Add a dated note", placeholder="Record a meeting, call, or next step")
            if st.form_submit_button("Add interaction"):
                if interaction.strip():
                    donor.setdefault("interactions", []).append({"date": pd.Timestamp.today().date().isoformat(), "note": interaction.strip()})
                    set_donors(donors)
                    st.toast("Interaction added.")
        for entry in reversed(donor.get("interactions", [])):
            st.markdown(f"**{escape_html(entry['date'])}** · {escape_html(entry['note'])}")
    st.subheader("Stage overview")
    counts = pd.Series([row["stage"] for row in donors]).value_counts()
    for label, count in counts.items():
        st.markdown(f"**{escape_html(label)}** · {count}")
        st.progress(count / max(counts.max(), 1))
    st.download_button("Export CRM CSV", pd.DataFrame(donors).to_csv(index=False), "jgvs_donor_crm.csv", "text/csv")
