APP_CSS = """
<style>
:root {
    --bg: #030712;
    --panel: rgba(15, 23, 42, .68);
    --line: rgba(148, 163, 184, .22);
    --teal: #00d4aa;
    --sky: #38bdf8;
    --violet: #a78bfa;
    --danger: #ef4444;
    --success: #22c55e;
}

.stApp {
    background:
        radial-gradient(circle at 16% 12%, rgba(0, 212, 170, .15), transparent 30%),
        radial-gradient(circle at 84% 6%, rgba(167, 139, 250, .16), transparent 28%),
        linear-gradient(135deg, #030712 0%, #07111f 48%, #030712 100%);
    color: #e5f5ff;
}

/* RTL Support for Arabic */
.rtl-container {
    direction: rtl;
    text-align: right;
}
.rtl-container .glass-card, 
.rtl-container .hero, 
.rtl-container .friendly-note,
.rtl-container .step-card {
    text-align: right !important;
}
.rtl-container .metric-label,
.rtl-container .metric-value,
.rtl-container .metric-note {
    text-align: right !important;
}
.rtl-container .pipeline-grid,
.rtl-container .metric-grid {
    direction: rtl !important;
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background: linear-gradient(115deg, transparent, rgba(56,189,248,.08), transparent);
    animation: scanGlow 12s ease-in-out infinite;
}

@keyframes scanGlow {
    0%, 100% { transform: translateX(-30%); opacity: .45; }
    50% { transform: translateX(30%); opacity: .85; }
}

[data-testid="stSidebar"] {
    background: rgba(3, 7, 18, .92);
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] * {
    color: #dbeafe;
}

h1, h2, h3 {
    letter-spacing: 0;
    color: #f8fbff;
}

.hero {
    border: 1px solid rgba(56, 189, 248, .24);
    border-radius: 12px;
    padding: 32px;
    background: linear-gradient(135deg, rgba(15, 23, 42, .85), rgba(14, 116, 144, .25));
    box-shadow: 0 25px 80px rgba(0, 212, 170, .1);
    backdrop-filter: blur(24px);
    margin-bottom: 24px;
    border-left: 5px solid var(--teal);
}

.hero .eyebrow {
    color: var(--teal);
    font-weight: 800;
    text-transform: uppercase;
    font-size: .85rem;
    letter-spacing: 1.2px;
}

.hero h1 {
    font-size: clamp(2.2rem, 5vw, 4.2rem);
    line-height: 1.1;
    margin: 12px 0 14px;
    font-weight: 800;
}

.hero p {
    color: #cbd5e1;
    font-size: 1.1rem;
    max-width: 900px;
    line-height: 1.6;
}

.glass-card {
    border: 1px solid rgba(148, 163, 184, .25);
    border-radius: 12px;
    padding: 22px;
    background: rgba(15, 23, 42, .65);
    box-shadow: 0 20px 60px rgba(0, 0, 0, .3);
    backdrop-filter: blur(20px);
    transition: all .3s cubic-bezier(0.4, 0, 0.2, 1);
    min-height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.glass-card:hover {
    transform: translateY(-6px);
    border-color: var(--teal);
    box-shadow: 0 20px 70px rgba(0, 212, 170, .15);
    background: rgba(15, 23, 42, .75);
}

.metric-label {
    color: #94a3b8;
    font-size: .8rem;
    text-transform: uppercase;
    font-weight: 800;
    letter-spacing: 0.5px;
}

.metric-value {
    font-size: clamp(1.4rem, 2.5vw, 2.4rem);
    font-weight: 900;
    color: #ffffff;
    margin-top: 10px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.metric-note {
    color: #64748b;
    font-size: .85rem;
    margin-top: 10px;
    line-height: 1.5;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 14px;
    margin: 12px 0 18px;
    width: 100%;
}

.status-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: 14px;
    margin: 12px 0 18px;
    width: 100%;
}

.pipeline-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 14px;
    margin: 12px 0 18px;
    width: 100%;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border: 1px solid rgba(0, 212, 170, .34);
    background: rgba(0, 212, 170, .1);
    color: #bfffea;
    padding: 8px 11px;
    border-radius: 999px;
    font-size: .84rem;
}

.ai-button button {
    border: 1px solid rgba(0, 212, 170, .55) !important;
    background: linear-gradient(90deg, #00d4aa, #38bdf8, #a78bfa) !important;
    color: #020617 !important;
    font-weight: 900 !important;
    box-shadow: 0 0 28px rgba(0, 212, 170, .32) !important;
}

[data-testid="stFormSubmitButton"] button {
    border: 1px solid rgba(0, 212, 170, .55) !important;
    background: linear-gradient(90deg, #00d4aa, #38bdf8, #a78bfa) !important;
    color: #020617 !important;
    font-weight: 900 !important;
    box-shadow: 0 0 28px rgba(0, 212, 170, .32) !important;
}

.pipeline-node {
    border: 1px solid rgba(56, 189, 248, .3);
    border-radius: 8px;
    padding: 14px;
    background: rgba(8, 47, 73, .36);
    min-height: 108px;
    overflow: hidden;
    overflow-wrap: anywhere;
}

.pipeline-node strong {
    color: #e0f2fe;
}

.danger {
    border-color: rgba(239, 68, 68, .48);
    background: rgba(127, 29, 29, .36);
}

.success {
    border-color: rgba(34, 197, 94, .48);
    background: rgba(20, 83, 45, .34);
}

.small-muted {
    color: #94a3b8;
    font-size: .86rem;
    line-height: 1.45;
    overflow-wrap: anywhere;
}

.friendly-note {
    border: 1px solid rgba(56, 189, 248, .24);
    border-radius: 8px;
    padding: 14px 16px;
    background: rgba(8, 47, 73, .32);
    color: #dbeafe;
    line-height: 1.55;
    margin: 10px 0 18px;
}

.step-card {
    border: 1px solid rgba(148, 163, 184, .18);
    border-radius: 8px;
    padding: 16px;
    background: rgba(15, 23, 42, .48);
    min-height: 120px;
}

.step-card strong {
    color: #f8fafc;
    display: block;
    margin: 8px 0 6px;
}

[data-testid="stMetric"] {
    background: rgba(15,23,42,.48);
    border: 1px solid rgba(148,163,184,.18);
    padding: 14px;
    border-radius: 8px;
}

[data-testid="stProgress"] p {
    color: #bfdbfe !important;
    font-weight: 650;
}

[data-testid="stWidgetLabel"] *,
[data-testid="stSlider"] *,
[data-testid="stToggle"] *,
[data-baseweb="select"] * {
    color: #dbeafe !important;
}

[data-baseweb="select"] input,
[data-baseweb="select"] div {
    color: #0f172a !important;
}

button, input, textarea, select {
    border-radius: 8px !important;
}

button, label, p, span, div {
    overflow-wrap: anywhere;
}

[data-testid="stDataFrame"] {
    max-width: 100%;
    overflow: auto;
}

@media (max-width: 620px) {
    .hero {
        padding: 20px;
    }

    .metric-grid,
    .status-grid,
    .pipeline-grid {
        grid-template-columns: 1fr;
    }
}

@media (min-width: 700px) and (max-width: 1050px) {
    .main .block-container,
    [data-testid="stMain"] .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-left: 21rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
}
</style>
"""
