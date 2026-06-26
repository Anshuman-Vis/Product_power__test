import streamlit as st
import json
import tempfile
import os
from productpower import llm_nutritionist
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# ===========================
# PAGE CONFIGURATION
# ===========================
st.set_page_config(
    page_title="ProductPower FSSAI",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================
# SESSION STATE
# ===========================
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# ===========================
# ALL CSS STYLES
# ===========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: #0a0e1a !important;
}
.main .block-container {
    padding-top: 0px !important;
    max-width: 100% !important;
}

/* ---- NAVBAR ---- */
.pp-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 48px;
    background: rgba(10,14,26,0.97);
    border-bottom: 1px solid rgba(255,255,255,0.07);
    backdrop-filter: blur(12px);
}
.pp-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 20px;
    font-weight: 800;
    color: white;
}
.pp-logo-icon {
    width: 34px;
    height: 34px;
    background: linear-gradient(135deg, #a855f7, #3b82f6);
    border-radius: 8px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}
.pp-power { color: #a855f7; }
.pp-nav-actions {
    display: flex;
    gap: 12px;
    align-items: center;
}
.pp-btn-login {
    color: rgba(255,255,255,0.75);
    font-size: 14px;
    font-weight: 500;
    background: none;
    border: none;
    padding: 8px 16px;
    cursor: pointer;
}
.pp-btn-get {
    background: linear-gradient(135deg, #a855f7, #7c3aed);
    color: white;
    border: none;
    padding: 10px 22px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 4px 20px rgba(168,85,247,0.35);
}

/* ---- HERO ---- */
.pp-hero {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 64px 48px 56px;
    background: #0a0e1a;
    gap: 40px;
    min-height: 88vh;
}
.pp-hero-left { flex: 1; max-width: 560px; }
.pp-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(168,85,247,0.1);
    border: 1px solid rgba(168,85,247,0.3);
    color: #c084fc;
    padding: 7px 16px;
    border-radius: 100px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 28px;
    letter-spacing: 0.3px;
}
.pp-badge-dot {
    width: 7px; height: 7px;
    background: #a855f7;
    border-radius: 50%;
    display: inline-block;
    animation: pp-blink 1.5s infinite;
}
@keyframes pp-blink {
    0%,100%{opacity:1} 50%{opacity:0.2}
}
.pp-title {
    font-size: 64px;
    font-weight: 900;
    line-height: 1.05;
    color: white;
    margin: 0 0 20px;
    letter-spacing: -2px;
}
.pp-cyan {
    background: linear-gradient(135deg, #06b6d4, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.pp-pink {
    background: linear-gradient(135deg, #a855f7, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.pp-subtitle {
    font-size: 17px;
    color: rgba(255,255,255,0.5);
    line-height: 1.7;
    margin-bottom: 40px;
    max-width: 480px;
}
.pp-btns { display: flex; gap: 16px; flex-wrap: wrap; }
.pp-btn-primary {
    background: linear-gradient(135deg, #a855f7, #7c3aed);
    color: white;
    border: none;
    padding: 15px 32px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 8px 32px rgba(168,85,247,0.35);
}
.pp-btn-secondary {
    background: rgba(255,255,255,0.05);
    color: rgba(255,255,255,0.85);
    border: 1px solid rgba(255,255,255,0.12);
    padding: 14px 28px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
}

/* ---- SCANNER PANEL ---- */
.pp-hero-right { flex: 1; max-width: 560px; }
.pp-panel {
    background: #0f1629;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 24px 80px rgba(0,0,0,0.6), 0 0 0 1px rgba(168,85,247,0.08);
}
.pp-titlebar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 13px 20px;
    background: #141928;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.pp-lights { display: flex; gap: 7px; }
.pp-tl {
    width: 12px; height: 12px; border-radius: 50%;
}
.pp-red{background:#ff5f57}
.pp-yellow{background:#febc2e}
.pp-green{background:#28c840}
.pp-panel-title {
    color: rgba(255,255,255,0.45);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}
.pp-ready {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #22c55e;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.pp-ready-dot {
    width: 7px; height: 7px;
    background: #22c55e;
    border-radius: 50%;
    display: inline-block;
    animation: pp-blink 2s infinite;
}
.pp-status-row {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    padding: 14px 20px 0;
}
.pp-sbadge {
    padding: 5px 14px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}
.pp-scan-badge {
    background: rgba(6,182,212,0.12);
    border: 1px solid rgba(6,182,212,0.3);
    color: #06b6d4;
}
.pp-fssai-badge {
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.3);
    color: #22c55e;
}
.pp-progress {
    height: 3px;
    background: linear-gradient(90deg, #06b6d4, #3b82f6);
    margin: 10px 20px 0;
    border-radius: 2px;
    animation: pp-prog 2s ease-in-out infinite;
}
@keyframes pp-prog {
    0%{width:40%;opacity:0.6}
    50%{width:100%;opacity:1}
    100%{width:40%;opacity:0.6}
}

/* ---- ROBOT SCENE ---- */
.pp-scene {
    height: 240px;
    position: relative;
    overflow: hidden;
    margin: 16px 20px 0;
}
.pp-arm-wrap {
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    animation: pp-arm 3s ease-in-out infinite;
    transform-origin: bottom center;
}
@keyframes pp-arm {
    0%{transform:translateX(-50%) rotate(-12deg)}
    50%{transform:translateX(-50%) rotate(12deg)}
    100%{transform:translateX(-50%) rotate(-12deg)}
}
.pp-beam {
    position: absolute;
    top: 90px;
    left: 50%;
    transform: translateX(-50%);
    width: 3px;
    height: 150px;
    background: linear-gradient(180deg,#06b6d4,transparent);
    filter: blur(1px);
    animation: pp-beam 1.5s ease-in-out infinite;
}
@keyframes pp-beam {
    0%,100%{opacity:0.3;width:3px}
    50%{opacity:1;width:8px}
}
.pp-belt {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 16px;
    background: linear-gradient(90deg,#1e293b,#334155,#1e293b);
    border-top: 2px solid #475569;
}
.pp-belt-lines {
    display: flex;
    height: 100%;
    align-items: center;
    gap: 28px;
    padding: 0 8px;
    animation: pp-belt 1.2s linear infinite;
}
@keyframes pp-belt {
    0%{transform:translateX(0)}
    100%{transform:translateX(-28px)}
}
.pp-belt-line {
    width: 18px; height: 3px;
    background: rgba(148,163,184,0.35);
    border-radius: 2px;
    flex-shrink: 0;
}
.pp-products {
    position: absolute;
    bottom: 16px;
    display: flex;
    gap: 18px;
    align-items: flex-end;
    animation: pp-slide 6s linear infinite;
}
@keyframes pp-slide {
    0%{transform:translateX(600px)}
    100%{transform:translateX(-600px)}
}
.pp-bottle {
    width: 26px; height: 50px;
    border-radius: 4px 4px 3px 3px;
    flex-shrink: 0;
    position: relative;
}
.pp-bottle::before {
    content:'';
    position:absolute;
    top:-7px; left:50%;
    transform:translateX(-50%);
    width:10px; height:7px;
    background:inherit;
    border-radius:2px 2px 0 0;
}
.pp-box {
    width: 42px; height: 42px;
    border-radius: 6px;
    flex-shrink: 0;
}
.c-purple{background:linear-gradient(180deg,#7c3aed,#a855f7)}
.c-orange{background:linear-gradient(180deg,#ea580c,#f97316)}
.c-blue{background:linear-gradient(180deg,#1d4ed8,#3b82f6)}
.c-green{background:linear-gradient(180deg,#15803d,#22c55e)}
.c-box-o{background:linear-gradient(135deg,#ea580c,#f97316)}
.c-box-b{background:linear-gradient(135deg,#1d4ed8,#60a5fa)}

/* ---- TERMINAL ---- */
.pp-term-bar {
    display:flex;
    justify-content:space-between;
    padding: 8px 20px;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin-top: 8px;
}
.pp-term-label, .pp-term-fps {
    color: rgba(255,255,255,0.3);
    font-size: 11px;
}
.pp-term-logs {
    padding: 10px 20px 18px;
    background: #080d1a;
}
.pp-log {
    font-family: 'Courier New', monospace;
    font-size: 11px;
    line-height: 1.9;
}
.pp-log-sys{color:#94a3b8}
.pp-log-ocr{color:#22c55e}
.pp-log-ai {color:#06b6d4}

/* ---- DIVIDER ---- */
.pp-divider {
    border:none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 0;
}

/* ---- METRIC CARDS ---- */
.metric-card {
    border-radius: 14px;
    padding: 20px;
    color: white;
}
.risk-excellent{background:linear-gradient(135deg,#065f46,#10b981)!important}
.risk-good{background:linear-gradient(135deg,#1e40af,#3b82f6)!important}
.risk-moderate{background:linear-gradient(135deg,#92400e,#f59e0b)!important}
.risk-high{background:linear-gradient(135deg,#7f1d1d,#ef4444)!important}

/* ---- DARK MODE OVERRIDES ---- */
.dark-mode .stApp { background:#0b1220!important }
.dark-mode section[data-testid="stSidebar"] { background:#0f172a!important }

</style>
""", unsafe_allow_html=True)

# ========================
# NAVBAR
# ========================
st.markdown("""
<div class="pp-navbar">
    <div class="pp-logo">
        <div class="pp-logo-icon">⚡</div>
        <span>product<span class="pp-power">Power</span></span>
    </div>
    <div class="pp-nav-actions">
        <button class="pp-btn-login">Log In</button>
        <button class="pp-btn-get">Get Started</button>
    </div>
</div>
""", unsafe_allow_html=True)

# ========================
# HERO SECTION
# ========================
st.markdown("""
<div class="pp-hero">
    <div class="pp-hero-left">
        <div class="pp-badge">
            <span class="pp-badge-dot"></span>
            NEXT-GEN OCR ENGINE
        </div>
        <h1 class="pp-title">
            AI-Powered Food<br>
            <span class="pp-cyan">Label</span><span class="pp-pink"> Intelligence</span>
        </h1>
        <p class="pp-subtitle">
            Automate food safety auditing, risk assessment, and
            regulatory compliance with lightning-fast AI extraction.
            Precision data at the speed of light.
        </p>
        <div class="pp-btns">
            <button class="pp-btn-primary">Get Started Free</button>
            <button class="pp-btn-secondary">&#9654; Watch Demo</button>
        </div>
    </div>
    <div class="pp-hero-right">
        <div class="pp-panel">
            <div class="pp-titlebar">
                <div class="pp-lights">
                    <div class="pp-tl pp-red"></div>
                    <div class="pp-tl pp-yellow"></div>
                    <div class="pp-tl pp-green"></div>
                </div>
                <div class="pp-panel-title">ROBOTIC COMPLIANCE AUDITOR v1.0</div>
                <div class="pp-ready">
                    <span class="pp-ready-dot"></span> SYSTEM READY
                </div>
            </div>
            <div class="pp-status-row">
                <div class="pp-sbadge pp-scan-badge">&#10003; SCAN COMPLETED</div>
                <div class="pp-sbadge pp-fssai-badge">&#10003; FSSAI VERIFIED</div>
            </div>
            <div class="pp-progress"></div>
            <div class="pp-scene">
                <div class="pp-arm-wrap">
                    <svg width="110" height="125" viewBox="0 0 110 125">
                        <rect x="45" y="108" width="20" height="14" rx="3" fill="#334155"/>
                        <rect x="40" y="100" width="30" height="10" rx="4" fill="#475569"/>
                        <line x1="55" y1="100" x2="40" y2="58" stroke="#64748b" stroke-width="8" stroke-linecap="round"/>
                        <circle cx="40" cy="58" r="6" fill="#94a3b8"/>
                        <line x1="40" y1="58" x2="55" y2="18" stroke="#64748b" stroke-width="6" stroke-linecap="round"/>
                        <circle cx="55" cy="18" r="5" fill="#06b6d4"/>
                        <line x1="47" y1="13" x2="40" y2="6" stroke="#06b6d4" stroke-width="3" stroke-linecap="round"/>
                        <line x1="63" y1="13" x2="70" y2="6" stroke="#06b6d4" stroke-width="3" stroke-linecap="round"/>
                        <circle cx="55" cy="18" r="12" fill="rgba(6,182,212,0.12)"/>
                    </svg>
                </div>
                <div class="pp-beam"></div>
                <div class="pp-products">
                    <div class="pp-bottle c-purple"></div>
                    <div class="pp-box c-box-o"></div>
                    <div class="pp-bottle c-blue"></div>
                    <div class="pp-box c-box-b"></div>
                    <div class="pp-bottle c-orange"></div>
                    <div class="pp-bottle c-green"></div>
                    <div class="pp-box c-box-o"></div>
                    <div class="pp-bottle c-purple"></div>
                </div>
                <div class="pp-belt">
                    <div class="pp-belt-lines">
                        <div class="pp-belt-line"></div><div class="pp-belt-line"></div>
                        <div class="pp-belt-line"></div><div class="pp-belt-line"></div>
                        <div class="pp-belt-line"></div><div class="pp-belt-line"></div>
                        <div class="pp-belt-line"></div><div class="pp-belt-line"></div>
                        <div class="pp-belt-line"></div><div class="pp-belt-line"></div>
                        <div class="pp-belt-line"></div><div class="pp-belt-line"></div>
                    </div>
                </div>
            </div>
            <div class="pp-term-bar">
                <span class="pp-term-label">Terminal OCR Readout</span>
                <span class="pp-term-fps">60 FPS // LATENCY: 3.4ms</span>
            </div>
            <div class="pp-term-logs">
                <div class="pp-log pp-log-sys">[SYS] CONNECTING TO FSSAI SECURITY NETWORK...</div>
                <div class="pp-log pp-log-ocr">[OCR] EXTRACTING LABEL: FRUIT JUICE 90%, CHERRY EXTRACT 10%</div>
                <div class="pp-log pp-log-ai">[AI] RISK SCORE CALCULATED: 18/100 &#8212; GRADE A</div>
            </div>
        </div>
    </div>
</div>
<hr class="pp-divider">
""", unsafe_allow_html=True)

# ===========================
# DARK MODE STYLES
# ===========================
def apply_theme():
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
        .stApp { background-color: #0b1220 !important; }
        section[data-testid="stSidebar"] { background-color: #0f172a !important; }
        .stApp * { color: #ffffff !important; }
        .stMarkdown p { color: #cbd5e1 !important; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp { background-color: #0a0e1a !important; }
        section[data-testid="stSidebar"] { background-color: #0f172a !important; }
        .stApp h1, .stApp h2, .stApp h3,
        .stApp label, .stApp p { color: #e2e8f0 !important; }
        </style>
        """, unsafe_allow_html=True)

apply_theme()

# ===========================
# HELPER FUNCTIONS
# ===========================
def get_risk_css(score):
    if score <= 20: return "risk-excellent"
    elif score <= 40: return "risk-good"
    elif score <= 60: return "risk-moderate"
    else: return "risk-high"

def get_risk_grade(score):
    if score <= 20: return "A", "Excellent"
    elif score <= 40: return "B", "Good"
    elif score <= 60: return "C", "Moderate"
    elif score <= 80: return "D", "High Risk"
    else: return "F", "Very High Risk"

def create_risk_gauge(score, category):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Food Risk Score<br><span style='font-size:0.8em'>{category}</span>"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkred"},
            'steps': [
                {'range': [0, 20], 'color': '#d1fae5'},
                {'range': [20, 40], 'color': '#a7f3d0'},
                {'range': [40, 60], 'color': '#fef3c7'},
                {'range': [60, 80], 'color': '#fed7aa'},
                {'range': [80, 100], 'color': '#fecaca'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)')
    return fig

def create_breakdown_chart(breakdown):
    if not breakdown: return None
    df = pd.DataFrame(list(breakdown.items()), columns=['Factor', 'Score'])
    df['Factor'] = df['Factor'].str.replace('_', ' ').str.title()
    fig = px.bar(df, x='Score', y='Factor', orientation='h',
                 title='Risk Score Breakdown', color='Score',
                 color_continuous_scale='Reds')
    fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)')
    return fig

def create_nutrition_pie(nutrition):
    if not nutrition: return None
    def get_num(val):
        try: return float(val)
        except: return 0
    data = pd.DataFrame({
        'Nutrient': ['Protein', 'Carbohydrate', 'Fat', 'Sugar'],
        'Amount': [
            get_num(nutrition.get('protein', 0)),
            get_num(nutrition.get('carbohydrate', 0)),
            get_num(nutrition.get('fat', 0)),
            get_num(nutrition.get('sugar', 0))
        ]
    })
    fig = px.pie(data, values='Amount', names='Nutrient',
                 title='Nutrition Distribution',
                 color_discrete_sequence=['#10b981','#3b82f6','#f59e0b','#ef4444'])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)')
    return fig

def create_additives_chart(additives):
    if not additives: return None
    risk_counts = {}
    for a in additives:
        risk = a.get('risk_level', 'Safe')
        risk_counts[risk] = risk_counts.get(risk, 0) + 1
    colors_map = {'Safe':'#10b981','Moderate':'#f59e0b','High Concern':'#ef4444'}
    fig = px.pie(values=list(risk_counts.values()),
                 names=list(risk_counts.keys()),
                 title='Additives Risk Distribution',
                 color=list(risk_counts.keys()),
                 color_discrete_map=colors_map)
    fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)')
    return fig

def create_comparison_chart(history):
    if len(history) < 2: return None
    data = [{'Product': item['name'], 'Risk Score': item['risk_score']} for item in history]
    df = pd.DataFrame(data)
    fig = px.bar(df, x='Product', y='Risk Score',
                 title='Product Risk Comparison',
                 color='Risk Score', color_continuous_scale='RdYlGn_r')
    fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)')
    return fig

def generate_pdf_report(report):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'],
        fontSize=24, textColor=colors.HexColor('#1f77b4'), spaceAfter=30, alignment=1)
    story.append(Paragraph("Food Safety Report", title_style))
    story.append(Spacer(1, 0.3*inch))
    product = report.get('product_info', {})
    story.append(Paragraph(f"<b>Product:</b> {product.get('product_name','N/A')}", styles['Normal']))
    story.append(Paragraph(f"<b>Brand:</b> {product.get('brand_name','N/A')}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    grade, label = get_risk_grade(report.get('risk_score', 0))
    story.append(Paragraph(
        f"<b>Risk Score:</b> {report.get('risk_score',0)}/100 (Grade {grade} - {label})",
        styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))
    fssai = report.get('fssai', {})
    story.append(Paragraph(f"<b>FSSAI:</b> {fssai.get('message','N/A')}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    nutrition = product.get('nutrition', {})
    if nutrition:
        data = [['Nutrient','Value']] + [[k.replace('_',' ').title(), str(v) or 'N/A']
                                          for k,v in nutrition.items()]
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#1f77b4')),
            ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
            ('BACKGROUND',(0,1),(-1,-1),colors.beige),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.2*inch))
    additives = report.get('additives', [])
    if additives:
        story.append(Paragraph("<b>Detected Additives:</b>", styles['Heading2']))
        for a in additives:
            story.append(Paragraph(f"• {a['ins']} - {a['name']} ({a['risk_level']})", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
    if report.get('ingredient_analysis'):
        story.append(Paragraph("<b>Ingredient Analysis:</b>", styles['Heading2']))
        story.append(Paragraph(str(report['ingredient_analysis']).replace('\n','<br/>'), styles['Normal']))
    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_csv(report):
    product = report.get('product_info', {})
    nutrition = product.get('nutrition', {})
    data = {
        'Product Name': [product.get('product_name','')],
        'Brand': [product.get('brand_name','')],
        'Risk Score': [report.get('risk_score',0)],
        'Risk Category': [report.get('risk_category','')],
        'FSSAI Status': [report.get('fssai',{}).get('message','')],
    }
    for k, v in nutrition.items():
        data[k.replace('_',' ').title()] = [v]
    return pd.DataFrame(data).to_csv(index=False)

# ===========================
# SIDEBAR
# ===========================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/vegetarian-food.png", width=80)
    st.title("⚙️ Settings")

    if st.button("🌓 Toggle Dark Mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.markdown("---")

    show_verbose = st.checkbox("📝 Show detailed logs", value=False)
    auto_save = st.checkbox("💾 Auto-save results", value=True)
    show_charts = st.checkbox("📊 Show charts", value=True)

    st.markdown("---")

    st.subheader("📜 Analysis History")
    if st.session_state.analysis_history:
        st.write(f"Total analyzed: {len(st.session_state.analysis_history)}")
        if st.button("🗑️ Clear History"):
            st.session_state.analysis_history = []
            st.rerun()
    else:
        st.write("No history yet")

    st.markdown("---")
    st.markdown("### 📖 How to use")
    st.markdown("""
    1. 📤 Upload food label image(s)
    2. 🔍 Click Analyze All
    3. 📊 View risk score & charts
    4. 🧪 Check additives & FSSAI
    5. 💾 Download PDF / JSON / CSV
    6. 🔄 Compare multiple products
    """)

    st.markdown("---")
    st.markdown("### ✨ Features")
    st.markdown("""
    - ✅ OCR Label Analysis
    - ✅ Nutrition Extraction
    - ✅ Additive Detection (INS)
    - ✅ FSSAI Validation
    - ✅ Food Risk Score (0-100)
    - ✅ AI Ingredient Analysis
    - ✅ PDF / JSON / CSV Export
    - ✅ Product Comparison
    """)

    st.markdown("---")
    st.markdown("### 👥 Developed by")
    st.markdown("- Anshuman Vishwakarma")

# ===========================
# MAIN CONTENT
# ===========================
st.markdown('<h1 style="text-align:center;color:white;">🍱 ProductPower FSSAI</h1>',
            unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#64748b;">AI-Powered Food Safety & Risk Analyzer</p>',
            unsafe_allow_html=True)
st.markdown("---")

# ===========================
# FILE UPLOAD
# ===========================
uploaded_files = st.file_uploader(
    "📤 Upload Food Label Image(s)",
    type=["jpg","jpeg","png","webp","pdf"],
    accept_multiple_files=True,
    help="Upload one or more food label images"
)

if uploaded_files:
    num_files = len(uploaded_files)
    st.success(f"✅ {num_files} image(s) uploaded")

    cols = st.columns(min(3, num_files))
    for idx, uploaded_file in enumerate(uploaded_files):
        if not uploaded_file.name.lower().endswith('.pdf'):
            with cols[idx % 3]:
                image = Image.open(uploaded_file)
                st.image(image, caption=uploaded_file.name, use_column_width=True)

    st.markdown("---")

    if st.button("🔍 Analyze All Images", type="primary", use_container_width=True):
        results = []

        for file_idx, uploaded_file in enumerate(uploaded_files):
            st.markdown(f"### 📊 Analyzing: {uploaded_file.name}")
            suffix = os.path.splitext(uploaded_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_path = tmp_file.name

            try:
                progress_bar = st.progress(0)
                status_text = st.empty()

                status_text.text("🔄 Initializing analyzer...")
                progress_bar.progress(10)
                analyzer = llm_nutritionist()

                status_text.text("🔍 Running full analysis...")
                progress_bar.progress(30)
                report = analyzer.analyze(temp_path)

                progress_bar.progress(100)
                status_text.text("✅ Complete!")

                risk_score = report['risk_score']
                risk_category = report['risk_category']
                risk_css = get_risk_css(risk_score)
                grade, grade_label = get_risk_grade(risk_score)

                st.session_state.analysis_history.append({
                    'name': uploaded_file.name,
                    'report': report,
                    'risk_score': risk_score,
                })

                results.append({
                    'name': uploaded_file.name,
                    'report': report,
                    'analyzer': analyzer,
                    'risk_score': risk_score,
                    'risk_category': risk_category,
                    'risk_css': risk_css,
                    'grade': grade,
                    'grade_label': grade_label,
                })

                if auto_save:
                    name = os.path.splitext(uploaded_file.name)[0]
                    save_path = os.path.join("results", name)
                    analyzer.save(save_path)

                os.unlink(temp_path)

            except Exception as e:
                st.error(f"❌ Error analyzing {uploaded_file.name}: {str(e)}")
                if show_verbose:
                    st.exception(e)

        st.markdown("---")
        st.markdown("## 📈 Results")

        for result in results:
            report = result['report']
            product = report.get('product_info', {})
            nutrition = product.get('nutrition', {})
            additives = report.get('additives', [])
            fssai = report.get('fssai', {})

            with st.expander(
                f"📊 {result['name']} — Risk: {result['risk_score']}/100 ({result['risk_category']})",
                expanded=True
            ):
                st.markdown(f"""
                <div class="metric-card {result['risk_css']}">
                    <h2 style="margin:0;color:white;">
                        Food Risk Score: {result['risk_score']}/100
                    </h2>
                    <h3 style="margin:5px 0;color:white;">
                        Grade {result['grade']} — {result['grade_label']}
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

                if show_charts:
                    gauge_col, breakdown_col = st.columns(2)
                    with gauge_col:
                        st.plotly_chart(
                            create_risk_gauge(result['risk_score'], result['risk_category']),
                            use_container_width=True
                        )
                    with breakdown_col:
                        breakdown_chart = create_breakdown_chart(report.get('risk_breakdown', {}))
                        if breakdown_chart:
                            st.plotly_chart(breakdown_chart, use_container_width=True)

                st.subheader("📦 Product Information")
                info_col1, info_col2 = st.columns(2)
                with info_col1:
                    st.write("**Product:**", product.get('product_name','N/A'))
                    st.write("**Brand:**", product.get('brand_name','N/A'))
                    st.write("**Serving Size:**", product.get('serving_size','N/A'))
                with info_col2:
                    st.write("**Net Weight:**", product.get('net_weight','N/A'))
                    allergens = product.get('allergens', [])
                    st.write("**Allergens:**", ', '.join(allergens) if allergens else 'None detected')
                    ingredients = product.get('ingredients', [])
                    st.write("**Ingredients:**", ', '.join(ingredients[:10]) if ingredients else 'N/A')

                st.subheader("🥗 Nutrition Information")
                ncols = st.columns(4)
                for i, (key, value) in enumerate(nutrition.items()):
                    with ncols[i % 4]:
                        st.metric(key.replace('_',' ').title(), str(value) if value else 'N/A')

                if show_charts and nutrition:
                    pie_chart = create_nutrition_pie(nutrition)
                    if pie_chart:
                        st.plotly_chart(pie_chart, use_container_width=True)

                st.subheader("📋 FSSAI License Verification")
                if fssai.get('valid'):
                    st.success(f"✅ {fssai.get('message','Valid')}: {fssai.get('number','')}")
                else:
                    st.error(f"❌ {fssai.get('message','Invalid')}")

                with st.expander("View FSSAI Details"):
                    for k, v in fssai.get('details', {}).items():
                        st.write(f"**{k.replace('_',' ').title()}:** {v}")

                st.subheader("🧪 Additive Detection")
                if additives:
                    add_col1, add_col2 = st.columns([1,1])
                    with add_col1:
                        add_chart = create_additives_chart(additives)
                        if add_chart:
                            st.plotly_chart(add_chart, use_container_width=True)
                    with add_col2:
                        for a in additives:
                            risk = a.get('risk_level','Safe')
                            color_map = {
                                'Safe':'#10b981',
                                'Moderate':'#f59e0b',
                                'High Concern':'#ef4444'
                            }
                            color = color_map.get(risk,'#666')
                            st.markdown(f"""
                            <div style="padding:10px;border-left:4px solid {color};
                                 background:#0f1629;margin:5px 0;border-radius:5px;">
                                <b style="color:white;">{a['ins']} — {a['name']}</b><br>
                                <span style="color:#94a3b8;">Category: {a.get('category','N/A')}</span><br>
                                Risk: <span style="color:{color}"><b>{risk}</b></span><br>
                                <small style="color:#64748b;">{a.get('concerns','')}</small>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("✅ No INS-numbered additives detected")

                if report.get('ingredient_analysis'):
                    st.subheader("🧠 AI Ingredient Analysis")
                    st.info(report['ingredient_analysis'])

                if show_verbose and report.get('raw_text'):
                    with st.expander("📝 Raw OCR Text"):
                        st.text(report['raw_text'])

                st.subheader("💾 Export Report")
                dl_col1, dl_col2, dl_col3 = st.columns(3)
                with dl_col1:
                    pdf_buffer = generate_pdf_report(report)
                    st.download_button(
                        label="📄 PDF Report",
                        data=pdf_buffer,
                        file_name=f"{result['name']}_report.pdf",
                        mime="application/pdf"
                    )
                with dl_col2:
                    st.download_button(
                        label="📊 JSON Report",
                        data=json.dumps(report, indent=2, default=str),
                        file_name=f"{result['name']}_report.json",
                        mime="application/json"
                    )
                with dl_col3:
                    st.download_button(
                        label="📈 CSV Report",
                        data=generate_csv(report),
                        file_name=f"{result['name']}_report.csv",
                        mime="text/csv"
                    )

        if len(results) > 1:
            st.markdown("---")
            st.markdown("## 🔄 Product Comparison")
            comparison_chart = create_comparison_chart(
                st.session_state.analysis_history[-len(results):]
            )
            if comparison_chart:
                st.plotly_chart(comparison_chart, use_container_width=True)

            comparison_data = []
            for item in st.session_state.analysis_history[-len(results):]:
                r = item.get('report', {})
                product = r.get('product_info', {})
                nutrition = product.get('nutrition', {})
                comparison_data.append({
                    'Product': item['name'],
                    'Risk Score': item['risk_score'],
                    'Energy': nutrition.get('energy','N/A'),
                    'Protein': nutrition.get('protein','N/A'),
                    'Sugar': nutrition.get('sugar','N/A'),
                    'Fat': nutrition.get('fat','N/A'),
                    'Sodium': nutrition.get('sodium','N/A'),
                    'Additives': len(r.get('additives',[])),
                    'FSSAI': r.get('fssai',{}).get('message','N/A'),
                })
            st.dataframe(pd.DataFrame(comparison_data), use_container_width=True)

# ===========================
# FOOTER
# ===========================
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#64748b;'>ProductPower FSSAI © 2024 | Made with ❤️</p>",
    unsafe_allow_html=True
)