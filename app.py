# ---------------------------------------------------------------
# Insta Sugar Intelligence  |  Streamlit app  |  Full app
# Page design, logo, sidebar filters and all 8 tabs
# ---------------------------------------------------------------
import base64
import re
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from scipy import stats

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
.stTabs [data-baseweb="tab"], .stTabs button[role="tab"], .stTabs [data-testid="stTab"] { background:#F7DED9; border-radius:999px; padding:8px 18px; height:auto; font-weight:600; }
.stTabs .react-aria-SelectionIndicator { display:none !important; }
.stTabs [aria-selected="true"] { background:#111 !important; }
.stTabs [aria-selected="true"] p, .stTabs [aria-selected="true"] span { color:#EBB7B0 !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display:none; }

/* sidebar */
section[data-testid="stSidebar"] { border-right:3px solid #111; }
.side-head { display:flex; align-items:center; gap:14px; margin:0 0 2px 0; }
.side-head img { width:58px; }
.side-head span { font-weight:800; letter-spacing:4px; font-size:1rem; }
/* calendar pop-up: never taller than the window, scrolls if the window is short */
div[data-baseweb="popover"]:has([data-baseweb="calendar"]) { max-height: 88vh; overflow-y: auto; }
.flabel { font-weight:700; font-size:0.92rem; margin:14px 0 4px 0; }
button[data-testid^="stBaseButton-pills"], button[data-variant="pills"] { border:1.5px solid #111 !important; border-radius:999px !important; }
button[data-testid="stBaseButton-pillsActive"], button[data-variant="pills"][aria-checked="true"] { background:#111 !important; color:#EBB7B0 !important; }
button[data-testid="stBaseButton-pillsActive"] p, button[data-variant="pills"][aria-checked="true"] p { color:#EBB7B0 !important; }

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

/* read box: insight / so what / action */
.read3 { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin:10px 0 6px 0; }
.read3 > div { background:#fff; border-radius:18px; padding:14px 18px; box-shadow:0 4px 14px rgba(17,17,17,.08); font-size:.88rem; line-height:1.5; }
.read3 b.t { display:block; font-size:.78rem; letter-spacing:1px; text-transform:uppercase; margin-bottom:4px; }
.read3 > div:nth-child(1) { border-top:6px solid #EBB7B0; }
.read3 > div:nth-child(2) { border-top:6px solid #C75B6B; }
.read3 > div:nth-child(3) { border-top:6px solid #111; }
@media (max-width: 900px) { .read3 { grid-template-columns:1fr; } }
/* verdict card */
.vcard { border-radius:22px; padding:20px 24px; background:#fff; box-shadow:0 4px 14px rgba(17,17,17,.1); border-left:10px solid #E0A100; }
.vcard.do { border-left-color:#2E9D68; } .vcard.dont { border-left-color:#B3261E; }
.vcard .v { font-size:2rem; font-weight:800; }
.vcard .m { font-size:.9rem; color:#444; margin-top:6px; line-height:1.5; }
.pillrow span { display:inline-block; background:#F7DED9; border-radius:999px; padding:4px 12px; margin:4px 6px 0 0; font-size:.8rem; font-weight:600; }
.dd { background:#fff; border-radius:18px; padding:14px 20px; box-shadow:0 4px 14px rgba(17,17,17,.08); height:100%; }
.dd h4 { margin:0 0 8px 0; } .dd p { margin:0 0 6px 0; font-size:.88rem; line-height:1.45; }
.dd.do { border-top:6px solid #2E9D68; } .dd.dont { border-top:6px solid #B3261E; } .dd.test { border-top:6px solid #E0A100; }
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
    fig.update_traces(textangle=0, selector=dict(type="bar"))
    # numbers above bars: remove horizontal gridlines so no line runs through a number
    if any(t.type == "bar" and getattr(t, "textposition", None) == "outside" for t in fig.data):
        fig.update_yaxes(showgrid=False)
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
        f"""<div class="side-head"><img src="data:image/png;base64,{img_b64('sugar_logo_black.png')}"/>
<span>FILTERS</span></div>""",
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

if len(f) == 0:
    st.warning("No posts match these filters. Try removing one, or press Reset.")
    st.stop()

# ---------- 7. Helpers used by the tabs ----------
def group_stats(data, col):
    g = (data.groupby(col, observed=True)["Engagement Rate"]
         .agg(["mean", "std", "count"]).reset_index())
    g["std"] = g["std"].fillna(0)
    g["margin"] = 1.96 * g["std"] / np.sqrt(g["count"])
    return g


def luck_p(data, col):
    groups = [x["Engagement Rate"].values for _, x in data.groupby(col, observed=True) if len(x) >= 2]
    if len(groups) < 2:
        return None
    return float(stats.f_oneway(*groups).pvalue)


def p_sentence(p):
    if p is None:
        return "There are not enough groups to run the luck test."
    if p < 0.05:
        return f"The luck test gives p = {p:.3f}, below 0.05, so the gaps are unlikely to be only luck."
    return f"The luck test gives p = {p:.3f}, above 0.05, so the gaps could easily be luck."


def read_box(insight, so_what, action):
    st.markdown(
        '<div class="read3">'
        f'<div><b class="t">🔎 Insight</b>{insight}</div>'
        f'<div><b class="t">🤔 So what</b>{so_what}</div>'
        f'<div><b class="t">🎯 Action</b>{action}</div></div>',
        unsafe_allow_html=True,
    )


def er_bar(g, xcol, title, order=None, height=380):
    fig = px.bar(g, x=xcol, y="mean", error_y="margin", text=g["mean"].round(2), title=title,
                 category_orders={xcol: order} if order else None)
    fig.update_traces(marker_color=PINK, marker_line_color=BLACK, marker_line_width=1,
                      textposition="inside", insidetextanchor="middle", textangle=0, error_y_color=BLACK)
    fig.add_hline(y=BASE_ER, line_dash="dash", line_color=DEEP_PINK,
                  annotation_text=f"overall {BASE_ER:.2f}%", annotation_position="top left")
    fig.update_yaxes(range=[0, 26], title="Average engagement rate (%)")
    fig.update_xaxes(title=None)
    return style_fig(fig, height)


@st.cache_data
def recipe_table():
    cols = ["Post Type", "Campaign Type", "Audience Emotion", "Engagement Source"]
    rows = []
    for keys, sub in df.groupby(cols):
        n_, avg, lift, margin_, z = score(sub)
        rows.append(dict(zip(cols, keys)) | {"Posts": n_, "Avg_ER": avg, "Lift": lift,
                                              "Margin": margin_, "z": z, "Verdict": verdict(n_, z)})
    return pd.DataFrame(rows)


@st.cache_data
def shuffle_check(runs=1000):
    cols = ["Post Type", "Campaign Type", "Audience Emotion", "Engagement Source"]
    codes = df.groupby(cols).ngroup().values
    k = codes.max() + 1
    n_posts = np.bincount(codes, minlength=k)
    er = df["Engagement Rate"].values
    rng = np.random.default_rng(42)

    def zs(values):
        avg = np.bincount(codes, weights=values, minlength=k) / n_posts
        return (avg - BASE_ER) / (BASE_STD / np.sqrt(n_posts))

    real = int((np.abs(zs(er)) >= Z_HINT).sum())
    shuffled = [int((np.abs(zs(rng.permutation(er))) >= Z_HINT).sum()) for _ in range(runs)]
    return real, float(np.mean(shuffled))


def posts_needed(lift_pp, alpha=0.05, power=0.8):
    z_a, z_b = stats.norm.ppf(1 - alpha / 2), stats.norm.ppf(power)
    return int(np.ceil(2 * ((z_a + z_b) * BASE_STD / lift_pp) ** 2))


# Recipe Lab rules (same as in the Colab notebook)
RECIPE_COLS = ["Post Type", "Campaign Type", "Audience Emotion", "Engagement Source"]
N_RECIPES = df.groupby(RECIPE_COLS).ngroups
Z_STRICT = float(stats.norm.ppf(1 - 0.05 / (2 * N_RECIPES)))
Z_HINT = 1.96
MIN_POSTS = 30


def score(sub):
    n_ = len(sub)
    avg = sub["Engagement Rate"].mean()
    lift = avg - BASE_ER
    se = BASE_STD / np.sqrt(n_)
    return n_, avg, lift, 1.96 * se, lift / se


def verdict(n_, z):
    if n_ < MIN_POSTS:
        return "⚪ TOO FEW POSTS"
    if z >= Z_STRICT:
        return "🟢 DO"
    if z <= -Z_STRICT:
        return "🔴 DON'T"
    if z >= Z_HINT:
        return "🟡 TEST (leans up)"
    if z <= -Z_HINT:
        return "🟡 TEST (leans down)"
    return "🟡 TEST"


# ---------- 8. Tabs ----------
tab_names = ["🏠 Overview", "📈 Trends", "🏆 Top Posts", "🎬 Format Lab",
             "🔻 Funnel", "#️⃣ Hashtags", "🧪 Recipe Lab", "💡 Insights"]
tabs = st.tabs(tab_names)
n = len(f)

# ===== Tab 1: Overview =====
with tabs[0]:
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

    fig_hist = px.histogram(f, x="Engagement Rate", nbins=40,
                            title=f"How engagement rate varies (black line: selection {avg_er:.1f}%, dashed: overall {BASE_ER:.1f}%)")
    fig_hist.update_traces(marker_color=PINK, marker_line_color=BLACK, marker_line_width=0.5)
    fig_hist.add_vline(x=avg_er, line_color=BLACK, line_width=3)
    fig_hist.add_vline(x=BASE_ER, line_dash="dash", line_color=DEEP_PINK, line_width=3)
    fig_hist.update_layout(xaxis_title="Engagement rate (%)", yaxis_title="Posts")
    fig_hist.update_layout(title=dict(font=dict(size=13)))
    right.plotly_chart(style_fig(fig_hist), width="stretch")

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

# ===== Tab 2: Trends =====
with tabs[1]:
    st.caption(f"Based on {n:,} selected posts")
    days_in_month = df.groupby("Year-Month")["Post Date"].nunique()
    partial = df.groupby("Year-Month")["Is Partial Month"].first()
    m = (f.groupby("Year-Month")["Engagement Rate"].agg(["mean", "count"]).reset_index())
    m["Days"] = m["Year-Month"].map(days_in_month)
    m["Posts per day"] = (m["count"] / m["Days"]).round(1)
    m["Month type"] = np.where(m["Year-Month"].map(partial), "Partial month", "Full month")

    st.markdown('<div class="sec-title">📅 Posting and performance by month</div>', unsafe_allow_html=True)
    l, r = st.columns(2)
    fig = px.bar(m, x="Year-Month", y="Posts per day", color="Month type",
                 color_discrete_map={"Full month": PINK, "Partial month": "#B9A5A1"},
                 title="Posts per day (partial months shown in grey)", hover_data=["Days"],
                 category_orders={"Year-Month": sorted(m["Year-Month"])})
    fig.update_layout(xaxis_title=None, showlegend=False)
    fig.update_xaxes(type="category", tickangle=-45)
    l.plotly_chart(style_fig(fig, 400), width="stretch")

    fig = px.line(m, x="Year-Month", y="mean", markers=True, title="Average engagement rate by month")
    fig.update_traces(line_color=BLACK, marker_color=DEEP_PINK, marker_size=9)
    fig.add_hline(y=BASE_ER, line_dash="dash", line_color=DEEP_PINK)
    fig.update_yaxes(range=[0, 26], title="Engagement rate (%)")
    fig.update_xaxes(type="category", tickangle=-45, title=None)
    fig = style_fig(fig, 400)
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=90))
    r.plotly_chart(fig, width="stretch")

    st.markdown('<div class="sec-title">🗓️ Best day of the week</div>', unsafe_allow_html=True)
    gd = group_stats(f, "Weekday")
    pd_ = luck_p(f, "Weekday")
    l, r = st.columns(2)
    l.plotly_chart(er_bar(gd, "Weekday", "Average engagement rate by weekday (with margin of error)", WEEKDAYS),
                   width="stretch")
    pw = f.groupby("Weekday", observed=True).size().reset_index(name="Posts")
    fig = px.bar(pw, x="Weekday", y="Posts", text="Posts", title="Number of posts by weekday",
                 category_orders={"Weekday": WEEKDAYS})
    fig.update_traces(marker_color=PINK, marker_line_color=BLACK, marker_line_width=1,
                      texttemplate="%{text:,}", textposition="outside", cliponaxis=False)
    fig.update_yaxes(rangemode="tozero", title=None)
    fig.update_xaxes(title=None)
    r.plotly_chart(style_fig(fig), width="stretch")

    best, worst = gd.loc[gd["mean"].idxmax()], gd.loc[gd["mean"].idxmin()]
    gap = best["mean"] - worst["mean"]
    read_box(
        f"<b>{best['Weekday']}</b> scores highest ({best['mean']:.2f}%) and <b>{worst['Weekday']}</b> lowest "
        f"({worst['mean']:.2f}%), a gap of {gap:.2f} points. Posting is steady at about "
        f"{m['Posts per day'].mean():.0f} post records a day. {p_sentence(pd_)}",
        "April 2024 and April 2025 are partial months, so their raw monthly counts look low, but posts per day stay steady. "
        + ("No weekday clearly stands out." if (pd_ is None or pd_ >= 0.05)
           else "There is a weekday pattern worth testing."),
        "Keep a steady posting rhythm and compare months using posts per day. "
        + ("Do not set a 'best day' rule from this data. Test two or three days first."
           if (pd_ is None or pd_ >= 0.05) else "Test the stronger days with similar content before making a rule."),
    )

# ===== Tab 3: Top Posts =====
with tabs[2]:
    st.caption(f"Based on {n:,} selected posts")
    a, b = st.columns([1, 1])
    rank_by = a.segmented_control("Rank posts by", ["Engagement rate", "Likes"],
                                  default="Engagement rate", key="tp_rank") or "Engagement rate"
    top_n = b.slider("How many posts", 5, 20, 10, key="tp_n")
    rank_col = "Engagement Rate" if rank_by == "Engagement rate" else "Likes"
    top = f.nlargest(top_n, rank_col)

    fig = px.bar(top.sort_values(rank_col), x=rank_col, y="Post Label", orientation="h",
                 hover_data=["Reach", "Likes", "Engagement Rate"],
                 title=f"Top {top_n} posts by {rank_by.lower()}")
    fig.update_traces(marker_color=PINK, marker_line_color=BLACK, marker_line_width=1)
    fig.update_layout(yaxis_title=None, xaxis_title=rank_by)
    st.plotly_chart(style_fig(fig, 80 + 34 * top_n), width="stretch")

    show = top[["Post Label", "Engagement Rate", "Likes", "Reach", "Post Type", "Campaign Type",
                "Audience Emotion", "Engagement Source"]].round(2)
    st.dataframe(show, width="stretch", hide_index=True)

    top_reach, all_reach = top["Reach"].mean(), f["Reach"].mean()
    corr_rl = f["Reach"].corr(f["Likes"]) if n > 2 else float("nan")
    corr_re = f["Reach"].corr(f["Engagement Rate"]) if n > 2 else float("nan")
    if rank_col == "Likes":
        read_box(
            f"The {top_n} most-liked posts reached about <b>{top_reach:,.0f}</b> accounts on average, against "
            f"{all_reach:,.0f} for all selected posts. Reach and likes move together (correlation {corr_rl:.2f}).",
            "Likes mostly show which posts had the biggest audience, not which content was best.",
            "Use likes to see audience size. Judge content quality by engagement rate.",
        )
    else:
        read_box(
            f"The {top_n} best posts by engagement rate reached about <b>{top_reach:,.0f}</b> accounts on average "
            f"(all posts: {all_reach:,.0f}). Reach and engagement rate are almost unrelated (correlation {corr_re:.2f}).",
            "Engagement rate shows how well a post connected with the people who saw it. "
            "The top posts come from many formats and campaigns, so there is no single winning formula.",
            "Do not copy one top post. Ten posts out of thousands are not a pattern, so test ideas on purpose.",
        )

# ===== Tab 4: Format Lab =====
with tabs[3]:
    st.caption(f"Based on {n:,} selected posts")
    dim = st.segmented_control("Compare by", ["Post Type", "Campaign Type", "Audience Emotion", "Engagement Source"],
                               default="Post Type", key="fl_dim") or "Post Type"
    g = group_stats(f, dim)
    p_dim = luck_p(f, dim)

    l, r = st.columns(2)
    l.plotly_chart(er_bar(g.sort_values("mean", ascending=False), dim,
                          f"Average engagement rate by {dim.lower()} (with margin of error)", height=520),
                   width="stretch")

    inter = (f.groupby(dim, observed=True)[["Likes", "Comments", "Shares", "Saves"]].mean().reset_index()
             .melt(id_vars=dim, var_name="Interaction", value_name="Average per post"))
    fig = px.bar(inter, x=dim, y="Average per post", facet_col="Interaction", facet_col_wrap=2,
                 facet_row_spacing=0.2, facet_col_spacing=0.14, text="Average per post",
                 color=dim, color_discrete_sequence=[PINK, BLACK, DEEP_PINK, "#8C6A66", "#D9C2BE"],
                 category_orders={"Interaction": ["Likes", "Comments", "Shares", "Saves"]},
                 title="Average interactions per post (each chart has its own scale)")
    fig.update_yaxes(matches=None, showticklabels=True, rangemode="tozero", title=None)
    fig.update_xaxes(title=None, showticklabels=False)
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", textangle=0,
                      textfont=dict(size=11), cliponaxis=False)
    fig.update_layout(legend_title=None, legend=dict(orientation="h", y=-0.1), bargap=0.08)
    ymax = {}
    for tr in fig.data:
        key = tr.yaxis or "y"
        ymax[key] = max(ymax.get(key, 0), float(np.max(tr.y)))
    for key, top_val in ymax.items():
        axis_name = "yaxis" if key == "y" else "yaxis" + key[1:]
        fig.layout[axis_name].range = [0, top_val * 1.3]
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    r.plotly_chart(style_fig(fig, 520), width="stretch")

    tbl = g.rename(columns={"mean": "Avg engagement rate", "count": "Posts", "margin": "Margin of error (±)"})
    tbl = tbl[[dim, "Posts", "Avg engagement rate", "Margin of error (±)"]].round(2)
    st.dataframe(tbl.sort_values("Avg engagement rate", ascending=False), width="stretch", hide_index=True)

    best, worst = g.loc[g["mean"].idxmax()], g.loc[g["mean"].idxmin()]
    gap = best["mean"] - worst["mean"]
    clear = p_dim is not None and p_dim < 0.05
    read_box(
        f"<b>{best[dim]}</b> is highest ({best['mean']:.2f}%) and <b>{worst[dim]}</b> lowest ({worst['mean']:.2f}%), "
        f"a gap of {gap:.2f} points. Each bar has a margin of error of about ±{g['margin'].mean():.2f}. {p_sentence(p_dim)}",
        ("The differences look real, but remember they may come from other factors, so this shows association, not cause."
         if clear else f"{dim} alone does not clearly explain why some posts do better."),
        ("Test the stronger option on similar content before shifting effort."
         if clear else "Choose by message and audience, and run a small test, such as the same content in two options, before changing plans."),
    )

# ===== Tab 5: Funnel =====
with tabs[4]:
    st.caption(f"Based on {n:,} selected posts")
    stages = ["Impressions", "Reach", "Total interactions", "Profile visits", "Follows"]
    vals = [f["Impressions"].sum(), f["Reach"].sum(), f["Total Engagement"].sum(),
            f["Profile Visits"].sum(), f["Follows"].sum()]
    labels = [f"{vals[0] / 1e6:,.1f}M"] + [
        f"{vals[i] / 1e6:,.1f}M<br>{vals[i] / vals[i - 1] * 100:.1f}% of previous" for i in range(1, len(vals))]
    fig = go.Figure(go.Funnel(y=stages, x=[v / 1e6 for v in vals], text=labels, texttemplate="%{text}",
                              marker=dict(color=[BLACK, "#5A3B3B", DEEP_PINK, "#E08C98", PINK])))
    fig.update_layout(title="Engagement funnel: from views to follows (drop-off view)")
    st.plotly_chart(style_fig(fig, 430), width="stretch")

    ft = pd.DataFrame({"Stage": stages, "Total": vals})
    ft["% of previous stage"] = (ft["Total"] / ft["Total"].shift(1) * 100).round(1)
    ft["% of impressions"] = (ft["Total"] / ft["Total"].iloc[0] * 100).round(2)
    ft_show = pd.DataFrame({
        "Stage": ft["Stage"],
        "Total": ft["Total"].map("{:,.0f}".format),
        "% of previous stage": ft["% of previous stage"].map(lambda x: "-" if pd.isna(x) else f"{x:.1f}%"),
        "% of impressions": ft["% of impressions"].map("{:.2f}%".format),
    })
    st.dataframe(ft_show, width="stretch", hide_index=True)

    steps = ft.iloc[1:].reset_index(drop=True)
    drop = steps.loc[steps["% of previous stage"].idxmin()]
    mixp = f[["Likes", "Comments", "Shares", "Saves"]].sum()
    mixp = mixp / mixp.sum() * 100
    read_box(
        f"About {ft.loc[1, '% of previous stage']:.0f}% of impressions reached a different account, and "
        f"{ft.loc[2, '% of previous stage']:.1f}% of reach became an interaction. The weakest step is "
        f"<b>{drop['Stage']}</b> (only {drop['% of previous stage']:.1f}% of the step before). "
        f"Only {ft.loc[4, '% of impressions']:.2f}% of impressions end in a follow. Likes are {mixp['Likes']:.0f}% of interactions.",
        "This is a drop-off view, not a proven journey: the steps count different things, and we cannot show that "
        "one step happens after another. Likes are easy, while saves and shares are stronger signals and are rare.",
        "Add clear calls to action such as 'save this' and 'tap our profile', make saveable content such as tutorials, "
        "and compare the profile visit rate before and after.",
    )

# ===== Tab 6: Hashtags =====
with tabs[5]:
    st.caption(f"Based on {n:,} selected posts")
    hx = f.assign(Hashtag=f["Hashtags"].str.split(", ")).explode("Hashtag")
    gh = group_stats(hx, "Hashtag")
    gc = group_stats(f, "Hashtag Count")
    p_count = luck_p(f, "Hashtag Count")

    l, r = st.columns(2)
    l.plotly_chart(er_bar(gh.sort_values("mean", ascending=False), "Hashtag",
                          "Average engagement rate by hashtag (with margin of error)"), width="stretch")
    gc["Hashtag Count"] = gc["Hashtag Count"].astype(str) + " hashtag(s)"
    r.plotly_chart(er_bar(gc, "Hashtag Count", "Does the number of hashtags matter?"), width="stretch")

    tbl = gh.rename(columns={"mean": "Avg engagement rate", "count": "Posts", "margin": "Margin of error (±)"})
    st.dataframe(tbl[["Hashtag", "Posts", "Avg engagement rate", "Margin of error (±)"]].round(2)
                 .sort_values("Avg engagement rate", ascending=False), width="stretch", hide_index=True)

    bh, wh = gh.loc[gh["mean"].idxmax()], gh.loc[gh["mean"].idxmin()]
    best_c = gc.loc[gc["mean"].idxmax()]
    read_box(
        f"<b>{bh['Hashtag']}</b> is highest ({bh['mean']:.2f}%) and <b>{wh['Hashtag']}</b> lowest ({wh['mean']:.2f}%), "
        f"a gap of {bh['mean'] - wh['mean']:.2f} points, about the size of each margin of error (±{gh['margin'].mean():.2f}). "
        f"Posts with <b>{best_c['Hashtag Count']}</b> score highest. {p_sentence(p_count)}",
        "No hashtag is a clear winner or loser, so there is no 'bad hashtag' to drop. A post with several hashtags counts "
        "under each of them, so the hashtag bars overlap and are only a rough guide.",
        "Keep the core brand hashtags (#VeganBeauty, #BoldLooks, #CrueltyFree), and test 2 hashtags against 3 on similar posts.",
    )

# ===== Tab 7: Recipe Lab =====
with tabs[6]:
    st.markdown('<div class="sec-title">🧪 Content Recipe Lab</div>', unsafe_allow_html=True)
    st.write("Pick a content recipe. The Lab compares it with the overall average of "
             f"**{BASE_ER:.2f}%** and tells you if it is a **Do**, a **Don't**, or something to **Test**. "
             "A Do or Don't needs a very strong result, because checking hundreds of recipes makes some look special by luck.")
    st.caption("The Recipe Lab always uses all 50,000 posts, so the sidebar filters do not change it.")

    pc = st.columns(4)
    pick_fmt = pc[0].pills("🎬 Format", list(FORMAT_ICON), selection_mode="single", key="rl_fmt",
                           format_func=lambda x: f"{FORMAT_ICON[x]} {x}")
    pick_cmp = pc[1].pills("🎯 Campaign", list(CAMPAIGN_ICON), selection_mode="single", key="rl_cmp",
                           format_func=lambda x: f"{CAMPAIGN_ICON[x]} {x}")
    pick_emo = pc[2].pills("💭 Emotion", list(EMOTION_ICON), selection_mode="single", key="rl_emo",
                           format_func=lambda x: f"{EMOTION_ICON[x]} {x}")
    pick_src = pc[3].pills("🤝 Source", list(SOURCE_ICON), selection_mode="single", key="rl_src",
                           format_func=lambda x: f"{SOURCE_ICON[x]} {x}")
    st.caption("Leave a group empty to mean 'any'.")

    picks = {"Post Type": pick_fmt, "Campaign Type": pick_cmp,
             "Audience Emotion": pick_emo, "Engagement Source": pick_src}
    sub = df
    for col_, val in picks.items():
        if val:
            sub = sub[sub[col_] == val]
    rn, ravg, rlift, rmargin, rz = score(sub)
    rv = verdict(rn, rz)

    css = "do" if rv.startswith("🟢") else "dont" if rv.startswith("🔴") else ""
    if rn < MIN_POSTS:
        why = "There are too few posts in this recipe to say anything."
    elif rv.startswith("🟢"):
        why = f"This recipe beat the average by {rlift:+.2f} points and passes the strict check (z = {rz:.2f}, bar = {Z_STRICT:.2f})."
    elif rv.startswith("🔴"):
        why = f"This recipe fell below the average by {rlift:+.2f} points and passes the strict check (z = {rz:.2f}, bar = -{Z_STRICT:.2f})."
    elif "leans" in rv:
        why = (f"The recipe is {rlift:+.2f} points from the average (z = {rz:.2f}). That is a hint, but luck can easily "
               f"create it: with {N_RECIPES} recipes, about 20 look like this by chance. Treat it as an idea to test.")
    else:
        why = f"The gap of {rlift:+.2f} points is within normal luck (z = {rz:.2f}). There is no evidence this recipe is better or worse than usual."

    v1, v2 = st.columns([1.1, 1])
    chip_names = {"Post Type": "Format", "Campaign Type": "Campaign",
                  "Audience Emotion": "Emotion", "Engagement Source": "Source"}
    chips = "".join(f"<span>{chip_names[k]}: {v or 'Any'}</span>" for k, v in picks.items())
    v1.markdown(
        f'<div class="vcard {css}"><div class="v">{rv}</div>'
        f'<div class="pillrow">{chips}</div>'
        f'<div class="m"><b>{rn:,}</b> posts · average rate <b>{ravg:.2f}%</b> · lift <b>{rlift:+.2f}</b> points '
        f'· margin ±{rmargin:.2f}<br>{why}</div></div>',
        unsafe_allow_html=True,
    )
    lim = max(3.0, abs(rlift) + rmargin + 0.5)
    fig = go.Figure(go.Scatter(x=[rlift], y=["This recipe"], mode="markers",
                               marker=dict(size=16, color=DEEP_PINK, line=dict(color=BLACK, width=2)),
                               error_x=dict(type="data", array=[rmargin], color=BLACK, thickness=3, width=8)))
    fig.add_vline(x=0, line_color=BLACK, line_dash="dash")
    fig.update_xaxes(range=[-lim, lim], title="Lift vs overall average (points), with margin of error")
    fig.update_yaxes(title=None)
    fig.update_layout(title="Is it really different from average?")
    v2.plotly_chart(style_fig(fig, 250), width="stretch")

    st.markdown('<div class="sec-title">🎲 Best and weakest bets</div>', unsafe_allow_html=True)
    rt = recipe_table()
    rt["Recipe"] = (rt["Post Type"] + " · " + rt["Campaign Type"] + " · " + rt["Audience Emotion"]
                    + " · " + rt["Engagement Source"])
    cols_show = ["Recipe", "Posts", "Avg_ER", "Lift", "z"]
    ren = {"Avg_ER": "Avg rate (%)", "Lift": "Lift (pts)"}
    tb1, tb2 = st.columns(2)
    tb1.markdown("**Top 5 leaning up (ideas to test)**")
    tb1.dataframe(rt.sort_values("z", ascending=False).head(5)[cols_show].rename(columns=ren).round(2),
                  width="stretch", hide_index=True)
    tb2.markdown("**Top 5 leaning down (question these)**")
    tb2.dataframe(rt.sort_values("z").head(5)[cols_show].rename(columns=ren).round(2),
                  width="stretch", hide_index=True)

    real_leans, shuf_leans = shuffle_check()
    n_do = int(rt["Verdict"].str.contains("DO").sum())
    n_dont = int(rt["Verdict"].str.contains("DON'T").sum())
    st.markdown('<div class="sec-title">🍀 Luck check and test planner</div>', unsafe_allow_html=True)
    k1, k2, k3 = st.columns(3)
    k1.metric("Proven Do / Don't recipes", f"{n_do} / {n_dont}", help=f"Out of {N_RECIPES} recipes")
    k2.metric("Recipes that 'lean' in real data", real_leans)
    k3.metric("Same count in randomly shuffled data", f"{shuf_leans:.1f}",
              help="Average of 1,000 shuffles where nothing real can remain")
    delta = st.slider("How big a difference do you want to prove (engagement rate points)?", 0.2, 3.0, 1.0, 0.1,
                      key="rl_delta")
    st.markdown(f"To prove a **{delta:.1f}-point** difference in an A/B test, you need about "
                f"**{posts_needed(delta):,} posts in each group**.")

    read_box(
        f"No recipe out of {N_RECIPES} passes the strict bar (z = {Z_STRICT:.2f}). {real_leans} recipes lean up or down, "
        f"but randomly shuffled data produces about {shuf_leans:.0f} such recipes by luck alone.",
        "In this dataset we cannot honestly say which content to make or avoid. The Lab says so instead of inventing rules. "
        "With real, larger data, the same engine can flag true Do and Don't recipes.",
        "Treat the top 'leaning up' recipes as ideas to test with an A/B test, and use the planner to size it.",
    )

# ===== Tab 8: Insights =====
with tabs[7]:
    st.markdown('<div class="sec-title">💡 What the data says, in one place</div>', unsafe_allow_html=True)
    all_mix = df[["Likes", "Comments", "Shares", "Saves"]].sum()
    all_mix = all_mix / all_mix.sum() * 100
    pv_total, fo_total = df["Profile Visits"].sum(), df["Follows"].sum()
    d1, d2, d3 = st.columns(3)
    d1.markdown(
        '<div class="dd do"><h4>✅ Do</h4>'
        "<p>• Keep posting at a steady pace (about 135 post records a day, every month).</p>"
        "<p>• Judge content by <b>engagement rate</b>, not by likes. Likes follow reach.</p>"
        "<p>• Add calls to action: <b>save this</b>, <b>share with a friend</b>, <b>tap our profile</b>.</p>"
        "<p>• Track saves and shares as their own goals.</p></div>", unsafe_allow_html=True)
    d2.markdown(
        '<div class="dd dont"><h4>⛔ Don&#39;t</h4>'
        "<p>• Don't drop any hashtag, format, campaign or posting day based on this data. No gap is reliable.</p>"
        "<p>• Don't move the whole plan to Reels. Reel leads Image by only 0.18 points.</p>"
        "<p>• Don't assume paid posts reach more people. Paid reach was no higher than Organic.</p>"
        "<p>• Don't copy one 'top post'. Ten posts are not a pattern.</p></div>", unsafe_allow_html=True)
    d3.markdown(
        '<div class="dd test"><h4>🧪 Test</h4>'
        "<p>• Reel vs Image for the same message.</p>"
        "<p>• 2 hashtags vs 3 hashtags on similar posts.</p>"
        "<p>• Posts with and without a save or share call to action.</p>"
        "<p>• Paid vs Organic for the same content, to check the return on spend.</p></div>", unsafe_allow_html=True)

    st.markdown('<div class="sec-title">⚖️ Pros and cons</div>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    p1.markdown(
        '<div class="ins good"><h4>Pros</h4>'
        f"<p>• Healthy baseline: average engagement rate of <b>{BASE_ER:.2f}%</b>.</p>"
        f"<p>• About <b>{df['Profile Visit Rate'].mean():.1f}%</b> of reached accounts visit the profile, and "
        f"<b>{df['Follow Conversion'].mean():.0f}%</b> of visitors follow.</p>"
        "<p>• Posting is consistent across all months.</p>"
        "<p>• Every format, campaign, emotion and source performs about the same, so nothing is clearly failing.</p></div>",
        unsafe_allow_html=True)
    p2.markdown(
        '<div class="ins warn"><h4>Cons</h4>'
        f"<p>• Likes are <b>{all_mix['Likes']:.0f}%</b> of interactions. Saves and shares are only "
        f"<b>{all_mix['Saves'] + all_mix['Shares']:.0f}%</b>.</p>"
        f"<p>• Only <b>{fo_total / df['Impressions'].sum() * 100:.2f}%</b> of impressions end in a follow.</p>"
        "<p>• No format, campaign, day or hashtag shows a reliable advantage, so there is no clear lever to pull.</p>"
        "<p>• Paid posts show no extra reach.</p></div>", unsafe_allow_html=True)

    st.markdown('<div class="sec-title">📌 Recommendations for Sugar Cosmetics</div>', unsafe_allow_html=True)
    recs = pd.DataFrame([
        ["1", "Add save and share calls to action", "Saves + shares are only about 9% of interactions", "Compare save and share rates with and without the call to action"],
        ["2", "Make the profile visit easier", "Only about 16% as many profile visits as interactions", "Add 'tap our profile' to posts and compare the profile visit rate"],
        ["3", "Run A/B tests instead of copying a top post", "No recipe is proven; 24 'leaning' recipes are normal luck", "Use the Recipe Lab planner: about 800 posts per group to prove 1 point"],
        ["4", "Test Reel vs Image on the same message", "Reel leads by 0.18 points, which could be luck", "Post the same content in both formats and compare engagement rate"],
        ["5", "Check the return on paid posts", "Paid reach was no higher than Organic", "Track budget alongside reach and engagement rate"],
        ["6", "Collect richer data", "No caption, post ID or time of day in this data", "Add captions, post IDs, time of day and follower count"],
    ], columns=["#", "Recommendation", "Why (evidence)", "How to check"])
    st.dataframe(recs, width="stretch", hide_index=True)
