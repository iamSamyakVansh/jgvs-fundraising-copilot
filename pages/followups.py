"""Follow-up calendar list and editable, approval-gated email drafts."""
from datetime import date, timedelta
from services.ids import new_id
import streamlit as st

from models import ApprovalItem
from services.export import escape_html
from state import add_approval, add_followup, get_donors, get_followups
from ui.components import page_header

TEMPLATES = {
    "Guidelines request": "Could you share the current programme guidelines and application timeline?",
    "Proposal follow-up": "I am following up on the concept note for {project}. Please let us know if additional information would be helpful.",
    "Thank you": "Thank you for taking the time to speak with us about your funding priorities.",
}


def render() -> None:
    """Create reminders and queue email text for human review only."""
    page_header("Follow-ups", "Plan donor follow-ups and prepare outreach drafts for human review.")
    donors = get_donors()
    if not donors:
        st.info("Add a donor record before planning follow-ups.")
        return
    donor_name = st.selectbox("Donor", [row["donor"] for row in donors])
    due = st.date_input("Follow-up date", date.today() + timedelta(days=7))
    template = st.selectbox("Email template", list(TEMPLATES))
    project = st.text_input("Project or opportunity", "Information Required")
    purpose_default = TEMPLATES[template].format(project=project)
    with st.form("followup_form"):
        purpose = st.text_area("Message", purpose_default)
        contact = st.text_input("Contact name", "[Donor Contact]")
        if st.form_submit_button("Save reminder and queue email draft", type="primary"):
            if due < date.today():
                st.error("Choose a current or future date for a new follow-up.")
            else:
                subject = "Follow-up on potential funding collaboration"
                body = f"Subject: {subject}\n\nDear {contact},\n\n{purpose}\n\nRegards,\nAuthorised JGVS Representative\n[Verified contact details required]"
                reminder = {"id": new_id(), "donor": donor_name, "date": due.isoformat(), "purpose": purpose}
                add_followup(reminder)
                add_approval(ApprovalItem("Follow-up email draft", donor_name, body))
                st.session_state["latest_followup_draft"] = body
                st.toast("Reminder saved and email draft queued for human approval.")
                st.rerun()
    st.subheader("Upcoming follow-ups")
    if st.session_state.get("latest_followup_draft"):
        st.caption("Latest draft · copy from the code block or review in Approval Queue")
        st.code(st.session_state["latest_followup_draft"], language=None)
    items = sorted(get_followups(), key=lambda item: item["date"])
    if not items:
        st.info("No follow-ups planned yet.")
    for item in items:
        days = (date.fromisoformat(item["date"]) - date.today()).days
        label = "Overdue" if days < 0 else "Today" if days == 0 else f"In {days} days"
        st.markdown(f"**{escape_html(item['date'])} · {escape_html(item['donor'])}** · {label}")
        st.text(item["purpose"])
    st.info("Email sending is disabled. Every outreach draft must be approved by a human first.")
