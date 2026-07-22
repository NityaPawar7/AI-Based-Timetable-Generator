"""Reusable Streamlit styling helpers for the dark dashboard UI."""

from __future__ import annotations

from html import escape

import streamlit as st


def inject_custom_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --bg: #0F172A;
            --panel: rgba(15, 23, 42, 0.76);
            --panel-strong: rgba(30, 41, 59, 0.92);
            --line: rgba(148, 163, 184, 0.22);
            --text: #F8FAFC;
            --muted: #CBD5E1;
            --cyan: #38BDF8;
            --blue: #2563EB;
            --purple: #8B5CF6;
            --success: #22C55E;
            --warning: #F59E0B;
            --danger: #EF4444;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(56, 189, 248, 0.22), transparent 30rem),
                radial-gradient(circle at top right, rgba(139, 92, 246, 0.22), transparent 28rem),
                linear-gradient(135deg, #0F172A 0%, #111827 48%, #1E1B4B 100%);
            color: var(--text);
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.98), rgba(30, 41, 59, 0.96));
            border-right: 1px solid var(--line);
        }

        section[data-testid="stSidebar"] * {
            color: var(--text);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2.5rem;
            max-width: 1240px;
        }

        h1, h2, h3 {
            color: var(--text);
            letter-spacing: 0;
        }

        p, li, label, span {
            color: var(--muted);
        }

        div[data-testid="stTabs"] button {
            color: var(--muted);
            border-radius: 12px 12px 0 0;
            font-weight: 700;
        }

        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: var(--cyan);
            background: rgba(56, 189, 248, 0.08);
        }

        div[data-testid="stMetric"] {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.86), rgba(15, 23, 42, 0.9));
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 1rem;
            box-shadow: 0 18px 45px rgba(2, 6, 23, 0.24);
        }

        div[data-testid="stMetricLabel"] p {
            color: #A5B4FC;
            font-size: 0.86rem;
            font-weight: 700;
        }

        div[data-testid="stMetricValue"] {
            color: var(--text);
            font-weight: 800;
        }

        .stButton > button,
        .stDownloadButton > button,
        .stFormSubmitButton > button {
            border: 0;
            border-radius: 14px;
            color: #F8FAFC;
            font-weight: 800;
            background: linear-gradient(135deg, #2563EB, #38BDF8);
            box-shadow: 0 14px 32px rgba(37, 99, 235, 0.28);
            transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        .stFormSubmitButton > button:hover {
            transform: translateY(-1px);
            filter: brightness(1.08);
            box-shadow: 0 18px 44px rgba(56, 189, 248, 0.30);
            color: #FFFFFF;
        }

        .stTextInput input,
        .stNumberInput input,
        .stDateInput input,
        .stSelectbox div[data-baseweb="select"],
        .stSelectbox div[data-baseweb="select"] > div,
        .stMultiSelect div[data-baseweb="select"],
        .stMultiSelect div[data-baseweb="select"] > div {
            background: rgba(15, 23, 42, 0.88);
            border: 1px solid var(--line);
            color: var(--text);
            border-radius: 12px;
        }

        div[data-testid="stDataFrame"],
        div[data-testid="stDataEditor"] {
            border: 1px solid var(--line);
            border-radius: 18px;
            overflow: hidden;
            box-shadow: 0 18px 45px rgba(2, 6, 23, 0.26);
        }

        div[data-testid="stForm"],
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(15, 23, 42, 0.48);
            border: 1px solid var(--line);
            border-radius: 18px;
            box-shadow: 0 18px 45px rgba(2, 6, 23, 0.18);
        }

        .hero-card {
            position: relative;
            overflow: hidden;
            padding: 2.25rem;
            border-radius: 28px;
            border: 1px solid rgba(148, 163, 184, 0.24);
            background:
                linear-gradient(135deg, rgba(15, 23, 42, 0.92), rgba(30, 27, 75, 0.86)),
                linear-gradient(90deg, rgba(56, 189, 248, 0.14), rgba(139, 92, 246, 0.16));
            box-shadow: 0 24px 70px rgba(2, 6, 23, 0.38);
        }

        .hero-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--cyan);
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(56, 189, 248, 0.26);
            border-radius: 999px;
            padding: 0.45rem 0.85rem;
            font-size: 0.82rem;
            font-weight: 800;
            text-transform: uppercase;
        }

        .hero-title {
            color: var(--text);
            font-size: clamp(2.2rem, 5vw, 4.5rem);
            line-height: 1.02;
            margin: 1.1rem 0 1rem 0;
            font-weight: 800;
        }

        .hero-subtitle {
            max-width: 820px;
            color: #DDE7F6;
            font-size: 1.12rem;
            line-height: 1.75;
            margin-bottom: 1.5rem;
        }

        .hero-strip {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
        }

        .hero-chip,
        .status-pill {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            border: 1px solid rgba(148, 163, 184, 0.22);
            background: rgba(15, 23, 42, 0.56);
            color: #E0F2FE;
            font-weight: 800;
            font-size: 0.88rem;
            padding: 0.55rem 0.85rem;
        }

        .dashboard-card {
            min-height: 150px;
            padding: 1.25rem;
            border-radius: 20px;
            border: 1px solid rgba(148, 163, 184, 0.22);
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.84), rgba(15, 23, 42, 0.84));
            box-shadow: 0 18px 45px rgba(2, 6, 23, 0.25);
        }

        .dashboard-card h3 {
            margin: 0.6rem 0 0.5rem 0;
            font-size: 1.05rem;
            color: var(--text);
        }

        .dashboard-card p {
            margin: 0;
            font-size: 0.94rem;
            line-height: 1.62;
            color: #CBD5E1;
        }

        .card-icon {
            width: 2.6rem;
            height: 2.6rem;
            display: grid;
            place-items: center;
            border-radius: 14px;
            color: #FFFFFF;
            font-weight: 800;
            background: linear-gradient(135deg, #38BDF8, #8B5CF6);
            box-shadow: 0 12px 28px rgba(56, 189, 248, 0.22);
        }

        .section-card {
            padding: 1.35rem;
            border-radius: 20px;
            border: 1px solid var(--line);
            background: rgba(15, 23, 42, 0.58);
            box-shadow: 0 18px 45px rgba(2, 6, 23, 0.20);
            margin-bottom: 1rem;
        }

        .section-title {
            color: var(--text);
            font-weight: 800;
            font-size: 1.35rem;
            margin: 0 0 0.25rem 0;
        }

        .section-copy {
            color: var(--muted);
            margin: 0 0 1rem 0;
            line-height: 1.65;
        }

        .sidebar-brand {
            padding: 1rem;
            border-radius: 18px;
            border: 1px solid rgba(56, 189, 248, 0.22);
            background: linear-gradient(145deg, rgba(37, 99, 235, 0.18), rgba(139, 92, 246, 0.12));
            margin-bottom: 1rem;
        }

        .sidebar-brand h2 {
            font-size: 1.05rem;
            margin: 0 0 0.35rem 0;
            color: #F8FAFC;
        }

        .sidebar-brand p {
            color: #CBD5E1;
            font-size: 0.86rem;
            line-height: 1.5;
            margin: 0;
        }

        .status-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.7rem;
            margin: 0.5rem 0 1.1rem 0;
        }

        .status-success {
            color: #DCFCE7;
            border-color: rgba(34, 197, 94, 0.34);
            background: rgba(34, 197, 94, 0.13);
        }

        .status-info {
            color: #E0F2FE;
            border-color: rgba(56, 189, 248, 0.34);
            background: rgba(56, 189, 248, 0.12);
        }

        .big-generate button {
            min-height: 4rem;
            font-size: 1.1rem;
            letter-spacing: 0;
        }

        .metric-card {
            min-height: 112px;
            padding: 1.1rem;
            border-radius: 18px;
            border: 1px solid var(--line);
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.88), rgba(15, 23, 42, 0.92));
            box-shadow: 0 18px 45px rgba(2, 6, 23, 0.24);
        }

        .metric-label {
            color: #A5B4FC;
            font-size: 0.82rem;
            font-weight: 800;
            margin-bottom: 0.45rem;
        }

        .metric-value {
            color: #F8FAFC;
            font-size: 2.1rem;
            line-height: 1.05;
            font-weight: 800;
            white-space: normal;
            word-break: break-word;
        }

        .dark-table-wrap {
            width: 100%;
            overflow-x: auto;
            border: 1px solid var(--line);
            border-radius: 18px;
            box-shadow: 0 18px 45px rgba(2, 6, 23, 0.26);
            background: rgba(15, 23, 42, 0.7);
        }

        table.dark-table {
            width: 100%;
            border-collapse: collapse;
            color: #E2E8F0;
            font-size: 0.9rem;
        }

        table.dark-table thead th {
            background: rgba(56, 189, 248, 0.13);
            color: #E0F2FE;
            font-weight: 800;
            text-align: left;
            padding: 0.85rem;
            border-bottom: 1px solid var(--line);
            white-space: nowrap;
        }

        table.dark-table tbody td {
            padding: 0.78rem 0.85rem;
            border-bottom: 1px solid rgba(148, 163, 184, 0.12);
            color: #E2E8F0;
            white-space: nowrap;
        }

        table.dark-table tbody tr:nth-child(even) {
            background: rgba(30, 41, 59, 0.45);
        }

        table.dark-table tbody tr:hover {
            background: rgba(56, 189, 248, 0.10);
        }

        hr {
            border-color: rgba(148, 163, 184, 0.18);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero_section() -> None:
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-eyebrow">DAA + AIML Project Dashboard</div>
            <div class="hero-title">AI-Based Examination Timetable Generator</div>
            <div class="hero-subtitle">
                Generate conflict-free exam schedules using Graph Coloring,
                Backtracking, and Constraint Satisfaction while balancing rooms,
                time slots, and student group conflicts.
            </div>
            <div class="hero-strip">
                <span class="hero-chip">Graph Coloring</span>
                <span class="hero-chip">Backtracking Search</span>
                <span class="hero-chip">Constraint Satisfaction</span>
                <span class="hero-chip">CSV Input and Output</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_card(title: str, body: str, icon: str) -> None:
    st.markdown(
        f"""
        <div class="dashboard-card">
            <div class="card-icon">{escape(icon)}</div>
            <h3>{escape(title)}</h3>
            <p>{escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, body: str = "") -> None:
    body_html = f'<p class="section-copy">{escape(body)}</p>' if body else ""
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-title">{escape(title)}</div>
            {body_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badges(items: list[tuple[str, str]]) -> None:
    badges = "\n".join(
        f'<span class="status-pill {escape(kind)}">{escape(label)}</span>'
        for label, kind in items
    )
    st.markdown(f'<div class="status-row">{badges}</div>', unsafe_allow_html=True)


def metric_card(label: str, value: object) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{escape(label)}</div>
            <div class="metric-value">{escape(str(value))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def dark_table(df) -> None:
    html = df.to_html(index=False, classes="dark-table", border=0, escape=True)
    st.markdown(f'<div class="dark-table-wrap">{html}</div>', unsafe_allow_html=True)


def sidebar_brand() -> None:
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <h2>Exam Scheduler AI</h2>
            <p>DAA mini-project dashboard for conflict graphs, timetable generation, and result analysis.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
