"""Streamlit entry point and grouped page router."""
import logging
import json
from hashlib import sha256

import streamlit as st

from config import APP_TITLE
from pages import approval_queue, donor_crm, eligibility, followups, knowledge_base, opportunities, overview, proposal
from state import export_state, import_state, init_state
from services.export import json_backup
from theme import apply_theme

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
LOGGER = logging.getLogger(__name__)

st.set_page_config(page_title=APP_TITLE, page_icon="🤝", layout="wide", initial_sidebar_state="expanded")
apply_theme()
init_state()

st.sidebar.markdown("### 🤝 JGVS Fundraising")
st.sidebar.caption("FUNDING WORKSPACE · DEMO")
pages = {
    "Workspace": [
        st.Page(overview.render, title="Overview", url_path="overview", icon=":material/dashboard:", default=True),
        st.Page(opportunities.render, title="Opportunity Finder", url_path="opportunities", icon=":material/search:"),
        st.Page(eligibility.render, title="Eligibility Match", url_path="eligibility", icon=":material/checklist:"),
    ],
    "Prepare": [
        st.Page(knowledge_base.render, title="Knowledge Base", url_path="knowledge-base", icon=":material/library_books:"),
        st.Page(proposal.render, title="Proposal & Budget", url_path="proposal-budget", icon=":material/description:"),
    ],
    "Manage": [
        st.Page(donor_crm.render, title="Donor CRM", url_path="donor-crm", icon=":material/group:"),
        st.Page(approval_queue.render, title="Approval Queue", url_path="approval-queue", icon=":material/rule:"),
        st.Page(followups.render, title="Follow-ups", url_path="follow-ups", icon=":material/event_upcoming:"),
    ],
}
selected_page = st.navigation(pages, position="sidebar")
st.sidebar.divider()
st.sidebar.caption("OUTREACH SAFETY")
st.sidebar.markdown("Emails are never sent automatically. Every draft requires human approval.")
with st.sidebar.expander("Session backup"):
    st.download_button("Export JSON backup", json_backup(export_state()), "jgvs_session_backup.json", "application/json")
    backup = st.file_uploader("Import JSON backup", type=["json"], key="backup_upload")
    backup_bytes = backup.getvalue() if backup else b""
    backup_digest = sha256(backup_bytes).hexdigest() if backup_bytes else ""
    if backup and backup_digest != st.session_state.get("last_backup_digest"):
        try:
            import_state(json.loads(backup_bytes))
            st.session_state["last_backup_digest"] = backup_digest
            st.toast("Backup imported.")
            st.rerun()
        except (json.JSONDecodeError, ValueError, TypeError, AttributeError) as exc:
            st.error(f"Backup could not be imported: {exc}")

nav_target = st.session_state.pop("nav_target", None)
if nav_target:
    for group in pages.values():
        for page in group:
            if page.title == nav_target:
                st.switch_page(page)

try:
    selected_page.run()
except Exception as exc:
    LOGGER.exception("Page rendering failed: %s", selected_page.title)
    st.error("This page could not be displayed. Your session data has been kept; refresh or try again.")
