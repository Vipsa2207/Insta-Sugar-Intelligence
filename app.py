# ---------------------------------------------------------------
# Insta Sugar Intelligence  |  Streamlit app  |  Part 1
# Page design, logo, sidebar filters and the Overview tab
# ---------------------------------------------------------------
import base64
import re
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

# ---------- 1. Paths and constants ----------
ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "sugar_instagram_clean.csv"
ASSETS = ROOT / "assets"

BLACK, PINK, DEEP_PINK, CREAM = "#111111", "#EBB7B0", "#C75B6B", "#FFFBF9"
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

FORMAT_ICON = {"Reel": "🎞️", "Story": "📱", "Video": "🎥", "Image": "🖼️"}
CAMPAIGN_ICON = {"Giveaway": "🎁", "Tutorial": "🎓", "Festive Offer": "🪔",
                 "Product Launch": "🚀", "Influencer Collab": "🤝"}
EMOTION_ICON = {"Curious": "🤔", "Confident": "😎", "Happy": "😊",
                "Excited": "🤩", "Inspired": "✨"}
SOURCE_ICON = {"Organic": "🌱", "Paid": "💰", "Collab": "👯", "Influencer": "🌟"}

st.set_page_config(
    page_title="Insta Sugar Intelligence",
    page_icon=Image.open(ASSETS / "favicon.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- 2. Styling (CSS) ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stMarkdown, button { font-family: 'Poppins', sans-serif; }
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 1.6rem; max-width: 1400px; }

/* brand header */
.brand-bar { display:flex; align-items:center; gap:22px; }
.brand-logo { height:84px; }
.brand-title { font-size:2.7rem; font-weight:800; margin:0; letter-spacing:-0.5px; color:#111; }
.brand-title span { color:#C75B6B; }
.brand-line { height:4px; border-radius:4px; margin:14px 0 18px 0;
              background:linear-gradient(90deg,#111 0%,#C75B6B 45%,#EBB7B0 100%); }

/* tabs */
.stTabs [data-baseweb="tab-list"] { gap:8px; flex-wrap:wrap; }
.stTabs [data-baseweb="tab"] { background:#F7DED9; border-radius:999px; padding:8px 18px; height:auto; font-weight:600; }
.stTabs [aria-selected="true"] { background:#111; }
.stTabs [aria-selected="true"] p { color:#EBB7B0 !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display:none; }

/* sidebar */
section[data-testid="stSidebar"] { border-right:3px solid #111; }
.side-logo { text-align:center; margin:4px 0 6px 0; }
.side-logo img { width:92px; }
.side-title { text-align:center; font-weight:800; letter-spacing:3px; font-size:0.85rem; margin-bottom:14px; }
.flabel { font-weight:700; font-size:0.92rem; margin:14px 0 4px 0; }
.counter { background:#111; color:#EBB7B0; border-radius:16px; padding:12px 14px; text-align:center;
           font-weight:700; margin-top:16px; }
.counter small { display:block; color:#fff; font-weight:400; opacity:.8; }
button[data-testid^="stBaseButton-pills"] { border:1.5px solid #111 !important; border-radius:999px !important; }
button[data-testid="stBaseButton-pillsActive"] { background:#111 !important; color:#EBB7B0 !important; }

/* KPI cards */
.kpi { background:#fff; border-radius:20px; padding:16px 18px; box-shadow:0 4px 14px rgba(17,17,17,.08);
       border-left:7px solid #EBB7B0; min-height:128px; }
.kpi-label { font-size:.72rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:#555; }
.kpi-value { font-size:2rem; font-weight:800; line-height:1.15; margin:4px 0 2px 0; }
.kpi-note { font-size:.78rem; color:#666; }
.kpi-note.good { color:#1E7F4F; font-weight:600; }
.kpi-note.bad { color:#B3261E; font-weight:600; }

/* insight cards */
.ins { background:#fff; border-radius:20px; padding:16px 20px; box-shadow:0 4px 14px rgba(17,17,17,.08); height:100%; }
.ins h4 { margin:0 0 8px 0; font-size:1rem; }
.ins p { margin:0 0 6px 0; font-size:.88rem; line-height:1.45; }
.ins.good { border-top:6px solid #2E9D68; }
.ins.warn { border-top:6px solid #E0A100; }
.ins.act  { border-top:6px solid #111; }
.sec-title { font-size:1.25rem; font-weight:800; margin:22px 0 8px 0; }
.footnote { font-size:.75rem; color:#666; margin-top:26px; border-top:1px solid #E5D5D0; padding-top:10px; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------- 3. Data ----------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["Post Date"])
    df["Weekday"] = pd.Categorical(df["Weekday"], categories=WEEKDAYS, ordered=True)
    return df


@st.cache_data
def img_b64(name):
    return base64.b64encode((ASSETS / name).read_bytes()).decode()


df = load_data()
TOTAL_POSTS = len(df)
BASE_ER = df["Engagement Rate"].mean()
BASE_STD = df["Engagement Rate"].std()
MIN_D, MAX_D = df["Post Date"].min().date(), df["Post Date"].max().date()
HASHTAGS = sorted({h for row in df["Hashtags"].str.split(", ") for h in row})


def human(n):
    if abs(n) >= 1e9:
        return f"{n / 1e9:.2f}B"
    if abs(n) >= 1e6:
        return f"{n / 1e6:.1f}M"
    if abs(n) >= 1e3:
        return f"{n / 1e3:.1f}K"
    return f"{n:,.0f}"


def style_fig(fig, height=360):
    fig.update_layout(
        height=height, margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Poppins, sans-serif", color=BLACK),
        title=dict(font=dict(size=16)), colorway=[BLACK, PINK, DEEP_PINK],
    )
    fig.update_xaxes(gridcolor="#EADBD7")
    fig.update_yaxes(gridcolor="#EADBD7")
    return fig


# ---------- 4. Header (logo + title stay above every tab) ----------
st.markdown(
    f"""
<div class="brand-bar">
  <img class="brand-logo" src="data:image/png;base64,{img_b64('sugar_logo_black.png')}"/>
  <h1 class="brand-title">Insta <span>Sugar</span> Intelligence</h1>
</div>
<div class="brand-line"></div>
""",
    unsafe_allow_html=True,
)

# ---------- 5. Sidebar filters ----------
FILTER_KEYS = ["f_format", "f_campaign", "f_emotion", "f_source", "f_hashtag"]


def reset_filters():
    st.session_state["f_dates"] = (MIN_D, MAX_D)
    for k in FILTER_KEYS:
        st.session_state[k] = []


if "f_dates" not in st.session_state:
    st.session_state["f_dates"] = (MIN_D, MAX_D)

with st.sidebar:
    st.markdown(
        f"""<div class="side-logo"><img src="data:image/png;base64,{img_b64('sugar_logo_black.png')}"/></div>
<div class="side-title">FILTERS</div>""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="flabel">📅 Posting period</div>', unsafe_allow_html=True)
    date_val = st.date_input("Posting period", min_value=MIN_D, max_value=MAX_D,
                             key="f_dates", label_visibility="collapsed")

    st.markdown('<div class="flabel">🎬 Format</div>', unsafe_allow_html=True)
    sel_format = st.pills("Format", list(FORMAT_ICON), selection_mode="multi", key="f_format",
                          format_func=lambda x: f"{FORMAT_ICON[x]} {x}", label_visibility="collapsed")

    st.markdown('<div class="flabel">🎯 Campaign</div>', unsafe_allow_html=True)
    sel_campaign = st.pills("Campaign", list(CAMPAIGN_ICON), selection_mode="multi", key="f_campaign",
                            format_func=lambda x: f"{CAMPAIGN_ICON[x]} {x}", label_visibility="collapsed")

    st.markdown('<div class="flabel">💭 Audience emotion</div>', unsafe_allow_html=True)
    sel_emotion = st.pills("Emotion", list(EMOTION_ICON), selection_mode="multi", key="f_emotion",
                           format_func=lambda x: f"{EMOTION_ICON[x]} {x}", label_visibility="collapsed")

    st.markdown('<div class="flabel">🤝 Engagement source</div>', unsafe_allow_html=True)
    sel_source = st.pills("Source", list(SOURCE_ICON), selection_mode="multi", key="f_source",
                          format_func=lambda x: f"{SOURCE_ICON[x]} {x}", label_visibility="collapsed")

    st.markdown('<div class="flabel">#️⃣ Hashtags</div>', unsafe_allow_html=True)
    sel_hashtag = st.pills("Hashtags", HASHTAGS, selection_mode="multi", key="f_hashtag",
                           format_func=lambda x: f"🏷️ {x}", label_visibility="collapsed")

    st.caption("Tap to filter. Nothing selected means all.")
    st.button("↺  Reset all filters", on_click=reset_filters, width="stretch")

# ---------- 6. Apply the filters ----------
if isinstance(date_val, (tuple, list)) and len(date_val) == 2:
    start, end = date_val
elif isinstance(date_val, (tuple, list)) and len(date_val) == 1:
    start, end = date_val[0], MAX_D
else:
    start, end = date_val, MAX_D

mask = (df["Post Date"].dt.date >= start) & (df["Post Date"].dt.date <= end)
if sel_format:
    mask &= df["Post Type"].isin(sel_format)
if sel_campaign:
    mask &= df["Campaign Type"].isin(sel_campaign)
if sel_emotion:
    mask &= df["Audience Emotion"].isin(sel_emotion)
if sel_source:
    mask &= df["Engagement Source"].isin(sel_source)
if sel_hashtag:
    mask &= df["Hashtags"].str.contains("|".join(re.escape(h) for h in sel_hashtag))
f = df[mask]

with st.sidebar:
    st.markdown(
        f'<div class="counter">{len(f):,} posts<small>of {TOTAL_POSTS:,} selected</small></div>',
        unsafe_allow_html=True,
    )

if len(f) == 0:
    st.warning("No posts match these filters. Try removing one, or press Reset.")
    st.stop()

# ---------- 7. Tabs ----------
tab_names = ["🏠 Overview", "📈 Trends", "🏆 Top Posts", "🎬 Format Lab",
             "🔻 Funnel", "#️⃣ Hashtags", "🧪 Recipe Lab", "💡 Insights"]
tabs = st.tabs(tab_names)

# ===== Tab 1: Overview =====
with tabs[0]:
    n = len(f)
    avg_er = f["Engagement Rate"].mean()
    diff = avg_er - BASE_ER
    margin = 1.96 * BASE_STD / np.sqrt(n)
    beyond = abs(diff) > margin

    likes_share = f["Likes"].sum() / f["Total Engagement"].sum() * 100
    saves_shares = (f["Saves"].sum() + f["Shares"].sum()) / f["Total Engagement"].sum() * 100

    if beyond:
        er_note = f"{diff:+.2f} vs overall {BASE_ER:.2f}% (beyond margin)"
        er_tone = "good" if diff > 0 else "bad"
    else:
        er_note = f"{diff:+.2f} vs overall {BASE_ER:.2f}% (within normal range)"
        er_tone = ""

    st.markdown('<div class="sec-title">📊 Key numbers for your selection</div>', unsafe_allow_html=True)

    def kpi(label, value, note="", tone=""):
        return (f'<div class="kpi"><div class="kpi-label">{label}</div>'
                f'<div class="kpi-value">{value}</div><div class="kpi-note {tone}">{note}</div></div>')

    c = st.columns(4)
    c[0].markdown(kpi("Posts", f"{n:,}", f"{n / TOTAL_POSTS:.0%} of all posts"), unsafe_allow_html=True)
    c[1].markdown(kpi("Impressions", human(f["Impressions"].sum()), "times posts were shown"), unsafe_allow_html=True)
    c[2].markdown(kpi("Post-level reach", human(f["Reach"].sum()), "same person can repeat"), unsafe_allow_html=True)
    c[3].markdown(kpi("Total interactions", human(f["Total Engagement"].sum()),
                      "likes + comments + shares + saves"), unsafe_allow_html=True)

    st.write("")
    c = st.columns(4)
    c[0].markdown(kpi("Avg engagement rate", f"{avg_er:.2f}%", er_note, er_tone), unsafe_allow_html=True)
    c[1].markdown(kpi("Median engagement rate", f"{f['Engagement Rate'].median():.2f}%",
                      "the middle post"), unsafe_allow_html=True)
    c[2].markdown(kpi("Profile visit rate", f"{f['Profile Visit Rate'].mean():.2f}%",
                      "of reached accounts visit"), unsafe_allow_html=True)
    c[3].markdown(kpi("Follow conversion", f"{f['Follow Conversion'].mean():.1f}%",
                      "of profile visitors follow"), unsafe_allow_html=True)

    st.markdown('<div class="sec-title">🔍 What people do, and how posts vary</div>', unsafe_allow_html=True)
    left, right = st.columns(2)

    mix = f[["Likes", "Comments", "Shares", "Saves"]].sum()
    mix_pct = (mix / mix.sum() * 100).round(1)
    fig_mix = px.bar(x=mix_pct.index, y=mix_pct.values, text=mix_pct.values,
                     title="Share of all interactions (%)")
    fig_mix.update_traces(texttemplate="%{text}%", textposition="outside", cliponaxis=False,
                          marker_color=[BLACK, PINK, DEEP_PINK, "#8C6A66"])
    fig_mix.update_layout(xaxis_title=None, yaxis_title=None)
    fig_mix.update_yaxes(range=[0, 100])
    left.plotly_chart(style_fig(fig_mix), width="stretch")

    fig_hist = px.histogram(f, x="Engagement Rate", nbins=40, title="How engagement rate varies from post to post")
    fig_hist.update_traces(marker_color=PINK, marker_line_color=BLACK, marker_line_width=0.5)
    fig_hist.add_vline(x=avg_er, line_color=BLACK, line_width=3,
                       annotation_text=f"selection avg {avg_er:.1f}%", annotation_position="top left")
    fig_hist.add_vline(x=BASE_ER, line_dash="dash", line_color=DEEP_PINK,
                       annotation_text=f"overall {BASE_ER:.1f}%", annotation_position="top right")
    fig_hist.update_layout(xaxis_title="Engagement rate (%)", yaxis_title="Posts")
    right.plotly_chart(style_fig(fig_hist), width="stretch")

    # insight cards: what is good, what to watch, what to do
    st.markdown('<div class="sec-title">💡 Quick read</div>', unsafe_allow_html=True)
    good = [
        f"Average engagement rate is <b>{avg_er:.2f}%</b>, "
        + ("clearly different from" if beyond else "in line with")
        + f" the overall {BASE_ER:.2f}%.",
        f"About <b>{f['Profile Visit Rate'].mean():.1f}%</b> of reached accounts visit the profile, "
        f"and <b>{f['Follow Conversion'].mean():.0f}%</b> of those visitors follow.",
    ]
    warn = [
        f"Likes are <b>{likes_share:.0f}%</b> of all interactions. Saves and shares, the stronger signals, "
        f"are only <b>{saves_shares:.0f}%</b>.",
        f"Margin of error here is about <b>±{margin:.2f}</b> points, so smaller gaps are likely luck.",
    ]
    if n < 500:
        warn.append("This is a small selection, so treat the numbers with care.")
    act = [
        "Add clear calls to action such as <b>save this for later</b> and <b>tap our profile</b>.",
        "Judge content by engagement rate, not by likes, and test ideas before changing strategy.",
    ]
    cols = st.columns(3)
    for col, cls, title, items in zip(
        cols, ["good", "warn", "act"], ["✅ What looks good", "⚠️ Watch out", "🎯 What to do"], [good, warn, act]
    ):
        col.markdown(
            f'<div class="ins {cls}"><h4>{title}</h4>' + "".join(f"<p>• {i}</p>" for i in items) + "</div>",
            unsafe_allow_html=True,
        )

# ===== Other tabs (built in the next steps) =====
for t in tabs[1:]:
    with t:
        st.info("This tab is added in the next step.")

st.markdown(
    '<div class="footnote">Data: 50,000 post records, 19 Apr 2024 to 19 Apr 2025, provided by the LabMatics mentor. '
    "Engagement rate = (likes + comments + shares + saves) ÷ reach × 100. "
    "The data has no caption or post ID and looks synthetic. Results show association, not cause.</div>",
    unsafe_allow_html=True,
)
