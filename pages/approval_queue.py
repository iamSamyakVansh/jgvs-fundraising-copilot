"""Human review inbox with confirmations and an audit trail."""
from datetime import datetime
from difflib import unified_diff
import streamlit as st

from config import ApprovalStatus
from services.export import escape_html
from state import audit_user, get_approvals, get_proposal_versions, persist
from ui.components import empty_state, page_header


@st.dialog("Confirm review action")
def _confirm(item_id: str, action: str) -> None:
    """Confirm an approval action and append reviewer audit data."""
    comment = st.text_area("Reviewer comment", placeholder="Optional context for the next step")
    current = next(entry for entry in get_approvals() if entry["id"] == item_id)
    st.write(f"{action} **{escape_html(current['item_type'])}**: {escape_html(current['item'])}?")
    if st.button(f"Confirm {action.lower()}", type="primary"):
        item = next(entry for entry in get_approvals() if entry["id"] == item_id)
        item["status"] = ApprovalStatus.APPROVED if action == "Approve" else ApprovalStatus.CHANGES_REQUESTED
        item["reviewer_comment"] = comment.strip()
        item["audit"].append({"who": audit_user(), "when": datetime.now().astimezone().isoformat(timespec="seconds"), "action": action, "version": str(item["version"])})
        persist("approvals")
        st.toast(f"{action} recorded in this demo session.")
        st.rerun()


def render() -> None:
    """Render pending and reviewed drafts with immutable content previews."""
    page_header("Approval Queue", "Review proposal and follow-up drafts. Nothing is sent or submitted automatically.")
    pending_tab, approved_tab, changes_tab = st.tabs(["Pending", "Approved", "Changes requested"])
    groups = [(pending_tab, ApprovalStatus.PENDING), (approved_tab, ApprovalStatus.APPROVED), (changes_tab, ApprovalStatus.CHANGES_REQUESTED)]
    approvals = get_approvals()
    for tab, status in groups:
        with tab:
            rows = [item for item in approvals if item["status"] == status]
            if not rows:
                empty_state("Nothing here yet", "Drafts appear here when submitted for human review.")
            for item in rows:
                with st.container(border=True):
                    st.markdown(f"### {escape_html(item['item'])}")
                    st.caption(f"{item['item_type']} · Version {item['version']} · Created {item['created']}")
                    if item.get("content"):
                        with st.expander("Review draft"):
                            st.markdown(item["content"])
                            st.download_button("Download reviewed draft", item["content"], f"draft-v{item['version']}.md", key="approval_download_"+item["id"])
                            versions = [version for version in get_proposal_versions() if version["title"] == item["item"] and version["version"] < item["version"]]
                            if versions:
                                previous = max(versions, key=lambda version: version["version"])
                                diff = "\n".join(unified_diff(previous["content"].splitlines(), item["content"].splitlines(), fromfile=f"v{previous['version']}", tofile=f"v{item['version']}", lineterm=""))
                                with st.expander("Changes from previous version"):
                                    st.code(diff or "No text changes.")
                    if item.get("reviewer_comment"):
                        st.info("Reviewer note: " + escape_html(item["reviewer_comment"]))
                    if status == ApprovalStatus.PENDING:
                        left, right = st.columns(2)
                        with left:
                            if st.button("Approve for next step", key="approve_"+item["id"], type="primary"):
                                _confirm(item["id"], "Approve")
                        with right:
                            if st.button("Request changes", key="changes_"+item["id"]):
                                _confirm(item["id"], "Request changes")
                    if item.get("audit"):
                        with st.expander("Audit trail"):
                            st.write(item["audit"])
    st.caption("Demo reviewer identity and audit timestamps are session-only; production needs authenticated identities and durable audit storage.")
