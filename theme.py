"""Design tokens and scoped Streamlit theme injection."""
import streamlit as st

from config import COLORS


def apply_theme() -> None:
    """Apply the frozen palette, type scale, spacing, and accessible controls."""
    st.markdown(f"""
    <style>
    :root {{
      --ink:{COLORS['ink']}; --muted:{COLORS['muted']}; --accent:{COLORS['accent']};
      --accent-hover:{COLORS['accent_hover']}; --paper:{COLORS['paper']}; --line:{COLORS['line']};
      --white:{COLORS['white']}; --space-1:8px; --space-2:16px; --space-3:24px; --space-4:32px;
      --radius-control:12px; --radius-card:18px; --radius-pill:999px;
    }}
    html,body {{background:var(--paper); color:var(--ink);}}
    .block-container,[data-testid="stMainBlockContainer"] {{max-width:1280px; padding:56px 32px 64px!important; overflow:visible!important;}}
    h1,h2,h3,h4 {{font-family:-apple-system,"SF Pro Display","SF Pro Text",Inter,sans-serif; color:var(--ink); letter-spacing:-.035em;}}
    h1 {{font-size:clamp(2.5rem,4vw,3rem); font-weight:650; line-height:1.08;}}
    h2 {{font-size:28px; font-weight:620;}}
    p,li,span,label {{font-family:-apple-system,"SF Pro Text",Inter,sans-serif; line-height:1.55;}}
    /* Streamlit data-testid selectors: isolated so UI changes can be updated here. */
    [data-testid="stAppViewContainer"] {{background:var(--paper); color:var(--ink);}}
    [data-testid="stHeader"] {{background:color-mix(in srgb,var(--paper) 86%,transparent); backdrop-filter:saturate(180%) blur(20px);}}
    [data-testid="stSidebar"] {{background:var(--white); border-right:1px solid var(--line);}}
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{color:var(--muted)!important;}}
    [data-testid="stMetric"] {{background:var(--white); border:1px solid var(--line); border-radius:var(--radius-card); padding:20px; box-shadow:0 1px 2px color-mix(in srgb,var(--ink) 4%,transparent),0 8px 24px color-mix(in srgb,var(--ink) 4%,transparent);}}
    [data-testid="stMetricLabel"] {{color:var(--muted)!important; font-size:13px;}}
    [data-testid="stMetricValue"] {{color:var(--ink)!important; font-size:30px; font-weight:650;}}
    [data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea,[data-testid="stNumberInput"] input,
    [data-testid="stDateInput"] input {{background:var(--white)!important; color:var(--ink)!important; border:1px solid var(--muted)!important; border-radius:var(--radius-control)!important;}}
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {{background:var(--white)!important; color:var(--ink)!important; border:1px solid var(--muted)!important; border-radius:var(--radius-control)!important;}}
    [data-testid="stFileUploaderDropzone"] {{background:var(--white)!important; border:1px dashed var(--muted)!important; border-radius:var(--radius-card)!important;}}
    [data-testid="stFileUploaderDropzone"] * {{color:var(--ink)!important;}}
    /* Stable button selectors; keep Streamlit-specific selectors isolated here. */
    [data-testid="stButton"] button,[data-testid="stFormSubmitButton"] button,[data-testid="stDownloadButton"] button {{
      min-height:48px; height:auto!important; border-radius:var(--radius-pill)!important; padding:10px 20px!important;
      font-weight:600!important; transition:background-color .18s ease,border-color .18s ease,transform .18s ease;
    }}
    [data-testid="stButton"] button p,[data-testid="stFormSubmitButton"] button p,
    [data-testid="stDownloadButton"] button p {{white-space:normal!important; overflow:visible!important; text-overflow:clip!important;}}
    [data-testid="stButton"] button:not([data-testid="stBaseButton-primary"]),
    [data-testid="stFormSubmitButton"] button:not([data-testid="stBaseButton-primary"]),
    [data-testid="stDownloadButton"] button {{background:var(--white)!important; color:var(--ink)!important; border:1px solid var(--line)!important;}}
    [data-testid="stButton"] button:not([data-testid="stBaseButton-primary"]):hover,
    [data-testid="stFormSubmitButton"] button:not([data-testid="stBaseButton-primary"]):hover,
    [data-testid="stDownloadButton"] button:hover {{background:color-mix(in srgb,var(--accent) 8%,var(--white))!important; transform:translateY(-1px);}}
    [data-testid="stButton"] button[data-testid="stBaseButton-primary"],
    [data-testid="stFormSubmitButton"] button[data-testid="stBaseButton-primary"] {{background:var(--accent)!important; color:var(--white)!important; border:1px solid var(--accent)!important;}}
    [data-testid="stButton"] button[data-testid="stBaseButton-primary"] *,
    [data-testid="stFormSubmitButton"] button[data-testid="stBaseButton-primary"] * {{color:var(--white)!important;}}
    [data-testid="stButton"] button[data-testid="stBaseButton-primary"]:hover,
    [data-testid="stFormSubmitButton"] button[data-testid="stBaseButton-primary"]:hover {{background:var(--accent-hover)!important;}}
    [data-testid="stAppViewContainer"] button:focus-visible,[data-testid="stAppViewContainer"] input:focus-visible,
    [data-testid="stAppViewContainer"] textarea:focus-visible {{outline:3px solid var(--accent)!important; outline-offset:2px;}}
    [data-testid="stAlert"] {{border-radius:var(--radius-card); background:var(--white)!important; border:1px solid var(--line)!important;}}
    [data-testid="stDataFrame"],[data-testid="stTable"] {{border:1px solid var(--line); border-radius:var(--radius-control); overflow-x:auto;}}
    @media(max-width:700px) {{[data-testid="stHorizontalBlock"] {{flex-wrap:wrap; gap:16px;}} [data-testid="column"] {{min-width:100%!important; flex:1 1 100%;}}}}
    /* End Streamlit data-testid selectors. */
    .page-eyebrow {{display:block; margin:0 0 12px; color:var(--accent); font-size:12px; line-height:1.5; font-weight:700; letter-spacing:.12em; text-transform:uppercase; overflow:visible;}}
    .hero-title {{font-size:clamp(40px,6vw,56px); line-height:1.03; font-weight:680; letter-spacing:-.05em; color:var(--ink); max-width:850px;}}
    .hero-copy {{font-size:17px; line-height:1.6; color:var(--muted); max-width:720px;}}
    .section-label {{font-size:12px; text-transform:uppercase; letter-spacing:.1em; color:var(--muted); font-weight:650;}}
    .surface-card {{background:var(--white); border:1px solid var(--line); border-radius:var(--radius-card); padding:20px; box-shadow:0 1px 2px color-mix(in srgb,var(--ink) 4%,transparent),0 8px 24px color-mix(in srgb,var(--ink) 4%,transparent); transition:transform .18s ease,box-shadow .18s ease;}}
    .surface-card:hover {{transform:translateY(-1px); box-shadow:0 2px 4px color-mix(in srgb,var(--ink) 5%,transparent),0 12px 28px color-mix(in srgb,var(--ink) 6%,transparent);}}
    .status-pill {{display:inline-block; padding:4px 10px; border-radius:var(--radius-pill); background:color-mix(in srgb,var(--accent) 10%,var(--white)); color:var(--ink); border:1px solid color-mix(in srgb,var(--accent) 24%,var(--line)); font-size:12px; font-weight:600;}}
    .fact-card {{background:var(--white); border:1px solid var(--line); border-radius:var(--radius-card); padding:16px; min-height:96px;}}
    .fact-label {{font-size:13px; color:var(--muted); margin-bottom:6px;}}
    .fact-value {{font-size:16px; font-weight:600; color:var(--ink); line-height:1.4; overflow-wrap:anywhere;}}
    .table-wrap {{overflow-x:auto; border:1px solid var(--line); border-radius:var(--radius-control); background:var(--white);}}
    table.prototype-table {{border-collapse:collapse; width:100%; min-width:760px; color:var(--ink); font-size:14px;}}
    table.prototype-table th {{background:var(--paper); color:var(--ink); font-weight:650; text-align:left;}}
    table.prototype-table th,table.prototype-table td {{padding:12px 14px; border-bottom:1px solid var(--line);}}
    table.prototype-table tr:last-child td {{border-bottom:0;}}
    @media(max-width:700px) {{.block-container,[data-testid="stMainBlockContainer"] {{padding:32px 16px 40px!important;}} .hero-title {{font-size:40px;}}}}
    @media(prefers-reduced-motion:reduce) {{*,*::before,*::after {{transition:none!important; scroll-behavior:auto!important;}}}}
    </style>
    """, unsafe_allow_html=True)
