"""Reusable, escaped Streamlit view components."""
from datetime import date
from collections.abc import Callable

import streamlit as st

from services.export import escape_html


def page_header(title: str, subtitle: str, actions: list[tuple[str, Callable[[], None]]] | None = None) -> None:
    """Render a consistent page title, helper text, and optional action buttons."""
    st.title(title)
    st.caption(subtitle)
    if actions:
        columns = st.columns(len(actions))
        for column, (label, callback) in zip(columns, actions):
            with column:
                st.button(label, on_click=callback)


def section_label(label: str) -> None:
    """Render a small uppercase section marker."""
    st.markdown(f'<div class="section-label">{escape_html(label)}</div>', unsafe_allow_html=True)


def segmented_choice(label: str, options: list[str], default: str, key: str) -> str:
    """Prefer Streamlit's segmented control with a selectbox compatibility fallback."""
    if hasattr(st, "segmented_control"):
        return st.segmented_control(label, options, default=default, key=key)
    return st.selectbox(label, options, index=options.index(default), key=key)


def status_pill(label: str) -> None:
    """Render a palette-safe text status pill."""
    st.markdown(f'<span class="status-pill">{escape_html(label)}</span>', unsafe_allow_html=True)


def fact_card(label: str, value: str) -> None:
    """Render a profile fact without truncating unknown values."""
    st.markdown(f'<div class="fact-card"><div class="fact-label">{escape_html(label)}</div><div class="fact-value">{escape_html(value)}</div></div>', unsafe_allow_html=True)


def stat_card(column, label: str, value: object, delta: str | None = None) -> None:
    """Render a consistent Streamlit metric card."""
    column.metric(label, value, delta=delta)


def opportunity_card(record: dict) -> None:
    """Render escaped opportunity details; callers provide source actions separately."""
    st.markdown(
        f'<div class="surface-card"><h3>{escape_html(record["title"])}</h3>'
        f'<p><strong>{escape_html(record["donor"])}</strong> · {escape_html(record["theme"])} · {escape_html(record["geography"])}</p>'
        f'<p>Indicative amount: {escape_html(record["amount"])} · {escape_html(record["deadline"])}</p>'
        f'<p>{escape_html(record["eligibility"])}</p></div>', unsafe_allow_html=True
    )


def empty_state(title: str, helper: str, icon: str = "○") -> None:
    """Show a compact empty state with a helpful next step."""
    st.markdown(f'<div class="surface-card"><span class="section-label">{escape_html(icon)}</span><br><strong>{escape_html(title)}</strong><br><span>{escape_html(helper)}</span></div>', unsafe_allow_html=True)


def callout(message: str, label: str = "Note") -> None:
    """Render a neutral, text-labeled callout on a white surface."""
    st.markdown(f'<div class="surface-card"><span class="section-label">{escape_html(label)}</span><p>{escape_html(message)}</p></div>', unsafe_allow_html=True)


def deadline_chip(deadline: str) -> str:
    """Return a small deadline label with days remaining."""
    try:
        days = (date.fromisoformat(deadline) - date.today()).days
        urgency = "Overdue" if days < 0 else "Due today" if days == 0 else f"{days} days left"
    except ValueError:
        urgency = "Date needs verification"
    return f"{deadline} · {urgency}"


def render_table(frame) -> None:
    """Render a responsive, escaped HTML table with predictable light colors."""
    st.markdown('<div class="table-wrap">' + frame.to_html(index=False, escape=True, classes="prototype-table", border=0) + "</div>", unsafe_allow_html=True)


def workflow_stepper(labels: list[str]) -> None:
    """Render a compact four-step workflow."""
    cols = st.columns(len(labels))
    for index, (column, label) in enumerate(zip(cols, labels), start=1):
        with column:
            st.markdown(f'<div class="surface-card"><span class="section-label">STEP {index:02}</span><p><strong>{escape_html(label)}</strong></p></div>', unsafe_allow_html=True)
