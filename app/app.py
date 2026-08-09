import os
from pathlib import Path
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------
# Page Configuration & Light Dashboard UI Theme
# ---------------------------------------------------------
st.set_page_config(
    page_title="Accident Severity Predictor & Risk Analytics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - 100% Identical to Target Light Dashboard Design
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
    /* ============ GLOBAL LIGHT THEME ============ */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, label {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #1e293b;
    }

    .stApp {
        background: linear-gradient(135deg, #ebf0f9 0%, #e2e8f5 100%) !important;
    }

    /* Main Content Card */
    .main .block-container {
        background: #f8f9fc;
        border-radius: 28px;
        padding: 2.2rem;
        margin-top: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.04);
        max-width: 1380px;
    }

    /* ============ SIDEBAR UNIFORM COMPONENT DESIGN ============ */
    [data-testid="stSidebar"] {
        background: linear-gradient(170deg, #3d47c8 0%, #3139a2 45%, #252d87 80%, #1a2068 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.15) !important;
        padding-top: 1rem !important;
        box-shadow: 4px 0 25px rgba(0, 0, 0, 0.18) !important;
    }

    /* Sidebar default text */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #e2e8f0;
    }

    [data-testid="stSidebar"] button[kind="header"] {
        color: #ffffff !important;
    }

    /* ---- 1. Sidebar Nav Radio Pills (Uniform 46px Height & 12px Radius) ---- */
    [data-testid="stSidebar"] .stRadio label {
        margin-bottom: 0.6rem !important;
    }

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        gap: 0.5rem !important;
    }

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.10) !important;
        height: 46px !important;
        min-height: 46px !important;
        max-height: 46px !important;
        padding: 0 1.1rem !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        display: flex !important;
        align-items: center !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        margin: 0 !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.22) !important;
        color: #ffffff !important;
        border-color: rgba(255, 255, 255, 0.30) !important;
        transform: translateX(4px) !important;
    }

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {
        background: #e5ebf5 !important;
        border-radius: 12px !important;
        border-color: #cbd5e1 !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25) !important;
    }

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] *,
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] p,
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] span {
        color: #1e293b !important;
        font-weight: 800 !important;
        font-size: 0.92rem !important;
    }

    /* ---- 2. Sidebar Selectbox Controls (Uniform 46px Height & 12px Radius) ---- */
    [data-testid="stSidebar"] [data-testid="stSelectbox"] {
        --text-color: #000000 !important;
        margin-bottom: 0.5rem !important;
    }

    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"],
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background-color: #e5ebf5 !important;
        background: #e5ebf5 !important;
        border-radius: 12px !important;
        border: 2px solid #cbd5e1 !important;
        transition: all 0.2s ease !important;
        height: 46px !important;
        min-height: 46px !important;
        max-height: 46px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
    }

    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"]:hover,
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"]:hover {
        border-color: #4f46e5 !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.15) !important;
    }

    /* Selected Option & Input Text */
    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] *,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] div,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] span,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] p,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] input,
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] *,
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div,
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span,
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] p,
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] input,
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[class*="ValueContainer"] *,
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[class*="singleValue"] *,
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[class*="placeholder"] * {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        background-color: transparent !important;
        font-weight: 800 !important;
        font-size: 0.92rem !important;
        opacity: 1 !important;
    }

    /* Dropdown Arrow Icon */
    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] svg,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] svg path,
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] svg,
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] svg path {
        fill: #000000 !important;
        stroke: #000000 !important;
        color: #000000 !important;
        opacity: 1 !important;
    }

    /* Sidebar Dropdown Menu Popup when clicked */
    [data-baseweb="popover"],
    [data-baseweb="popover"] *,
    [data-baseweb="menu"],
    [data-baseweb="menu"] * {
        background-color: #e5ebf5 !important;
        background: #e5ebf5 !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        opacity: 1 !important;
    }

    [data-baseweb="menu"] li,
    [data-baseweb="popover"] li {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 700 !important;
    }

    [data-baseweb="menu"] li:hover,
    [data-baseweb="popover"] li:hover {
        background-color: #e0e7ff !important;
        background: #e0e7ff !important;
        color: #4338ca !important;
        -webkit-text-fill-color: #4338ca !important;
    }

    [data-baseweb="menu"] li[aria-selected="true"],
    [data-baseweb="popover"] li[aria-selected="true"] {
        background-color: #4f46e5 !important;
        background: #4f46e5 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-weight: 800 !important;
    }

    /* Sidebar Filter Section Label (Above selectbox) */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"],
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSelectbox label p,
    [data-testid="stSidebar"] .stSelectbox label span {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        opacity: 1 !important;
        margin-bottom: 0.3rem !important;
    }

    /* ============ TOP BANNER ============ */
    .top-search-pill {
        background: #ffffff;
        border-radius: 20px;
        padding: 0.4rem 1rem;
        font-size: 0.85rem;
        font-weight: 600;
        color: #4b5563;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        border: 1px solid #e5e7eb;
    }

    /* ============ HERO CARD (Matching Gradient Effect) ============ */
    .hero-coral-card {
        background: linear-gradient(135deg, #3d47c8 0%, #3139a2 60%, #222982 100%);
        border-radius: 24px;
        padding: 1.8rem;
        color: #ffffff;
        box-shadow: 0 14px 30px rgba(49, 57, 162, 0.3);
        position: relative;
    }

    .hero-coral-card .card-title {
        font-size: 0.95rem;
        font-weight: 600;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .hero-coral-card .card-metric {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0.4rem 0 1.2rem 0;
        letter-spacing: -0.03em;
    }

    .hero-coral-submetrics {
        display: flex;
        gap: 1.5rem;
        font-size: 0.88rem;
        font-weight: 600;
        border-top: 1px solid rgba(255, 255, 255, 0.25);
        padding-top: 1rem;
    }

    /* ============ WHITE CARDS ============ */
    .white-card {
        background: #eef2f6;
        border-radius: 24px;
        padding: 1.6rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
        border: 1px solid #d1d5db;
    }

    /* ============ METRIC PILL BOXES ============ */
    .pink-pill-box {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: #eef2f6;
        border-radius: 22px;
        padding: 1rem 1.4rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
        border: 1px solid #d1d5db;
    }

    .pink-pill-badge {
        background: #eef0ff;
        color: #5a67d8;
        font-weight: 800;
        font-size: 1.25rem;
        padding: 0.55rem 1.1rem;
        border-radius: 16px;
    }

    .pink-pill-label {
        font-weight: 700;
        color: #1e293b;
        font-size: 1rem;
    }

    /* ============ PROFESSIONAL BUTTONS & FORM SUBMIT BUTTON ============ */
    .stButton > button,
    [data-testid="stFormSubmitButton"] > button,
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.03em !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 16px !important;
        padding: 0.85rem 2.2rem !important;
        box-shadow: 0 8px 25px rgba(49, 46, 129, 0.35) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        width: 100% !important;
        text-transform: uppercase !important;
        margin-top: 0.5rem !important;
    }

    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] > button:hover,
    div[data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(135deg, #312e81 0%, #4338ca 50%, #4f46e5 100%) !important;
        box-shadow: 0 12px 30px rgba(79, 70, 229, 0.5) !important;
        transform: translateY(-2px) !important;
        color: #ffffff !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
    }

    .stButton > button:active,
    [data-testid="stFormSubmitButton"] > button:active,
    div[data-testid="stFormSubmitButton"] button:active {
        transform: translateY(0) !important;
        box-shadow: 0 4px 14px rgba(49, 46, 129, 0.3) !important;
    }

    .stButton > button p,
    [data-testid="stFormSubmitButton"] > button p,
    div[data-testid="stFormSubmitButton"] button p {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
    }

    /* ============ FORMS & MAIN-AREA INPUTS ============ */
    [data-testid="stForm"] {
        background: #eef2f6;
        border-radius: 24px;
        padding: 2rem;
        border: 1px solid #d1d5db;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    }

    .stSelectbox div[data-baseweb="select"] > div,
    [data-testid="stForm"] .stSelectbox div[data-baseweb="select"] > div {
        background-color: #e5ebf5 !important;
        background: #e5ebf5 !important;
        border-radius: 14px !important;
        border: 1.5px solid #cbd5e1 !important;
        color: #000000 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
    }

    .stSelectbox div[data-baseweb="select"] > div *,
    [data-testid="stForm"] .stSelectbox div[data-baseweb="select"] > div * {
        color: #000000 !important;
        font-weight: 700 !important;
    }

    .stNumberInput div[data-baseweb="input"] {
        background-color: #e5ebf5 !important;
        background: #e5ebf5 !important;
        border-radius: 14px !important;
        border: 1.5px solid #cbd5e1 !important;
        color: #000000 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
    }

    .stNumberInput div[data-baseweb="input"] input {
        color: #000000 !important;
        font-weight: 700 !important;
    }

    /* ============ ICON BOXES ============ */
    .icon-box {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        background-color: #eef0ff;
        border: 1.5px solid #5a67d8;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
        flex-shrink: 0;
    }

    .icon-box-lg {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        background-color: #eef0ff;
        border: 2px solid #5a67d8;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin-bottom: 0.6rem;
    }

    /* ============ SECTION HEADERS ============ */
    .section-header {
        font-size: 1.4rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        letter-spacing: -0.02em;
    }

    .sub-section-header {
        font-size: 1.05rem;
        font-weight: 700;
        color: #475569;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    /* ============ RESULT CARDS ============ */
    .result-card-slight {
        background: #ecfdf5;
        border: 2px solid #10b981;
        border-radius: 20px;
        padding: 1.5rem;
        color: #065f46;
    }
    .result-card-serious {
        background: #fffbeb;
        border: 2px solid #f59e0b;
        border-radius: 20px;
        padding: 1.5rem;
        color: #92400e;
    }
    .result-card-fatal {
        background: #fef2f2;
        border: 2px solid #ef4444;
        border-radius: 20px;
        padding: 1.5rem;
        color: #991b1b;
    }

    .result-card-slight *,
    .result-card-serious *,
    .result-card-fatal * {
        color: inherit !important;
    }

    hr {
        margin: 1.6rem 0;
        border-color: #e5e7eb;
    }

    /* ============ RESPONSIVE ============ */
    @media (max-width: 1024px) {
        .main .block-container {
            padding: 1.5rem !important;
            border-radius: 20px !important;
        }
        .hero-coral-card .card-metric {
            font-size: 2rem !important;
        }
    }

    @media (max-width: 768px) {
        .main .block-container {
            padding: 1.2rem !important;
            margin-top: 0.5rem !important;
            border-radius: 16px !important;
        }
        .hero-coral-card {
            padding: 1.2rem !important;
        }
        .hero-coral-card .card-metric {
            font-size: 1.8rem !important;
        }
        .hero-coral-submetrics {
            flex-wrap: wrap;
            gap: 0.8rem;
        }
        .white-card {
            padding: 1.2rem !important;
        }
        .pink-pill-box {
            padding: 0.8rem 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Minimal SVG Line Icons (Black Outline Style)
# ---------------------------------------------------------
def render_icon(name: str, size: int = 20, is_lg: bool = False) -> str:
    """Renders minimalist vector SVG icon with sharp black line strokes."""
    svg_map = {
        "shield": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#5a67d8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
        "compass": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#5a67d8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>',
        "sliders": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#5a67d8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg>',
        "gauge": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#5a67d8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        "user": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#5a67d8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
        "cloud": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#5a67d8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9z"/></svg>',
        "activity": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#5a67d8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
        "target": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#5a67d8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
        "chart": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#5a67d8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>',
        "pin": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#5a67d8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
        "clock": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#5a67d8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        "cpu": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#5a67d8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="15" x2="23" y2="15"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="15" x2="4" y2="15"/></svg>',
        "check": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
        "warning": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        "danger": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
        "info": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#5a67d8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'
    }

    svg_content = svg_map.get(name, "")
    box_class = "icon-box-lg" if is_lg else "icon-box"
    return f'<div class="{box_class}">{svg_content}</div>'


def apply_chart_theme(fig):
    """Applies clean professional light theme to Plotly figures."""
    fig.update_layout(
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#1e293b"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=30, l=30, r=30),
        xaxis=dict(gridcolor="#eef0f2", showline=True, linecolor="#d1d5db"),
        yaxis=dict(gridcolor="#eef0f2", showline=True, linecolor="#d1d5db")
    )
    return fig


# ---------------------------------------------------------
# Path Resolution & Resource Caching
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "Model" / "accident_severity_model.pkl"
ENCODERS_PATH = BASE_DIR / "Model" / "encoders.pkl"
DATASET_PATH = BASE_DIR / "Dataset" / "Road.csv"


@st.cache_resource
def load_ml_resources():
    """Load and cache ML model and label encoders."""
    if not MODEL_PATH.exists():
        st.error(f"Model file not found at: `{MODEL_PATH}`")
        st.stop()
    if not ENCODERS_PATH.exists():
        st.error(f"Encoders file not found at: `{ENCODERS_PATH}`")
        st.stop()
        
    model = joblib.load(MODEL_PATH)
    encoders = joblib.load(ENCODERS_PATH)
    return model, encoders


@st.cache_data
def load_dataset():
    """Load and cache accident dataset."""
    if not DATASET_PATH.exists():
        st.error(f"Dataset file not found at: `{DATASET_PATH}`")
        st.stop()
    df = pd.read_csv(DATASET_PATH)
    
    # Preprocess Time feature for temporal analytics
    df["Time_Converted"] = pd.to_datetime(df["Time"], errors="coerce")
    df["Accident_Hour"] = df["Time_Converted"].dt.hour

    def categorize_time_period(hour):
        if pd.isna(hour):
            return "Unknown"
        if 5 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 21:
            return "Evening"
        else:
            return "Night"

    df["Time_Period"] = df["Accident_Hour"].apply(categorize_time_period)
    return df


model, encoders = load_ml_resources()
raw_df = load_dataset()


# ---------------------------------------------------------
# Sidebar & Navigation (Indigo Professional Theme)
# ---------------------------------------------------------
st.sidebar.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 2.4rem; padding-left: 0.4rem; padding-top: 0.4rem;">
        <div style="background: rgba(255, 255, 255, 0.2); width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.15); backdrop-filter: blur(4px);">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
        </div>
        <span style="font-size: 1.25rem; font-weight: 800; color: #ffffff; letter-spacing: -0.01em;">Analytics</span>
    </div>
    """,
    unsafe_allow_html=True
)

nav_option = st.sidebar.radio(
    "Select Module",
    [
        "Severity Risk Predictor",
        "Accident Overview",
        "Area Risk & Hotspots",
        "Time-of-Day Analysis",
        "Model Insights & Explainability"
    ]
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.8rem; padding-left: 0.4rem;">
        {render_icon('sliders', size=16)}
        <span style="font-size: 1rem; font-weight: 700; color: #ffffff;">Dashboard Filters</span>
    </div>
    """,
    unsafe_allow_html=True
)

# Global Dashboard Filters
weather_filter = st.sidebar.selectbox(
    "Filter by Weather Condition",
    ["All"] + sorted(list(raw_df["Weather_conditions"].dropna().unique()))
)

day_filter = st.sidebar.selectbox(
    "Filter by Day of Week",
    ["All"] + list(encoders["Day_of_week"].classes_)
)

age_filter = st.sidebar.selectbox(
    "Filter by Driver Age Band",
    ["All"] + list(encoders["Age_band_of_driver"].classes_)
)

# Apply Filters to Dataset
filtered_df = raw_df.copy()
if weather_filter != "All":
    filtered_df = filtered_df[filtered_df["Weather_conditions"] == weather_filter]
if day_filter != "All":
    filtered_df = filtered_df[filtered_df["Day_of_week"] == day_filter]
if age_filter != "All":
    filtered_df = filtered_df[filtered_df["Age_band_of_driver"] == age_filter]

st.sidebar.markdown(
    """
    <div style="margin-top: 1.8rem; height: 46px; border-radius: 12px; background: rgba(255, 255, 255, 0.12); border: 1px solid rgba(255, 255, 255, 0.20); display: flex; align-items: center; justify-content: center; box-sizing: border-box;">
        <span style="font-size: 0.88rem; color: #ffffff; font-weight: 700;">System Engine: &nbsp;<b style="color: #ffffff; text-decoration: underline;">v2.4 Active</b></span>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Top Navigation / Search & Banner Row
# ---------------------------------------------------------
top_col1, top_col3 = st.columns([2.5, 1])

with top_col1:
    st.markdown(
        """
        <h1 style="margin: 0; font-size: 2.3rem; font-weight: 800; color: #111827; letter-spacing: -0.03em;">
            Accident Severity Predictor
        </h1>
        """,
        unsafe_allow_html=True
    )

with top_col3:
    st.markdown(
        """
        <div style="text-align: right;">
            <span style="background: #111217; color: white; padding: 0.65rem 1.4rem; border-radius: 30px; font-weight: 700; font-size: 0.9rem; box-shadow: 0 4px 12px rgba(17,18,23,0.2);">
                Active Engine
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

def format_encoder_label(val):
    """Formats raw encoder values for clean UI display without altering exact class strings."""
    s = str(val).strip()
    if s.lower() in ["nan", "na"]:
        return "Not Specified / Unknown"
    return s


# ---------------------------------------------------------
# Top Dashboard Card Row (100% Dynamic Matching Image Layout)
# ---------------------------------------------------------
total_count = len(filtered_df)
if total_count > 0:
    sev_counts_all = filtered_df["Accident_severity"].value_counts()
    fatal_pct = (sev_counts_all.get("Fatal injury", 0) / total_count) * 100
    serious_pct = (sev_counts_all.get("Serious Injury", 0) / total_count) * 100
    slight_pct = (sev_counts_all.get("Slight Injury", 0) / total_count) * 100
else:
    fatal_pct = serious_pct = slight_pct = 0.0

card_col1, card_col2, card_col3 = st.columns([1.3, 1.1, 1])

with card_col1:
    # Featured Hero Coral Card (Matching Top Left in Target Image)
    st.markdown(
        f"""
        <div class="hero-coral-card">
            <div class="card-title">Total Records Evaluated</div>
            <div class="card-metric">{total_count:,}</div>
            <div class="hero-coral-submetrics">
                <span>Fatal: {fatal_pct:.1f}%</span>
                <span>Serious: {serious_pct:.1f}%</span>
                <span>Slight: {slight_pct:.1f}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with card_col2:
    # Middle Donut/Summary Card (Matching Middle Card in Target Image)
    st.markdown(
        """
        <div class="white-card">
            <div style="font-size: 0.9rem; font-weight: 700; color: #6b7280; margin-bottom: 0.4rem;">Model Performance</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #111827;">84.09%</div>
            <div style="display: flex; gap: 1rem; margin-top: 1.1rem; font-size: 0.85rem; font-weight: 600;">
                <span style="color: #ff3355;">● Random Forest</span>
                <span style="color: #6b7280;">● 31 Features</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with card_col3:
    # Pink Pill Metric Boxes (Matching Top Right Pills in Target Image)
    st.markdown(
        """
        <div style="display: flex; flex-direction: column; gap: 0.8rem;">
            <div class="pink-pill-box">
                <div class="pink-pill-badge">31</div>
                <div class="pink-pill-label">Predictive Features</div>
            </div>
            <div class="pink-pill-box">
                <div class="pink-pill-badge">3</div>
                <div class="pink-pill-label">Severity Classes</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")


# =========================================================
# MODULE 1: SEVERITY PREDICTOR FORM & INFERENCE
# =========================================================
if nav_option == "Severity Risk Predictor":
    st.markdown(
        f"""
        <div class="section-header">
            {render_icon('gauge', size=20)}
            <span>Real-Time Accident Severity Risk Predictor</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write(
        "Input scenario parameters across driver, vehicle, environment, "
        "and casualty features to compute predicted accident severity risk."
    )
    
    with st.form("prediction_form"):
        st.markdown(
            f"""
            <div class="sub-section-header">
                {render_icon('user', size=18)}
                <span>1. Driver & Vehicle Profile</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        col1, col2, col3 = st.columns(3)
        
        with col1:
            time_val = st.selectbox("Time of Accident", encoders["Time"].classes_, format_func=format_encoder_label)
            day_val = st.selectbox("Day of Week", encoders["Day_of_week"].classes_, format_func=format_encoder_label)
            age_band_val = st.selectbox("Age Band of Driver", encoders["Age_band_of_driver"].classes_, format_func=format_encoder_label)
            sex_val = st.selectbox("Sex of Driver", encoders["Sex_of_driver"].classes_, format_func=format_encoder_label)
        
        with col2:
            education_val = st.selectbox("Educational Level", encoders["Educational_level"].classes_, format_func=format_encoder_label)
            driving_exp_val = st.selectbox("Driving Experience", encoders["Driving_experience"].classes_, format_func=format_encoder_label)
            vehicle_rel_val = st.selectbox("Vehicle Driver Relation", encoders["Vehicle_driver_relation"].classes_, format_func=format_encoder_label)
            vehicle_type_val = st.selectbox("Type of Vehicle", encoders["Type_of_vehicle"].classes_, format_func=format_encoder_label)
            
        with col3:
            owner_val = st.selectbox("Owner of Vehicle", encoders["Owner_of_vehicle"].classes_, format_func=format_encoder_label)
            service_yr_val = st.selectbox("Service Year of Vehicle", encoders["Service_year_of_vehicle"].classes_, format_func=format_encoder_label)
            defect_val = st.selectbox("Defect of Vehicle", encoders["Defect_of_vehicle"].classes_, format_func=format_encoder_label)

        st.markdown("---")
        st.markdown(
            f"""
            <div class="sub-section-header">
                {render_icon('cloud', size=18)}
                <span>2. Road & Environmental Conditions</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        col4, col5, col6 = st.columns(3)
        
        with col4:
            area_val = st.selectbox("Area Where Accident Occurred", encoders["Area_accident_occured"].classes_, format_func=format_encoder_label)
            lanes_val = st.selectbox("Lanes or Medians", encoders["Lanes_or_Medians"].classes_, format_func=format_encoder_label)
            road_align_val = st.selectbox("Road Alignment", encoders["Road_allignment"].classes_, format_func=format_encoder_label)
            
        with col5:
            junction_val = st.selectbox("Type of Junction", encoders["Types_of_Junction"].classes_, format_func=format_encoder_label)
            surface_type_val = st.selectbox("Road Surface Type", encoders["Road_surface_type"].classes_, format_func=format_encoder_label)
            surface_cond_val = st.selectbox("Road Surface Conditions", encoders["Road_surface_conditions"].classes_, format_func=format_encoder_label)
            
        with col6:
            light_val = st.selectbox("Light Conditions", encoders["Light_conditions"].classes_, format_func=format_encoder_label)
            weather_val = st.selectbox("Weather Conditions", encoders["Weather_conditions"].classes_, format_func=format_encoder_label)
            collision_val = st.selectbox("Type of Collision", encoders["Type_of_collision"].classes_, format_func=format_encoder_label)

        st.markdown("---")
        st.markdown(
            f"""
            <div class="sub-section-header">
                {render_icon('activity', size=18)}
                <span>3. Incident & Casualty Dynamics</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        col7, col8, col9 = st.columns(3)
        
        with col7:
            vehicles_cnt = st.number_input("Number of Vehicles Involved", min_value=1, max_value=10, value=2)
            casualties_cnt = st.number_input("Number of Casualties", min_value=1, max_value=20, value=1)
            movement_val = st.selectbox("Vehicle Movement", encoders["Vehicle_movement"].classes_, format_func=format_encoder_label)
            
        with col8:
            casualty_class_val = st.selectbox("Casualty Class", encoders["Casualty_class"].classes_, format_func=format_encoder_label)
            casualty_sex_val = st.selectbox("Sex of Casualty", encoders["Sex_of_casualty"].classes_, format_func=format_encoder_label)
            casualty_age_val = st.selectbox("Age Band of Casualty", encoders["Age_band_of_casualty"].classes_, format_func=format_encoder_label)
            casualty_sev_val = st.selectbox("Casualty Severity", encoders["Casualty_severity"].classes_, format_func=format_encoder_label)
            
        with col9:
            casualty_work_val = st.selectbox("Work of Casualty", encoders["Work_of_casuality"].classes_, format_func=format_encoder_label)
            fitness_val = st.selectbox("Fitness of Casualty", encoders["Fitness_of_casuality"].classes_, format_func=format_encoder_label)
            pedestrian_val = st.selectbox("Pedestrian Movement", encoders["Pedestrian_movement"].classes_, format_func=format_encoder_label)
            cause_val = st.selectbox("Cause of Accident", encoders["Cause_of_accident"].classes_, format_func=format_encoder_label)

        submit_button = st.form_submit_button("⚡ Run Severity Risk Assessment", use_container_width=True)

    if submit_button:
        # Build encoded feature input vector
        encoded_data = [[
            encoders["Time"].transform([time_val])[0],
            encoders["Day_of_week"].transform([day_val])[0],
            encoders["Age_band_of_driver"].transform([age_band_val])[0],
            encoders["Sex_of_driver"].transform([sex_val])[0],
            encoders["Educational_level"].transform([education_val])[0],
            encoders["Vehicle_driver_relation"].transform([vehicle_rel_val])[0],
            encoders["Driving_experience"].transform([driving_exp_val])[0],
            encoders["Type_of_vehicle"].transform([vehicle_type_val])[0],
            encoders["Owner_of_vehicle"].transform([owner_val])[0],
            encoders["Service_year_of_vehicle"].transform([service_yr_val])[0],
            encoders["Defect_of_vehicle"].transform([defect_val])[0],
            encoders["Area_accident_occured"].transform([area_val])[0],
            encoders["Lanes_or_Medians"].transform([lanes_val])[0],
            encoders["Road_allignment"].transform([road_align_val])[0],
            encoders["Types_of_Junction"].transform([junction_val])[0],
            encoders["Road_surface_type"].transform([surface_type_val])[0],
            encoders["Road_surface_conditions"].transform([surface_cond_val])[0],
            encoders["Light_conditions"].transform([light_val])[0],
            encoders["Weather_conditions"].transform([weather_val])[0],
            encoders["Type_of_collision"].transform([collision_val])[0],
            vehicles_cnt,
            casualties_cnt,
            encoders["Vehicle_movement"].transform([movement_val])[0],
            encoders["Casualty_class"].transform([casualty_class_val])[0],
            encoders["Sex_of_casualty"].transform([casualty_sex_val])[0],
            encoders["Age_band_of_casualty"].transform([casualty_age_val])[0],
            encoders["Casualty_severity"].transform([casualty_sev_val])[0],
            encoders["Work_of_casuality"].transform([casualty_work_val])[0],
            encoders["Fitness_of_casuality"].transform([fitness_val])[0],
            encoders["Pedestrian_movement"].transform([pedestrian_val])[0],
            encoders["Cause_of_accident"].transform([cause_val])[0]
        ]]

        feature_cols = [
            "Time", "Day_of_week", "Age_band_of_driver", "Sex_of_driver",
            "Educational_level", "Vehicle_driver_relation", "Driving_experience",
            "Type_of_vehicle", "Owner_of_vehicle", "Service_year_of_vehicle",
            "Defect_of_vehicle", "Area_accident_occured", "Lanes_or_Medians",
            "Road_allignment", "Types_of_Junction", "Road_surface_type",
            "Road_surface_conditions", "Light_conditions", "Weather_conditions",
            "Type_of_collision", "Number_of_vehicles_involved", "Number_of_casualties",
            "Vehicle_movement", "Casualty_class", "Sex_of_casualty",
            "Age_band_of_casualty", "Casualty_severity", "Work_of_casuality",
            "Fitness_of_casuality", "Pedestrian_movement", "Cause_of_accident"
        ]

        input_df = pd.DataFrame(encoded_data, columns=feature_cols)

        # Execute ML Model Inference
        raw_pred = model.predict(input_df)[0]
        raw_probs = model.predict_proba(input_df)[0]

        # Normalize Probabilities
        sum_probs = sum(raw_probs)
        norm_probs = [p / sum_probs for p in raw_probs] if sum_probs > 0 else raw_probs
        confidence_pct = norm_probs[raw_pred] * 100

        severity_map = {0: "Fatal Injury", 1: "Serious Injury", 2: "Slight Injury"}
        predicted_severity = severity_map.get(raw_pred, "Unknown")

        st.markdown("---")
        st.markdown(
            f"""
            <div class="section-header">
                {render_icon('target', size=20)}
                <span>Prediction Output & Risk Assessment</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        res_col1, res_col2 = st.columns([1, 1])

        with res_col1:
            if raw_pred == 2:  # Slight
                st.markdown(
                    f"""
                    <div class="result-card-slight">
                        {render_icon('check', size=24, is_lg=True)}
                        <h3 style="margin: 0; color: #065f46; font-size: 1.3rem;">Predicted Severity: Slight Injury</h3>
                        <h4 style="margin: 0.4rem 0; color: #047857; font-size: 1.1rem;">Confidence Score: {confidence_pct:.2f}%</h4>
                        <p style="margin: 0; opacity: 0.9; font-size: 0.92rem;">Low severity risk estimated. Standard traffic precautions recommended.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            elif raw_pred == 1:  # Serious
                st.markdown(
                    f"""
                    <div class="result-card-serious">
                        {render_icon('warning', size=24, is_lg=True)}
                        <h3 style="margin: 0; color: #92400e; font-size: 1.3rem;">Predicted Severity: Serious Injury</h3>
                        <h4 style="margin: 0.4rem 0; color: #b45309; font-size: 1.1rem;">Confidence Score: {confidence_pct:.2f}%</h4>
                        <p style="margin: 0; opacity: 0.9; font-size: 0.92rem;">Moderate to high injury risk estimated. Rapid emergency dispatch advised.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:  # Fatal
                st.markdown(
                    f"""
                    <div class="result-card-fatal">
                        {render_icon('danger', size=24, is_lg=True)}
                        <h3 style="margin: 0; color: #991b1b; font-size: 1.3rem;">Predicted Severity: Fatal Injury</h3>
                        <h4 style="margin: 0.4rem 0; color: #b91c1c; font-size: 1.1rem;">Confidence Score: {confidence_pct:.2f}%</h4>
                        <p style="margin: 0; opacity: 0.9; font-size: 0.92rem;">Critical severity risk estimated. High priority emergency response required.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with res_col2:
            # Probability Bar Chart
            prob_df = pd.DataFrame({
                "Severity Class": ["Fatal Injury", "Serious Injury", "Slight Injury"],
                "Probability (%)": [p * 100 for p in norm_probs]
            })

            fig_prob = px.bar(
                prob_df,
                x="Severity Class",
                y="Probability (%)",
                color="Severity Class",
                color_discrete_map={
                    "Fatal Injury": "#ef4444",
                    "Serious Injury": "#f59e0b",
                    "Slight Injury": "#10b981"
                },
                title="Class Probability Distribution",
                text_auto=".1f"
            )
            fig_prob = apply_chart_theme(fig_prob)
            fig_prob.update_layout(showlegend=False, height=270)
            st.plotly_chart(fig_prob, use_container_width=True)


# =========================================================
# MODULE 2: ACCIDENT OVERVIEW & DISTRIBUTION ANALYTICS
# =========================================================
elif nav_option == "Accident Overview":
    st.markdown(
        f"""
        <div class="section-header">
            {render_icon('chart', size=20)}
            <span>General Accident Distribution & Environmental Analysis</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("Overview of historical accident severity breakdown and environmental interaction.")

    if filtered_df.empty:
        st.warning("⚠️ No accident records match the currently selected sidebar filter criteria. Please adjust your filters.")
    else:
        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader("Accident Severity Distribution")
            sev_counts = filtered_df["Accident_severity"].value_counts().reset_index()
            sev_counts.columns = ["Accident_severity", "Count"]

            fig_sev = px.bar(
                sev_counts,
                x="Accident_severity",
                y="Count",
                color="Accident_severity",
                color_discrete_map={
                    "Fatal injury": "#ef4444",
                    "Serious Injury": "#f59e0b",
                    "Slight Injury": "#10b981"
                },
                title="Total Incidents by Severity Level",
                text="Count"
            )
            fig_sev = apply_chart_theme(fig_sev)
            st.plotly_chart(fig_sev, use_container_width=True)

        with col_b:
            st.subheader("Severity Proportion")
            fig_pie = px.pie(
                sev_counts,
                names="Accident_severity",
                values="Count",
                color="Accident_severity",
                color_discrete_map={
                    "Fatal injury": "#ef4444",
                    "Serious Injury": "#f59e0b",
                    "Slight Injury": "#10b981"
                },
                title="Percentage Share of Severity Classes",
                hole=0.45
            )
            fig_pie = apply_chart_theme(fig_pie)
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("---")
        st.subheader("Accident Severity by Weather Conditions")
        weather_sev = pd.crosstab(
            filtered_df["Weather_conditions"],
            filtered_df["Accident_severity"]
        ).reset_index()

        # Reindex columns safely
        for col in ["Fatal injury", "Serious Injury", "Slight Injury"]:
            if col not in weather_sev.columns:
                weather_sev[col] = 0

        fig_weather = px.bar(
            weather_sev,
            x="Weather_conditions",
            y=["Fatal injury", "Serious Injury", "Slight Injury"],
            color_discrete_map={
                "Fatal injury": "#ef4444",
                "Serious Injury": "#f59e0b",
                "Slight Injury": "#10b981"
            },
            title="Impact of Weather Conditions on Severity",
            barmode="group"
        )
        fig_weather = apply_chart_theme(fig_weather)
        st.plotly_chart(fig_weather, use_container_width=True)


# =========================================================
# MODULE 3: AREA-BASED RISK & HOTSPOT ANALYSIS
# =========================================================
elif nav_option == "Area Risk & Hotspots":
    st.markdown(
        f"""
        <div class="section-header">
            {render_icon('pin', size=20)}
            <span>Area-Based Risk & Hotspot Identification</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("Spatial analysis identifying locations with high accident density and severe incident risk.")

    if filtered_df.empty:
        st.warning("⚠️ No accident records match the currently selected sidebar filter criteria. Please adjust your filters.")
    else:
        area_sev = pd.crosstab(
            filtered_df["Area_accident_occured"],
            filtered_df["Accident_severity"]
        ).reset_index()

        for col in ["Fatal injury", "Serious Injury", "Slight Injury"]:
            if col not in area_sev.columns:
                area_sev[col] = 0

        # Calculate Weighted Risk Score: Fatal (3x) + Serious (2x) + Slight (1x)
        area_sev["Risk_Score"] = (
            area_sev["Fatal injury"] * 3 +
            area_sev["Serious Injury"] * 2 +
            area_sev["Slight Injury"] * 1
        )
        area_sev_sorted = area_sev.sort_values(by="Risk_Score", ascending=False)

        col_r1, col_r2 = st.columns([1.2, 1])

        with col_r1:
            st.subheader("Location-Based Risk Score Ranking")
            fig_risk = px.bar(
                area_sev_sorted,
                x="Area_accident_occured",
                y="Risk_Score",
                color="Risk_Score",
                color_continuous_scale="Reds",
                title="Calculated Risk Score by Area",
                text="Risk_Score"
            )
            fig_risk = apply_chart_theme(fig_risk)
            fig_risk.update_layout(xaxis_title="Area", yaxis_title="Weighted Risk Score")
            st.plotly_chart(fig_risk, use_container_width=True)

        with col_r2:
            st.subheader("Top 5 Highest Risk Areas")
            top_5_areas = area_sev_sorted.head(5)
            st.dataframe(
                top_5_areas[[
                    "Area_accident_occured", "Fatal injury",
                    "Serious Injury", "Slight Injury", "Risk_Score"
                ]],
                use_container_width=True
            )

            if not area_sev_sorted.empty:
                highest_area = area_sev_sorted.iloc[0]["Area_accident_occured"]
                highest_score = area_sev_sorted.iloc[0]["Risk_Score"]
                st.error(
                    f"**Highest Risk Area Detected**: **{highest_area}** "
                    f"with a Risk Score of **{highest_score:,}**."
                )


# =========================================================
# MODULE 4: TIME-OF-DAY ACCIDENT ANALYSIS
# =========================================================
elif nav_option == "Time-of-Day Analysis":
    st.markdown(
        f"""
        <div class="section-header">
            {render_icon('clock', size=20)}
            <span>Time-of-Day & Temporal Accident Risk</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("Temporal profiling showing hourly trends and period-of-day risk distributions.")

    if filtered_df.empty:
        st.warning("⚠️ No accident records match the currently selected sidebar filter criteria. Please adjust your filters.")
    else:
        t_col1, t_col2 = st.columns(2)

        with t_col1:
            st.subheader("Accident Count by Period of Day")
            time_period_order = ["Morning", "Afternoon", "Evening", "Night"]
            tp_counts = (
                filtered_df["Time_Period"]
                .value_counts()
                .reindex(time_period_order, fill_value=0)
                .reset_index()
            )
            tp_counts.columns = ["Time_Period", "Accident_Count"]

            fig_tp = px.bar(
                tp_counts,
                x="Time_Period",
                y="Accident_Count",
                color="Time_Period",
                color_discrete_sequence=px.colors.qualitative.Dark2,
                title="Accident Volume by Time Window",
                text="Accident_Count"
            )
            fig_tp = apply_chart_theme(fig_tp)
            st.plotly_chart(fig_tp, use_container_width=True)

        with t_col2:
            st.subheader("Hourly Trend Analysis")
            hourly = (
                filtered_df["Accident_Hour"]
                .value_counts()
                .sort_index()
                .reset_index()
            )
            hourly.columns = ["Hour", "Accident_Count"]

            fig_hourly = px.line(
                hourly,
                x="Hour",
                y="Accident_Count",
                markers=True,
                title="Accident Frequency Throughout the Day (24 Hrs)"
            )
            fig_hourly = apply_chart_theme(fig_hourly)
            fig_hourly.update_layout(
                xaxis=dict(tickmode="linear", dtick=1),
                xaxis_title="Hour of the Day (0 - 23)",
                yaxis_title="Total Incidents"
            )
            st.plotly_chart(fig_hourly, use_container_width=True)

        st.markdown("---")
        st.subheader("Time Period vs Severity Heatmap")

        time_sev_ct = pd.crosstab(
            filtered_df["Time_Period"],
            filtered_df["Accident_severity"]
        ).reindex(time_period_order, fill_value=0)

        fig_heat = px.imshow(
            time_sev_ct,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Blues",
            title="Severity Concentration Across Time Periods"
        )
        fig_heat = apply_chart_theme(fig_heat)
        st.plotly_chart(fig_heat, use_container_width=True)


# =========================================================
# MODULE 5: MODEL INSIGHTS & EXPLAINABILITY (XAI)
# =========================================================
elif nav_option == "Model Insights & Explainability":
    st.markdown(
        f"""
        <div class="section-header">
            {render_icon('cpu', size=20)}
            <span>Machine Learning Model Insights & Feature Importance</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("Understand which parameters drive the Random Forest model's predictions.")

    feature_names = [
        "Time", "Day_of_week", "Age_band_of_driver", "Sex_of_driver",
        "Educational_level", "Vehicle_driver_relation", "Driving_experience",
        "Type_of_vehicle", "Owner_of_vehicle", "Service_year_of_vehicle",
        "Defect_of_vehicle", "Area_accident_occured", "Lanes_or_Medians",
        "Road_allignment", "Types_of_Junction", "Road_surface_type",
        "Road_surface_conditions", "Light_conditions", "Weather_conditions",
        "Type_of_collision", "Number_of_vehicles_involved", "Number_of_casualties",
        "Vehicle_movement", "Casualty_class", "Sex_of_casualty",
        "Age_band_of_casualty", "Casualty_severity", "Work_of_casuality",
        "Fitness_of_casuality", "Pedestrian_movement", "Cause_of_accident"
    ]

    importances = model.feature_importances_
    fi_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances,
        "Importance (%)": importances * 100
    }).sort_values(by="Importance", ascending=False).reset_index(drop=True)

    col_f1, col_f2 = st.columns([1.3, 1])

    with col_f1:
        st.subheader("Top 10 Most Influential Features")
        top_10 = fi_df.head(10).sort_values(by="Importance", ascending=True)

        fig_fi = px.bar(
            top_10,
            x="Importance",
            y="Feature",
            orientation="h",
            color="Importance",
            color_continuous_scale="Blues",
            title="Top 10 Feature Gini Importance Scores",
            text_auto=".3f"
        )
        fig_fi = apply_chart_theme(fig_fi)
        st.plotly_chart(fig_fi, use_container_width=True)

    with col_f2:
        st.subheader("Top Feature Breakdown Table")
        st.dataframe(
            fi_df.head(10)[["Feature", "Importance (%)"]],
            use_container_width=True
        )

        top_feature = fi_df.iloc[0]["Feature"]
        top_pct = fi_df.iloc[0]["Importance (%)"]

        st.info(
            f"**Key Finding**: **{top_feature}** is the single most influential "
            f"predictor, contributing **{top_pct:.2f}%** to the model's decisions."
        )

    st.markdown("---")
    st.caption(
        "Feature importance values reflect Gini impurity reduction across all decision trees "
        "in the Random Forest model ensemble."
    )
