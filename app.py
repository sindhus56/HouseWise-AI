import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="HouseWise AI",
    page_icon="🏠",
    layout="centered"
)


# =========================================================
# PREMIUM UI / CSS
# =========================================================

st.markdown(
"""
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

body {
    background:
        radial-gradient(circle at 10% 15%, rgba(255, 190, 240, 0.55), transparent 28%),
        radial-gradient(circle at 90% 20%, rgba(100, 200, 255, 0.50), transparent 30%),
        radial-gradient(circle at 20% 85%, rgba(190, 150, 255, 0.45), transparent 30%),
        radial-gradient(circle at 85% 85%, rgba(80, 170, 255, 0.45), transparent 30%),
        linear-gradient(135deg, #d9d5ff 0%, #eee7ff 45%, #d7edff 100%);

    background-attachment: fixed;
    background-size: cover;
    min-height: 100vh;
}

body::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: -1;

    background:
        radial-gradient(circle at 8% 12%, rgba(255, 255, 255, 0.8) 0 3px, transparent 4px),
        radial-gradient(circle at 92% 30%, rgba(255, 255, 255, 0.7) 0 3px, transparent 4px),
        radial-gradient(circle at 15% 75%, rgba(255, 255, 255, 0.65) 0 2px, transparent 3px),
        radial-gradient(circle at 82% 82%, rgba(255, 255, 255, 0.7) 0 3px, transparent 4px);

    background-size: 280px 280px;
    opacity: 0.8;
}

.stApp {
    background: transparent;
}

.block-container {
    max-width: 1100px;
    padding-top: 4rem !important;
    padding-bottom: 2rem !important;
}

hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(
        90deg,
        transparent,
        #d8dcef,
        transparent
    ) !important;
    margin: 1.2rem 0 !important;
}


/* =========================================================
   PREMIUM HERO
   ========================================================= */

.hero-section {
    position: relative;
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 38px 40px;
    margin-bottom: 28px;
    border-radius: 24px;
    background: linear-gradient(
        135deg,
        #1e1b4b 0%,
        #3730a3 45%,
        #7c3aed 100%
    );
    color: white;
    overflow: hidden;
    box-shadow: 0 18px 40px rgba(79, 70, 229, 0.22);
}

.hero-section::before {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    right: -80px;
    top: -100px;
    border-radius: 50%;
    background: rgba(255,255,255,0.10);
}

.hero-section::after {
    content: "";
    position: absolute;
    width: 140px;
    height: 140px;
    left: -70px;
    bottom: -70px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
}

.hero-icon {
    position: relative;
    z-index: 2;
    min-width: 82px;
    height: 82px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 22px;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    font-size: 42px;
    backdrop-filter: blur(10px);
}

.hero-content {
    position: relative;
    z-index: 2;
}

.hero-badge {
    display: inline-block;
    padding: 6px 12px;
    margin-bottom: 9px;
    border-radius: 20px;
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.20);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.7px;
}

.hero-title {
    margin: 0 !important;
    padding: 0 !important;
    font-size: 42px !important;
    line-height: 1.1 !important;
    font-weight: 800 !important;
    color: white !important;
}

.hero-title span {
    color: #c4b5fd;
}

.hero-subtitle {
    margin: 7px 0 4px 0 !important;
    font-size: 19px !important;
    font-weight: 600 !important;
    color: #eef2ff !important;
}

.hero-description {
    font-size: 13px;
    color: #ddd6fe;
    max-width: 650px;
}


/* =========================================================
   SECTION TITLES
   ========================================================= */

.section-title {
    background: linear-gradient(
        90deg,
        #eef2ff,
        #f8f9ff
    );
    border-left: 4px solid #6366f1;
    border-radius: 9px;
    padding: 12px 16px;
    margin-top: 1rem;
    margin-bottom: 0.8rem;
    color: #1f2937;
    font-size: 1.1rem;
    font-weight: 750;
    box-shadow: 0 3px 12px rgba(79,70,229,0.06);
}


/* =========================================================
   INPUT BOXES
   ========================================================= */

div[data-testid="stNumberInput"] {
    margin-bottom: 0.2rem !important;
}

div[data-testid="stNumberInput"] input {
    background: #f1f4fa !important;
    border: 1px solid #e3e7f0 !important;
    border-radius: 10px !important;
    transition: all 0.2s ease;
}

div[data-testid="stNumberInput"] input:focus {
    border: 1px solid #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.12) !important;
}


/* =========================================================
   BUTTONS
   ========================================================= */

div.stButton > button {
    width: 100%;
    min-height: 48px !important;
    border-radius: 12px !important;
    font-weight: 650 !important;
    font-size: 15px !important;
    border: 1px solid #6366f1 !important;
    background: white !important;
    color: #4f46e5 !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 12px rgba(79,70,229,0.08);
}

div.stButton > button:hover {
    background: linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed
    ) !important;
    color: white !important;
    border-color: #4f46e5 !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(79,70,229,0.25);
}


/* =========================================================
   DOWNLOAD BUTTON
   ========================================================= */

div.stDownloadButton > button {
    width: 100%;
    border-radius: 10px !important;
    border: 1px solid #6366f1 !important;
    background: white !important;
    color: #4f46e5 !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

div.stDownloadButton > button:hover {
    background: #eef2ff !important;
    transform: translateY(-1px);
}


/* =========================================================
   PREMIUM PREDICTION RESULT CARD
   ========================================================= */

.prediction-card {
    background: rgba(220, 255, 240, 0.72);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);

    border: 1.5px solid rgba(52, 211, 153, 0.65);
    border-radius: 20px;

    box-shadow:
        0 10px 30px rgba(16, 185, 129, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.85);

    padding: 28px;
    margin: 20px 0;

    text-align: center;
    transition: all 0.25s ease;
}

.prediction-card:hover {
    transform: translateY(-2px);

    box-shadow:
        0 14px 35px rgba(16, 185, 129, 0.20),
        inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.prediction-card .prediction-label {
    color: #047857;
    font-weight: 700;
}

.prediction-card .prediction-price {
    color: #047857;
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1px;
    margin: 8px 0;
}

.prediction-card .prediction-description {
    color: #047857;
}


/* =========================================================
   METRICS
   ========================================================= */

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.80);
    border: 1px solid #e7e9f2;
    border-radius: 13px;
    padding: 12px 14px;
    box-shadow: 0 4px 12px rgba(31,41,55,0.05);
}

div[data-testid="stMetricLabel"] {
    color: #4b5563;
}

div[data-testid="stMetricValue"] {
    color: #303442;
}


/* =========================================================
   EXPANDERS
   ========================================================= */

div[data-testid="stExpander"] {
    border: 1px solid #dfe3ee !important;
    border-radius: 11px !important;
    background: rgba(255,255,255,0.85) !important;
    box-shadow: 0 3px 10px rgba(31,41,55,0.04);
    margin-bottom: 0.5rem;
}


/* =========================================================
   ALERTS
   ========================================================= */

div[data-testid="stAlert"] {
    border-radius: 11px !important;
}


/* =========================================================
   DATAFRAME
   ========================================================= */

div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}


/* =========================================================
   SLIDER
   ========================================================= */

div[data-testid="stSlider"] {
    padding-bottom: 0.5rem;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    text-align: center;
    padding: 24px 0 10px 0;
    color: #6b7280;
}

.footer-title {
    font-size: 18px;
    font-weight: 750;
    color: #4b5563;
}

.footer-subtitle {
    font-size: 13px;
    margin-top: 5px;
}

.footer-tech {
    font-size: 12px;
    margin-top: 8px;
    color: #9ca3af;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 700px) {

    .hero-section {
        padding: 28px 22px;
        gap: 15px;
    }

    .hero-icon {
        min-width: 62px;
        height: 62px;
        font-size: 32px;
    }

    .hero-title {
        font-size: 30px !important;
    }

    .hero-subtitle {
        font-size: 16px !important;
    }

    .hero-description {
        font-size: 12px;
    }
}

/* =========================================================
   GLASSY INPUTS & MODERN SECTION CARDS
   ========================================================= */

/* Section cards */
div[data-testid="stVerticalBlock"] > div:has(.section-title) {
    background: rgba(255, 255, 255, 0.42);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.65);
    border-radius: 18px;
    box-shadow:
        0 8px 25px rgba(76, 61, 150, 0.10),
        inset 0 1px 0 rgba(255, 255, 255, 0.75);
}

/* Input boxes */
div[data-testid="stNumberInput"] input {
    background: rgba(255, 255, 255, 0.52) !important;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.85) !important;
    border-radius: 12px !important;
    box-shadow:
        0 4px 14px rgba(76, 61, 150, 0.08),
        inset 0 1px 2px rgba(255, 255, 255, 0.8);
    transition: all 0.25s ease;
}

/* Input hover */
div[data-testid="stNumberInput"] input:hover {
    background: rgba(255, 255, 255, 0.86) !important;
    border-color: rgba(108, 92, 231, 0.35) !important;
}

/* Input focus */
div[data-testid="stNumberInput"] input:focus {
    background: rgba(255, 255, 255, 0.92) !important;
    border-color: #6c5ce7 !important;
    box-shadow:
        0 0 0 2px rgba(108, 92, 231, 0.15),
        0 6px 18px rgba(76, 61, 150, 0.12);
}

/* Number input container */
div[data-testid="stNumberInput"] {
    border-radius: 14px;
}

/* Plus / minus buttons */
div[data-testid="stNumberInput"] button {
    background: rgba(255, 255, 255, 0.65) !important;
    border: none !important;
    transition: all 0.2s ease;
}

div[data-testid="stNumberInput"] button:hover {
    background: rgba(108, 92, 231, 0.12) !important;
    color: #5b4bd8 !important;
}

/* Labels */
div[data-testid="stNumberInput"] label {
    font-weight: 600;
    color: #303044;
}

/* Small glass effect for common cards */
.glass-card {
    background: rgba(255, 255, 255, 0.42);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.65);
    border-radius: 18px;
    box-shadow:
        0 8px 25px rgba(76, 61, 150, 0.10),
        inset 0 1px 0 rgba(255, 255, 255, 0.8);
}

/* =========================================================
   PREMIUM PREDICTION HISTORY
   ========================================================= */

.history-container {
    background: rgba(255, 255, 255, 0.38);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);

    border: 1px solid rgba(255, 255, 255, 0.70);
    border-radius: 18px;

    box-shadow:
        0 8px 25px rgba(76, 61, 150, 0.10),
        inset 0 1px 0 rgba(255, 255, 255, 0.85);

    padding: 18px;
    margin-top: 20px;
}

.history-container table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    overflow: hidden;

    background: rgba(255, 255, 255, 0.38);
    border-radius: 12px;
}

.history-container th {
    background: rgba(79, 70, 229, 0.82);
    color: white;
    font-weight: 700;
    padding: 12px;
}

.history-container td {
    background: rgba(255, 255, 255, 0.32);
    color: #303044;
    padding: 11px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.45);
}

.history-container tr:hover td {
    background: rgba(255, 255, 255, 0.55);
}

/* History buttons */

.history-button {
    background: rgba(255, 255, 255, 0.42);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);

    border: 1.5px solid rgba(79, 70, 229, 0.65);
    border-radius: 12px;

    color: #4338ca;
    font-weight: 600;

    padding: 10px 18px;
    transition: all 0.25s ease;
}

.history-button:hover {
    background: rgba(79, 70, 229, 0.12);
    transform: translateY(-2px);

    box-shadow: 0 6px 18px rgba(79, 70, 229, 0.15);
}

/* =========================================================
   PREMIUM MODEL PERFORMANCE CARDS
   ========================================================= */

.performance-card {
    background: rgba(255, 255, 255, 0.48);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);

    border: 1px solid rgba(255, 255, 255, 0.75);
    border-radius: 16px;

    box-shadow:
        0 7px 22px rgba(76, 61, 150, 0.10),
        inset 0 1px 0 rgba(255, 255, 255, 0.85);

    padding: 18px;
    transition: all 0.25s ease;
}

.performance-card:hover {
    transform: translateY(-3px);

    background: rgba(255, 255, 255, 0.60);

    box-shadow:
        0 12px 28px rgba(76, 61, 150, 0.16),
        inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.performance-card .metric-label {
    color: #4b5563;
    font-size: 13px;
    font-weight: 600;
}

.performance-card .metric-value {
    color: #303044;
    font-size: 27px;
    font-weight: 700;
    margin-top: 5px;
}

/* =========================================================
   PREMIUM PROPERTY SUMMARY CARDS
   ========================================================= */

.summary-card {
    background: rgba(255, 255, 255, 0.48);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);

    border: 1px solid rgba(255, 255, 255, 0.72);
    border-radius: 16px;

    box-shadow:
        0 7px 22px rgba(76, 61, 150, 0.10),
        inset 0 1px 0 rgba(255, 255, 255, 0.85);

    padding: 18px;
    transition: all 0.25s ease;
}

.summary-card:hover {
    transform: translateY(-3px);

    background: rgba(255, 255, 255, 0.60);

    box-shadow:
        0 12px 28px rgba(76, 61, 150, 0.16),
        inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.summary-card .card-label {
    color: #4b5563;
    font-size: 14px;
    font-weight: 600;
}

.summary-card .card-value {
    color: #303044;
    font-size: 26px;
    font-weight: 700;
    margin-top: 5px;
}

/* =========================================================
   PREMIUM WHAT-IF ANALYSIS
   ========================================================= */

.whatif-card {
    background: rgba(255, 255, 255, 0.42);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);

    border: 1px solid rgba(255, 255, 255, 0.72);
    border-radius: 18px;

    box-shadow:
        0 8px 25px rgba(76, 61, 150, 0.10),
        inset 0 1px 0 rgba(255, 255, 255, 0.85);

    padding: 20px;
    margin: 15px 0;

    transition: all 0.25s ease;
}

.whatif-card:hover {
    background: rgba(255, 255, 255, 0.52);

    box-shadow:
        0 12px 30px rgba(76, 61, 150, 0.14),
        inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

/* What-If result */
.whatif-result {
    background: rgba(238, 242, 255, 0.55);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);

    border: 1px solid rgba(129, 140, 248, 0.35);
    border-radius: 16px;

    padding: 18px;
    margin-top: 15px;

    box-shadow:
        0 6px 20px rgba(76, 61, 150, 0.08);
}

/* What-If headings */
.whatif-card h3,
.whatif-card h4 {
    color: #3730a3;
}

/* =========================================================
   WEBSITE NAVIGATION
   ========================================================= */

.top-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 18px;
    margin-bottom: 22px;

    background: rgba(255, 255, 255, 0.38);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);

    border: 1px solid rgba(255, 255, 255, 0.65);
    border-radius: 16px;

    box-shadow:
        0 8px 25px rgba(76, 61, 150, 0.10),
        inset 0 1px 0 rgba(255,255,255,0.8);
}

.nav-brand {
    font-size: 18px;
    font-weight: 800;
    color: #312e81;
}

.nav-tagline {
    font-size: 11px;
    color: #64748b;
    margin-top: 2px;
}

.nav-button {
    text-align: center;
}

.nav-button button {
    border: none !important;
    background: transparent !important;
    color: #374151 !important;
    font-weight: 650 !important;
    min-height: 38px !important;
    box-shadow: none !important;
}

.nav-button button:hover {
    color: #4f46e5 !important;
    background: rgba(99,102,241,0.08) !important;
    transform: none !important;
}

.home-page {
    padding: 20px 0;
}

.home-hero {
    padding: 55px 45px;
    border-radius: 26px;

    background:
        radial-gradient(circle at 90% 10%, rgba(255,255,255,0.16), transparent 25%),
        linear-gradient(
            135deg,
            #1e1b4b 0%,
            #3730a3 48%,
            #7c3aed 100%
        );

    color: white;
    box-shadow: 0 20px 45px rgba(79,70,229,0.22);

    margin-bottom: 25px;
}

.home-badge {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 20px;

    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.22);

    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.6px;
}

.home-title {
    font-size: 48px;
    font-weight: 850;
    line-height: 1.05;
    margin-top: 18px;
}

.home-title span {
    color: #c4b5fd;
}

.home-subtitle {
    font-size: 22px;
    font-weight: 650;
    margin-top: 12px;
}

.home-description {
    font-size: 15px;
    color: #ddd6fe;
    max-width: 650px;
    margin-top: 12px;
    line-height: 1.6;
}

.feature-card {
    background: rgba(255,255,255,0.42);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);

    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 17px;

    padding: 20px;
    min-height: 120px;

    box-shadow:
        0 8px 24px rgba(76,61,150,0.09),
        inset 0 1px 0 rgba(255,255,255,0.85);
}

.feature-icon {
    font-size: 25px;
}

.feature-title {
    font-weight: 750;
    color: #312e81;
    margin-top: 7px;
}

.feature-text {
    font-size: 13px;
    color: #64748b;
    margin-top: 5px;
}

.info-page {
    background: rgba(255,255,255,0.42);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);

    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 20px;

    padding: 30px;
    box-shadow: 0 10px 28px rgba(76,61,150,0.10);
}

.info-page h1 {
    color: #312e81;
}

.info-page h3 {
    color: #4338ca;
}

.about-card,
.about-section {
    background: rgba(255, 255, 255, 0.55);
    border: 2px solid rgba(255, 255, 255, 0.9);
    border-radius: 22px;
    padding: 30px;
    margin: 20px 0;
    box-shadow: 0 8px 25px rgba(80, 70, 180, 0.08);
}

.about-card h1 {
    color: #302b7a;
    font-size: 42px;
    margin-bottom: 15px;
}

.about-card h2 {
    color: #493fd4;
    font-size: 25px;
    margin-bottom: 15px;
}

.about-card p,
.about-section p {
    color: #3f4054;
    font-size: 17px;
    line-height: 1.8;
}

.about-section h2 {
    color: #302b7a;
    font-size: 26px;
    margin-bottom: 15px;
}

.tech-card {
    background: rgba(255, 255, 255, 0.75);
    border: 1px solid rgba(90, 80, 200, 0.18);
    border-radius: 14px;
    padding: 22px 18px;
    margin-bottom: 18px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(60, 50, 150, 0.06);
    transition: all 0.2s ease;
}

.tech-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 18px rgba(60, 50, 150, 0.12);
}

.tech-name {
    color: #302b7a;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 7px;
}

.tech-desc {
    color: #77758a;
    font-size: 14px;
}

</style>
""",
unsafe_allow_html=True
)


# =====================================================
# WEBSITE NAVIGATION
# =====================================================

if "page" not in st.session_state:
    st.session_state.page = "Predict"


def go_to_page(page):
    st.session_state.page = page
    st.rerun()


nav1, nav2, nav3, nav4, nav5, nav6 = st.columns(
    [2.3, 0.9, 0.9, 0.9, 0.9, 1.2]
)

with nav1:
    st.markdown(
        """
        <div style="
            padding: 8px 0;
            font-size: 20px;
            font-weight: 800;
            color: #312e81;
        ">
            🏠 HouseWise AI
        </div>
        """,
        unsafe_allow_html=True
    )

with nav2:
    if st.button("Home", key="navbar_home", use_container_width=True):
        go_to_page("Home")

with nav3:
    if st.button("Predict", key="navbar_predict", use_container_width=True):
        go_to_page("Predict")

with nav4:
    if st.button("Insights", key="navbar_insights", use_container_width=True):
        go_to_page("Insights")

with nav5:
    if st.button("About", key="navbar_about", use_container_width=True):
        go_to_page("About")

with nav6:
    if st.button("🚀 Get Started", key="navbar_get_started", use_container_width=True):
        go_to_page("Get Started")

st.markdown("<br>", unsafe_allow_html=True)


# =====================================================
# LOAD MODEL
# =====================================================

model = joblib.load("house_price_model.pkl")


# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv("data.csv")


# =========================================================
# DATA PREPROCESSING
# =========================================================

columns_to_drop = [
    "Alley",
    "MasVnrType",
    "PoolQC",
    "Fence",
    "MiscFeature"
]

df = df.drop(
    columns=columns_to_drop,
    errors="ignore"
)


X = df.drop(
    "SalePrice",
    axis=1,
    errors="ignore"
)


# Fill numerical missing values
numeric_columns = X.select_dtypes(
    include=["int64", "float64"]
).columns

for column in numeric_columns:
    X[column] = X[column].fillna(
        X[column].median()
    )


# Fill categorical missing values
categorical_columns = X.select_dtypes(
    include=["object"]
).columns

for column in categorical_columns:
    if not X[column].mode().empty:
        X[column] = X[column].fillna(
            X[column].mode()[0]
        )


# One-hot encoding
X_processed = pd.get_dummies(
    X,
    drop_first=True
)


# Match model features
if hasattr(model, "feature_names_in_"):
    X_processed = X_processed.reindex(
        columns=model.feature_names_in_,
        fill_value=0
    )


# =========================================================
# HOME PAGE
# =========================================================

if st.session_state.page == "Home":

    st.title("🏠 HouseWise AI")

    st.subheader("Smart House Price Prediction")

    st.write(
        "Estimate residential property prices using "
        "Machine Learning and intelligent property analysis."
    )

    st.divider()

    st.markdown("## ✨ AI Powered • Machine Learning")

    st.markdown(
        """
        ### Predict House Prices with HouseWise AI

        Enter property details and get an estimated house price
        using our trained Machine Learning regression model.
        """
    )

    st.divider()

    st.markdown("### 🏡 Why use HouseWise AI?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            """
            **🎯 ML-Based Prediction**

            Uses a trained Machine Learning regression model
            to estimate house prices.
            """
        )

    with col2:
        st.info(
            """
            **📊 Data-Driven Insights**

            Explore property characteristics and
            model performance.
            """
        )

    with col3:
        st.info(
            """
            **⚡ Instant Prediction**

            Enter property details and receive an
            estimated price instantly.
            """
        )

    st.write("")

    if st.button(
        "🔮 Predict House Price →",
        use_container_width=True
    ):
        st.session_state.page = "Predict"
        st.rerun()

    st.write("")

    st.caption(
        "🏠 HouseWise AI • Python • Pandas • Scikit-learn • Streamlit"
    )

    st.stop()


elif st.session_state.page == "Get Started":

    # =====================================================
    # GET STARTED PAGE
    # =====================================================

    st.markdown(
        """
        # 🏠 Welcome to HouseWise AI

        ### Smart & Simple House Price Prediction

        Estimate the market value of a residential property
        using Machine Learning based on important property
        characteristics.
        """
    )

    st.divider()

    # =====================================================
    # HOW IT WORKS
    # =====================================================

    st.markdown("## 🚀 How HouseWise AI Works")

    st.caption(
        "Get your estimated house price in three simple steps."
    )

    step1, step2, step3 = st.columns(3)

    with step1:
        st.markdown("### 📝 1. Enter Details")
        st.write(
            "Provide property information such as living area, "
            "overall quality, bedrooms, bathrooms and garage capacity."
        )

    with step2:
        st.markdown("### 🤖 2. AI Prediction")
        st.write(
            "The trained Machine Learning regression model "
            "analyzes the property characteristics."
        )

    with step3:
        st.markdown("### 💰 3. Get Price")
        st.write(
            "Receive an estimated house price along with "
            "useful property insights."
        )

    st.divider()

    # =====================================================
    # WHAT YOU CAN PREDICT
    # =====================================================

    st.markdown("## 🏡 What You Can Use")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            **Property Details**

            - ⭐ Overall Quality
            - 📐 Living Area
            - 📅 Year Built
            - 🛏️ Bedrooms
            - 🚿 Bathrooms
            - 🚪 Total Rooms
            """
        )

    with col2:
        st.markdown(
            """
            **Supporting Features**

            - 🚗 Garage Capacity
            - 📏 Garage Area
            - 🏠 Basement Area
            - 🧱 First Floor Area
            - 🔧 Overall Condition
            """
        )

    st.divider()

    # =====================================================
    # READY TO START
    # =====================================================

    st.markdown("## 🎯 Ready to Predict?")

    st.write(
        "Enter your property details and let HouseWise AI "
        "estimate its market value."
    )

    st.markdown("")

    if st.button(
        "🔮 Start House Price Prediction",
        use_container_width=True
    ):
        go_to_page("Predict")

    st.markdown("")

    st.caption(
        "HouseWise AI • Machine Learning • Python • Scikit-learn • Streamlit"
    )

    st.stop()


elif st.session_state.page == "Insights":

    st.markdown(
        """
        <div class="info-page">
            <h1>📊 HouseWise AI Insights</h1>
            <h3>Data-driven property and model analysis</h3>
            <p>
            Explore the dataset, house-price distribution, important features,
            and performance of the trained Machine Learning model.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # DATASET OVERVIEW
    # =====================================================

    st.markdown(
        """
        <div class="section-title">
        📁 Dataset Overview
        </div>
        """,
        unsafe_allow_html=True
    )

    insight1, insight2, insight3, insight4 = st.columns(4)

    with insight1:
        st.metric(
            "🏠 Total Houses",
            f"{len(df):,}"
        )

    with insight2:
        st.metric(
            "📊 Total Features",
            f"{X.shape[1]:,}"
        )

    with insight3:
        st.metric(
            "💰 Average Price",
            f"${df['SalePrice'].mean():,.0f}"
        )

    with insight4:
        st.metric(
            "🏆 Maximum Price",
            f"${df['SalePrice'].max():,.0f}"
        )

    # =====================================================
    # MODEL PERFORMANCE
    # =====================================================

    st.markdown(
        """
        <div class="section-title">
        🤖 Model Performance
        </div>
        """,
        unsafe_allow_html=True
    )

    perf1, perf2, perf3, perf4 = st.columns(4)

    with perf1:
        st.metric("R² Score", "0.6428")

    with perf2:
        st.metric("MAE", "$20,468")

    with perf3:
        st.metric("RMSE", "$52,347")

    with perf4:
        st.metric("MSE", "2.74B")

    st.info(
        "💡 The model achieved an R² score of 0.6428, "
        "meaning it explains approximately 64.28% of the variation "
        "in house prices in the evaluation data."
    )

    # =====================================================
    # PRICE DISTRIBUTION
    # =====================================================

    st.markdown(
        """
        <div class="section-title">
        📈 House Price Distribution
        </div>
        """,
        unsafe_allow_html=True
    )

    fig_price = px.histogram(
        df,
        x="SalePrice",
        nbins=40,
        title="Distribution of House Sale Prices",
        labels={
            "SalePrice": "Sale Price"
        }
    )

    fig_price.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(
        fig_price,
        use_container_width=True
    )

    # =====================================================
    # IMPORTANT FEATURES
    # =====================================================

    st.markdown(
        """
        <div class="section-title">
        🏆 Important House Price Features
        </div>
        """,
        unsafe_allow_html=True
    )

    important_features = [
        ("Overall Quality", 0.791),
        ("Living Area", 0.709),
        ("Garage Cars", 0.640),
        ("Garage Area", 0.623),
        ("Basement Area", 0.614),
        ("First Floor Area", 0.606),
        ("Full Bathrooms", 0.561),
        ("Total Rooms", 0.534),
        ("Year Built", 0.523),
        ("Year Remodeled", 0.508)
    ]

    feature_df = pd.DataFrame(
        important_features,
        columns=["Feature", "Correlation"]
    )

    feature_df = feature_df.sort_values(
        "Correlation",
        ascending=True
    )

    fig_features = px.bar(
        feature_df,
        x="Correlation",
        y="Feature",
        orientation="h",
        title="Top Features Correlated with Sale Price",
        text="Correlation"
    )

    fig_features.update_traces(
        texttemplate="%{text:.3f}",
        textposition="outside"
    )

    fig_features.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=40, t=50, b=20),
        xaxis_title="Correlation with Sale Price",
        yaxis_title="Feature"
    )

    st.plotly_chart(
        fig_features,
        use_container_width=True
    )

    # =====================================================
    # KEY FINDINGS
    # =====================================================

    st.markdown(
        """
        <div class="section-title">
        💡 Key Findings
        </div>
        """,
        unsafe_allow_html=True
    )

    st.success(
        """
        **🏆 Overall Quality** is the strongest feature associated
        with Sale Price, with a correlation of approximately **0.791**.

        **🏠 Living Area** is also strongly associated with price,
        with a correlation of approximately **0.709**.

        **🚗 Garage capacity and garage area** show strong relationships
        with house prices.

        **🛁 Bathrooms, total rooms and house age-related features**
        also contribute to differences in property prices.
        """
    )

    st.caption(
        "HouseWise AI • Machine Learning • Data Analysis • Streamlit"
    )

    st.stop()


elif st.session_state.page == "About":
    st.markdown(
        """
        <div class="about-card">
            <h1>🏠 About HouseWise AI</h1>
            <h2>Machine learning for smarter property valuation</h2>
            <p>
                This application estimates residential property prices using a
                trained regression model, with supporting summaries, comparisons,
                and prediction history for real-world decision making.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="about-section">
            <h2>🎯 Project Objective</h2>
            <p>
                HouseWise AI is a machine learning-based application designed to
                estimate residential property prices using important property
                characteristics such as living area, overall quality, garage
                capacity, location, and other housing features.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="about-section">
            <h2>🤖 Machine Learning Model</h2>
            <p>
                The application uses a trained regression model developed using
                the House Prices dataset. Data preprocessing, feature engineering,
                categorical encoding, and model evaluation were performed before
                integrating the trained model into the application.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # TECHNOLOGIES USED
    # =====================================================

    st.markdown(
        """
        <div class="about-section">
            <h2>🛠️ Technologies Used</h2>
            <p style="margin-bottom: 25px;">
                Tools and technologies used to develop, train, evaluate,
                and deploy the HouseWise AI prediction system.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    tech_col1, tech_col2, tech_col3 = st.columns(3)

    with tech_col1:
        st.markdown(
            """
            <div class="tech-card">
                <div class="tech-name">Python</div>
                <div class="tech-desc">Core Programming</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with tech_col2:
        st.markdown(
            """
            <div class="tech-card">
                <div class="tech-name">Pandas</div>
                <div class="tech-desc">Data Processing</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with tech_col3:
        st.markdown(
            """
            <div class="tech-card">
                <div class="tech-name">NumPy</div>
                <div class="tech-desc">Numerical Computing</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    tech_col4, tech_col5, tech_col6 = st.columns(3)

    with tech_col4:
        st.markdown(
            """
            <div class="tech-card">
                <div class="tech-name">Scikit-learn</div>
                <div class="tech-desc">Machine Learning</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with tech_col5:
        st.markdown(
            """
            <div class="tech-card">
                <div class="tech-name">Matplotlib</div>
                <div class="tech-desc">Data Visualization</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with tech_col6:
        st.markdown(
            """
            <div class="tech-card">
                <div class="tech-name">Streamlit</div>
                <div class="tech-desc">Application Interface</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.stop()


# =========================================================
# HERO
# =========================================================

st.markdown(
"""
<div class="hero-section">
<div class="hero-icon">🏠</div>
<div class="hero-content">
<div class="hero-badge">✨ AI POWERED • MACHINE LEARNING</div>
<div class="hero-title">HouseWise <span>AI</span></div>
<div class="hero-subtitle">Smart House Price Prediction</div>
<div class="hero-description">Estimate residential property prices using machine learning and intelligent property analysis.</div>
</div>
</div>
""",
unsafe_allow_html=True
)


# =========================================================
# PROPERTY DETAILS
# =========================================================

st.markdown(
"""
<div class="section-title">
🏡 Property Details
</div>
""",
unsafe_allow_html=True
)
st.caption("Describe the home’s core characteristics to estimate its market value.")


col1, col2 = st.columns(2)


with col1:

    overall_qual = st.number_input(
        "Overall Quality",
        min_value=1,
        max_value=10,
        value=5,
        step=1,
        help="Rate the home’s overall finish and quality from 1 (poor) to 10 (excellent)."
    )

    gr_liv_area = st.number_input(
        "Living Area (sq ft)",
        min_value=1,
        value=1500,
        step=50,
        help="Enter the total above-ground living area in square feet for the main home."
    )

    bedrooms = st.number_input(
        "Number of Bedrooms",
        min_value=0,
        max_value=10,
        value=3,
        step=1,
        help="Enter the number of bedrooms above ground."
    )


with col2:

    year_built = st.number_input(
        "Year Built",
        min_value=1800,
        max_value=2026,
        value=2000,
        step=1,
        help="Enter the year the main structure was built."
    )

    full_bath = st.number_input(
        "Number of Full Bathrooms",
        min_value=0,
        max_value=5,
        value=2,
        step=1,
        help="Include only full bathrooms with a shower/tub and sink."
    )

    total_rooms = st.number_input(
        "Total Rooms",
        min_value=1,
        max_value=20,
        value=6,
        step=1,
        help="Count all rooms above ground, including bedrooms, living spaces, and common rooms."
    )


# =========================================================
# GARAGE & BASEMENT
# =========================================================

st.markdown(
"""
<div class="section-title">
🚗 Garage & Basement
</div>
""",
unsafe_allow_html=True
)
st.caption("Add the supporting space details that affect storage, parking, and overall property value.")


col1, col2 = st.columns(2)


with col1:

    garage_cars = st.number_input(
        "Garage Capacity (cars)",
        min_value=0,
        max_value=5,
        value=2,
        step=1,
        help="Enter how many cars the garage can fit comfortably."
    )


with col2:

    garage_area = st.number_input(
        "Garage Area (sq ft)",
        min_value=0,
        value=500,
        step=50,
        help="Enter the garage floor area in square feet."
    )


total_bsmt_sf = st.number_input(
    "Total Basement Area (sq ft)",
    min_value=0,
    value=1000,
    step=50,
    help="Enter the total finished or unfinished basement area in square feet."
)


# =========================================================
# PROPERTY CONDITION
# =========================================================

st.markdown(
"""
<div class="section-title">
🛠️ Property Condition
</div>
""",
unsafe_allow_html=True
)
st.caption("Provide the condition and layout measures that reflect the home’s upkeep and usability.")


col1, col2 = st.columns(2)


with col1:

    first_floor_sf = st.number_input(
        "First Floor Area (sq ft)",
        min_value=1,
        value=1000,
        step=50,
        help="Enter the size of the first floor in square feet."
    )


with col2:

    overall_cond = st.number_input(
        "Overall Condition",
        min_value=1,
        max_value=10,
        value=5,
        step=1,
        help="Rate the home’s general condition from 1 (poor) to 10 (excellent)."
    )


# =========================================================
# INPUT VALIDATION
# =========================================================

input_valid = True

if year_built > 2026:

    st.warning(
        "⚠️ Year Built cannot be in the future."
    )

    input_valid = False


if gr_liv_area <= 0:

    st.warning(
        "⚠️ Living Area must be greater than 0."
    )

    input_valid = False


if garage_area < 0:

    st.warning(
        "⚠️ Garage Area cannot be negative."
    )

    input_valid = False


if total_bsmt_sf < 0:

    st.warning(
        "⚠️ Basement Area cannot be negative."
    )

    input_valid = False


if first_floor_sf <= 0:

    st.warning(
        "⚠️ First Floor Area must be greater than 0."
    )

    input_valid = False


# =========================================================
# ACTION BUTTONS
# =========================================================

st.divider()


button_col1, button_col2 = st.columns(2)


with button_col1:

    predict_button = st.button(
        "🔮 Predict House Price",
        use_container_width=True
    )


with button_col2:

    reset_button = st.button(
        "🔄 Reset",
        use_container_width=True
    )


# =========================================================
# RESET
# =========================================================

if reset_button:

    st.session_state.clear()

    st.rerun()


# =========================================================
# PREDICTION
# =========================================================

if predict_button and input_valid:

    # -----------------------------------------------------
    # Create default input
    # -----------------------------------------------------

    input_data = {}

    for column in X.columns:

        if X[column].dtype == "object":

            input_data[column] = X[column].mode()[0]

        else:

            input_data[column] = X[column].median()


    input_df = pd.DataFrame(
        [input_data]
    )


    # -----------------------------------------------------
    # Replace with user values
    # -----------------------------------------------------

    input_df["OverallQual"] = overall_qual
    input_df["GrLivArea"] = gr_liv_area
    input_df["GarageCars"] = garage_cars
    input_df["GarageArea"] = garage_area
    input_df["TotalBsmtSF"] = total_bsmt_sf
    input_df["1stFlrSF"] = first_floor_sf
    input_df["YearBuilt"] = year_built
    input_df["BedroomAbvGr"] = bedrooms
    input_df["FullBath"] = full_bath
    input_df["TotRmsAbvGrd"] = total_rooms
    input_df["OverallCond"] = overall_cond


    # -----------------------------------------------------
    # Encode
    # -----------------------------------------------------

    input_processed = pd.get_dummies(
        input_df,
        drop_first=True
    )


    # -----------------------------------------------------
    # Match model's 234 features
    # -----------------------------------------------------

    input_processed = input_processed.reindex(
        columns=X_processed.columns,
        fill_value=0
    )


    # -----------------------------------------------------
    # Prediction
    # -----------------------------------------------------

    prediction = model.predict(
        input_processed
    )[0]

    st.session_state.prediction = prediction
    st.session_state.input_df = input_df.copy()


    # -----------------------------------------------------
    # Prediction history
    # -----------------------------------------------------

    if "prediction_history" not in st.session_state:

        st.session_state.prediction_history = []


    st.session_state.prediction_history.append(
        {
            "House Quality": overall_qual,
            "Living Area": gr_liv_area,
            "Bedrooms": bedrooms,
            "Bathrooms": full_bath,
            "Year Built": year_built,
            "Predicted Price": float(prediction)
        }
    )


# =========================================================
# DISPLAY RESULT
# =========================================================

if "prediction" in st.session_state:

    prediction = st.session_state.prediction

    # =====================================================
    # ESTIMATED PRICE RANGE
    # =====================================================

    lower_price = prediction * 0.90
    upper_price = prediction * 1.10

    predicted_input = st.session_state.input_df

    result_overall_qual = predicted_input["OverallQual"].iloc[0]
    result_gr_liv_area = predicted_input["GrLivArea"].iloc[0]
    result_bedrooms = predicted_input["BedroomAbvGr"].iloc[0]
    result_year_built = predicted_input["YearBuilt"].iloc[0]
    result_full_bath = predicted_input["FullBath"].iloc[0]
    result_total_rooms = predicted_input["TotRmsAbvGrd"].iloc[0]
    result_garage_cars = predicted_input["GarageCars"].iloc[0]
    result_garage_area = predicted_input["GarageArea"].iloc[0]
    result_total_bsmt_sf = predicted_input["TotalBsmtSF"].iloc[0]
    result_first_floor_sf = predicted_input["1stFlrSF"].iloc[0]
    result_overall_cond = predicted_input["OverallCond"].iloc[0]


    st.markdown(
    f"""
    <div class="prediction-card">
    <div class="prediction-label">
    🏠 Estimated House Price
    </div>
    <div class="prediction-price">
    ${prediction:,.2f}
    </div>
    <div class="prediction-description">
    Estimated using the trained Machine Learning model.
    </div>
    </div>
    """,
    unsafe_allow_html=True
    )

    # =====================================================
    # ESTIMATED PRICE RANGE
    # =====================================================

    lower_price = prediction * 0.90
    upper_price = prediction * 1.10

    st.markdown(
        f"""
        <div class="prediction-card">
            <div class="prediction-label">
                💰 Estimated Price Range
            </div>
            <div class="prediction-price">
                ${lower_price:,.0f} – ${upper_price:,.0f}
            </div>
            <div class="prediction-description">
                Approximate range based on the model prediction.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # WHY THIS PRICE?
    # =====================================================

    st.markdown(
        """
        <div class="section-title">
        🔍 Why This Price?
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Key property characteristics associated with the predicted value."
    )

    factor_col1, factor_col2, factor_col3 = st.columns(3)

    with factor_col1:
        st.metric(
            "⭐ Overall Quality",
            f"{result_overall_qual}/10"
        )

    with factor_col2:
        st.metric(
            "🏠 Living Area",
            f"{result_gr_liv_area:,.0f} sq ft"
        )

    with factor_col3:
        st.metric(
            "🚗 Garage Capacity",
            f"{result_garage_cars} cars"
        )

    st.info(
        """
        💡 **Key Price Drivers:**  
        Overall quality, living area, garage capacity, basement area,
        and property age are among the important characteristics associated
        with house prices in the training data.
        """
    )


    # =====================================================
    # PROPERTY SUMMARY
    # =====================================================

    st.markdown(
    """
    <div class="section-title">
    📊 Property Summary
    </div>
    """,
    unsafe_allow_html=True
    )


    summary_col1, summary_col2, summary_col3 = st.columns(3)


    with summary_col1:

        st.metric(
            "🏠 Living Area",
            f"{result_gr_liv_area:,.0f} sq ft"
        )

        st.metric(
            "🛏️ Bedrooms",
            result_bedrooms
        )


    with summary_col2:

        st.metric(
            "🛁 Bathrooms",
            result_full_bath
        )

        st.metric(
            "🚗 Garage",
            f"{result_garage_cars} cars"
        )


    with summary_col3:

        st.metric(
            "📅 Year Built",
            result_year_built
        )

        st.metric(
            "⭐ Quality",
            f"{result_overall_qual}/10"
        )


    # =========================================================
    # PROFESSIONAL PDF PREDICTION REPORT
    # =========================================================

    st.markdown(
        """
        <div class="section-title">
            📄 Prediction Report
        </div>
        """,
        unsafe_allow_html=True
    )

    def create_prediction_pdf():
        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=45,
            leftMargin=45,
            topMargin=45,
            bottomMargin=45
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "TitleStyle",
            parent=styles["Title"],
            fontSize=24,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#312e81"),
            spaceAfter=8
        )

        subtitle_style = ParagraphStyle(
            "SubtitleStyle",
            parent=styles["Normal"],
            fontSize=11,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#64748b"),
            spaceAfter=20
        )

        heading_style = ParagraphStyle(
            "HeadingStyle",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#312e81"),
            spaceBefore=12,
            spaceAfter=10
        )

        normal_style = ParagraphStyle(
            "NormalStyle",
            parent=styles["Normal"],
            fontSize=10,
            leading=15,
            textColor=colors.HexColor("#334155")
        )

        price_style = ParagraphStyle(
            "PriceStyle",
            parent=styles["Heading1"],
            fontSize=25,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#047857"),
            spaceBefore=8,
            spaceAfter=15
        )

        story = []

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        story.append(
            Paragraph("🏠 HouseWise AI", title_style)
        )

        story.append(
            Paragraph(
                "Smart House Price Prediction",
                subtitle_style
            )
        )

        story.append(
            Paragraph(
                "Machine Learning Powered Property Valuation",
                subtitle_style
            )
        )

        story.append(Spacer(1, 8))

        # -----------------------------------------------------
        # PREDICTION RESULT
        # -----------------------------------------------------

        story.append(
            Paragraph(
                "Estimated House Price",
                heading_style
            )
        )

        story.append(
            Paragraph(
                f"${prediction:,.2f}",
                price_style
            )
        )

        story.append(
            Paragraph(
                "Estimated using the trained Machine Learning regression model.",
                subtitle_style
            )
        )

        # -----------------------------------------------------
        # PROPERTY DETAILS
        # -----------------------------------------------------

        story.append(
            Paragraph(
                "🏡 Property Details",
                heading_style
            )
        )

        property_data = [
            ["Feature", "Value"],
            ["Overall Quality", f"{overall_qual}/10"],
            ["Living Area", f"{gr_liv_area:,} sq ft"],
            ["Garage Capacity", f"{garage_cars} cars"],
            ["Garage Area", f"{garage_area:,} sq ft"],
            ["Total Basement Area", f"{total_bsmt_sf:,} sq ft"],
            ["First Floor Area", f"{first_floor_sf:,} sq ft"],
            ["Year Built", str(year_built)],
            ["Bedrooms", str(bedrooms)],
            ["Full Bathrooms", str(full_bath)],
            ["Total Rooms", str(total_rooms)],
            ["Overall Condition", f"{overall_cond}/10"],
        ]

        property_table = Table(
            property_data,
            colWidths=[250, 200]
        )

        property_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#312e81")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (0, -1),
                    "Helvetica-Bold"
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.HexColor("#f8fafc")
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#cbd5e1")
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
            ])
        )

        story.append(property_table)

        story.append(Spacer(1, 20))

        # -----------------------------------------------------
        # MODEL INFORMATION
        # -----------------------------------------------------

        model_data = [
            ["Item", "Details"],
            ["Application", "HouseWise AI"],
            ["Task", "House Price Prediction"],
            ["Model Type", "Machine Learning Regression"],
            ["Prediction Output", "Estimated Sale Price"],
        ]

        model_table = Table(
            model_data,
            colWidths=[180, 270],
            repeatRows=1,
            splitByRow=0
        )

        model_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#4f46e5")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#cbd5e1")
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.HexColor("#f8fafc")
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
            ])
        )

        story.append(
            KeepTogether([
                Paragraph(
                    "🤖 Model Information",
                    heading_style
                ),
                model_table
            ])
        )

        story.append(Spacer(1, 20))

        # -----------------------------------------------------
        # DATE / DISCLAIMER
        # -----------------------------------------------------

        generated_time = datetime.now().strftime(
            "%d %B %Y, %I:%M %p"
        )

        story.append(
            Paragraph(
                f"<b>Report Generated:</b> {generated_time}",
                normal_style
            )
        )

        story.append(Spacer(1, 10))

        story.append(
            Paragraph(
                "<b>Disclaimer:</b> This report contains an estimated "
                "property value generated by the trained Machine Learning "
                "model. The prediction should be treated as an estimate "
                "and not as an official property valuation.",
                normal_style
            )
        )

        story.append(Spacer(1, 25))

        story.append(
            Paragraph(
                "HouseWise AI • Python • Scikit-learn • Streamlit",
                subtitle_style
            )
        )

        doc.build(story)

        buffer.seek(0)

        return buffer

    pdf_file = create_prediction_pdf()

    st.download_button(
        label="📥 Download Prediction Report",
        data=pdf_file,
        file_name="HouseWise_AI_Prediction_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    # =========================================================
    # MODEL PERFORMANCE
    # =========================================================

    st.markdown(
        """
        <div class="section-title">
            📊 Model Performance
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Evaluation results obtained from the trained Machine Learning model."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "MAE",
            "$20,468"
        )

    with col2:
        st.metric(
            "RMSE",
            "$52,347"
        )

    with col3:
        st.metric(
            "R² Score",
            "0.6428"
        )

    with col4:
        st.metric(
            "MSE",
            "2.74B"
        )

    st.info(
        "💡 The R² score indicates that the model explains approximately "
        "64.28% of the variation in house prices on the evaluation data."
    )

    # =====================================================
    # HOW IT WORKS
    # =====================================================

    with st.expander(
        "💡 How does this prediction work?"
    ):

        st.markdown(
        """
### Step 1 — Enter Property Details

Provide details such as house quality, living area,
bedrooms, bathrooms, garage, basement area and year built.

### Step 2 — Model Processing

The entered values are passed to the trained
Machine Learning regression model.

### Step 3 — Price Prediction

The model analyzes the property features and generates
an estimated house price.

### Step 4 — Result

The estimated price is displayed together with a
summary of the property details.
        """
        )


    # =====================================================
    # MODEL PERFORMANCE
    # =====================================================

    with st.expander(
        "🤖 Model Performance"
    ):

        st.write(
            "The prediction is generated using the trained "
            "Machine Learning regression model developed "
            "during the project."
        )


        metric1, metric2, metric3 = st.columns(3)


        with metric1:

            st.metric(
                "📈 R² Score",
                "64.28%"
            )


        with metric2:

            st.metric(
                "📉 MAE",
                "$20,468"
            )


        with metric3:

            st.metric(
                "📊 RMSE",
                "$52,347"
            )


        st.caption(
            "These metrics were obtained during model "
            "evaluation on the test dataset."
        )


    # =====================================================
    # PREDICTION HISTORY
    # =====================================================

    if (
        "prediction_history" in st.session_state
        and st.session_state.prediction_history
    ):

        st.markdown("---")


        st.markdown(
        """
        <div class="section-title">
        📜 Prediction History
        </div>
        """,
        unsafe_allow_html=True
        )


        history_df = pd.DataFrame(
            st.session_state.prediction_history
        )


        display_df = history_df.copy()


        if "Predicted Price" in display_df.columns:

            display_df["Predicted Price"] = (
                display_df["Predicted Price"]
                .apply(
                    lambda x: f"${x:,.2f}"
                )
            )


        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


        history_col1, history_col2 = st.columns(2)


        with history_col1:

            csv_data = display_df.to_csv(
                index=False
            )


            st.download_button(
                label="📥 Download History",
                data=csv_data,
                file_name="house_price_prediction_history.csv",
                mime="text/csv",
                use_container_width=True
            )


        with history_col2:

            if st.button(
                "🗑️ Clear History",
                use_container_width=True
            ):

                st.session_state.prediction_history = []

                st.rerun()


    # =====================================================
    # WHAT-IF ANALYSIS
    # =====================================================

    st.markdown("---")

    st.markdown(
        """
        <div class="section-title">
        💡 What-If Analysis
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Experiment with different property characteristics "
        "and see how the estimated price changes."
    )

    whatif_col1, whatif_col2, whatif_col3 = st.columns(3)

    with whatif_col1:

        what_if_area = st.slider(
            "🏠 Living Area (sq ft)",
            min_value=500,
            max_value=5000,
            value=max(500, min(5000, int(result_gr_liv_area))),
            step=100
        )

    with whatif_col2:

        what_if_quality = st.slider(
            "⭐ Overall Quality",
            min_value=1,
            max_value=10,
            value=int(result_overall_qual),
            step=1
        )

    with whatif_col3:

        what_if_garage = st.slider(
            "🚗 Garage Capacity",
            min_value=0,
            max_value=5,
            value=int(result_garage_cars),
            step=1
        )

    # -----------------------------------------------------
    # CREATE WHAT-IF INPUT
    # -----------------------------------------------------

    what_if_input = st.session_state.input_df.copy()

    what_if_input["GrLivArea"] = what_if_area
    what_if_input["OverallQual"] = what_if_quality
    what_if_input["GarageCars"] = what_if_garage

    # -----------------------------------------------------
    # PROCESS WHAT-IF INPUT
    # -----------------------------------------------------

    what_if_processed = pd.get_dummies(
        what_if_input,
        drop_first=True
    )

    what_if_processed = what_if_processed.reindex(
        columns=X_processed.columns,
        fill_value=0
    )

    # -----------------------------------------------------
    # WHAT-IF PREDICTION
    # -----------------------------------------------------

    what_if_prediction = model.predict(
        what_if_processed
    )[0]

    price_difference = (
        what_if_prediction - prediction
    )

    # =====================================================
    # WHAT-IF RESULTS
    # =====================================================

    st.markdown(
        """
        <div class="whatif-result">
        <h4>📊 Scenario Result</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:

        st.metric(
            "Current Price",
            f"${prediction:,.0f}"
        )

    with result_col2:

        st.metric(
            "What-If Price",
            f"${what_if_prediction:,.0f}"
        )

    with result_col3:

        st.metric(
            "Price Difference",
            f"${price_difference:,.0f}",
            delta=f"${price_difference:,.0f}"
        )

    # =====================================================
    # PRICE COMPARISON
    # =====================================================

    st.markdown(
        "### 📊 Price Comparison"
    )

    comparison_df = pd.DataFrame(
        {
            "Price Type": [
                "Current Price",
                "What-If Price"
            ],
            "Amount": [
                prediction,
                what_if_prediction
            ]
        }
    )

    fig = px.bar(
        comparison_df,
        x="Price Type",
        y="Amount",
        color="Price Type",
        color_discrete_sequence=[
            "#4f46e5",
            "#14b8a6"
        ],
        text=comparison_df["Amount"]
            .round(0)
            .astype(int)
            .astype(str)
            .map(lambda value: f"${value}"),
        labels={
            "Price Type": "Scenario",
            "Amount": "Estimated Price"
        }
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    fig.update_layout(
        title="Current vs What-If Price",
        template="plotly_white",
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        ),
        showlegend=False,
        yaxis_title="Estimated Price",
        xaxis_title="Scenario"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        height=320
    )


    # =====================================================
    # PROPERTY INSIGHTS
    # =====================================================

    st.markdown("---")

    st.markdown(
    """
    <div class="section-title">
    🏠 Property Insights
    </div>
    """,
    unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # Calculate derived property insights
    # -----------------------------------------------------
    price_per_sqft = (
        prediction / result_gr_liv_area
        if result_gr_liv_area > 0
        else 0
    )

    property_rating = round(
        (
            float(result_overall_qual)
            + float(result_overall_cond)
        ) / 2,
        1
    )

    # -----------------------------------------------------
    # INSIGHT CARDS — ROW 1
    # -----------------------------------------------------
    insight_col1, insight_col2, insight_col3, insight_col4 = st.columns(4)

    with insight_col1:
        st.metric(
            "🏠 Living Area",
            f"{result_gr_liv_area:,.0f} sq ft"
        )

    with insight_col2:
        st.metric(
            "🛏️ Bedrooms",
            f"{result_bedrooms}"
        )

    with insight_col3:
        st.metric(
            "🚿 Bathrooms",
            f"{result_full_bath}"
        )

    with insight_col4:
        st.metric(
            "🚗 Garage",
            f"{result_garage_cars} cars"
        )

    # -----------------------------------------------------
    # INSIGHT CARDS — ROW 2
    # -----------------------------------------------------
    insight_col5, insight_col6, insight_col7, insight_col8 = st.columns(4)

    with insight_col5:
        st.metric(
            "📅 Year Built",
            f"{result_year_built}"
        )

    with insight_col6:
        st.metric(
            "⭐ Overall Quality",
            f"{result_overall_qual}/10"
        )

    with insight_col7:
        st.metric(
            "💰 Price / Sq Ft",
            f"${price_per_sqft:,.2f}"
        )

    with insight_col8:
        st.metric(
            "🏆 Property Rating",
            f"{property_rating}/10"
        )

    # -----------------------------------------------------
    # AUTOMATIC PROPERTY INSIGHT
    # -----------------------------------------------------
    if property_rating >= 8:

        quality_text = (
            "Excellent property profile with strong overall "
            "quality and condition."
        )

    elif property_rating >= 6:

        quality_text = (
            "Good property profile with balanced quality "
            "and condition."
        )

    elif property_rating >= 4:

        quality_text = (
            "Average property profile with potential for "
            "improvement."
        )

    else:

        quality_text = (
            "Basic property profile that may benefit from "
            "renovation or improvements."
        )

    st.info(
        f"💡 **Property Summary:** {quality_text}"
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")


st.markdown(
"""
<div class="footer">
<div class="footer-title">
🏠 HouseWise AI
</div>
<div class="footer-subtitle">
Smart House Price Prediction using Machine Learning
</div>
<div class="footer-tech">
Built with Python • Scikit-learn • Streamlit
</div>
</div>
""",
unsafe_allow_html=True
)