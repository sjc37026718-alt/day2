import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime

st.set_page_config(page_title="Brand Analytics", page_icon="◼", layout="wide")

CHART_COLORS = ["#3182F6", "#F04452", "#00B386", "#F5A623", "#7B61FF",
                "#E5503C", "#45BCD6", "#6E56CF", "#D4A017", "#2EC4B6",
                "#FF6B6B", "#48C78E", "#845EF7", "#FD7E14", "#A78BFA"]

TOSS_BLUE = "#3182F6"

st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

    * { font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif !important; }
    html, body, [data-testid="stAppViewContainer"] {
        background: #F2F4F6 !important;
    }

    /* ── 레이아웃 ── */
    .block-container {
        padding: 1rem 2rem 3rem 2rem !important;
        max-width: 1280px !important;
    }
    .stMainBlockContainer {
        padding-top: 3rem !important;
    }

    /* ── 사이드바 ── */
    section[data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid #F2F4F6 !important;
        box-shadow: 2px 0 8px rgba(0,0,0,0.04) !important;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        padding: 1.5rem 1.25rem;
    }
    .sidebar-brand {
        font-size: 1.1rem;
        font-weight: 800;
        color: #191F28 !important;
        margin-bottom: 0.1rem;
    }
    .sidebar-section {
        font-size: 0.72rem;
        font-weight: 700;
        color: #8B95A1 !important;
        letter-spacing: 0.5px;
        margin-top: 1.5rem;
        margin-bottom: 0.6rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #F2F4F6;
    }
    .sidebar-divider {
        border-top: 1px solid #F2F4F6;
        margin: 1rem 0;
    }
    section[data-testid="stSidebar"] label {
        color: #4E5968 !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] .stMultiSelect > div {
        background: #F9FAFB !important;
        border: 1px solid #E5E8EB !important;
        border-radius: 12px !important;
    }
    section[data-testid="stSidebar"] .stMultiSelect > div:hover,
    section[data-testid="stSidebar"] .stMultiSelect > div:focus-within {
        border-color: #3182F6 !important;
        box-shadow: 0 0 0 3px rgba(49,130,246,0.12) !important;
    }
    section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {
        background: #E8F3FF !important;
        color: #3182F6 !important;
        border-radius: 8px !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] span {
        color: #3182F6 !important;
    }

    /* ── 토스 카드 ── */
    .toss-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .toss-card-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #191F28;
        margin-bottom: 0.2rem;
    }
    .toss-card-desc {
        font-size: 0.78rem;
        color: #8B95A1;
        font-weight: 400;
        margin-bottom: 0.75rem;
    }

    /* ── 헤더 ── */
    .toss-header {
        padding: 0.5rem 0 1.5rem 0;
    }
    .toss-header-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #191F28;
        letter-spacing: -0.3px;
    }
    .toss-header-sub {
        font-size: 0.85rem;
        color: #8B95A1;
        font-weight: 400;
        margin-top: 4px;
    }

    /* ── 상태 바 ── */
    .toss-status {
        background: #E8F7EE;
        border-radius: 12px;
        padding: 0.85rem 1.25rem;
        font-size: 0.82rem;
        color: #00875A;
        font-weight: 600;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .toss-status .dot {
        width: 8px; height: 8px;
        background: #00B386;
        border-radius: 50%;
        flex-shrink: 0;
    }

    /* ── KPI ── */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.4rem 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .kpi-label {
        font-size: 0.78rem;
        font-weight: 600;
        color: #8B95A1;
        margin-bottom: 0.6rem;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #191F28;
        line-height: 1.1;
        letter-spacing: -0.5px;
    }
    .kpi-unit {
        font-size: 0.9rem;
        font-weight: 700;
        color: #4E5968;
        margin-left: 2px;
    }
    .kpi-sub {
        font-size: 0.73rem;
        color: #8B95A1;
        font-weight: 500;
        margin-top: 0.5rem;
    }

    /* ── 탭 ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: #FFFFFF;
        border-radius: 12px;
        padding: 4px;
        border: none !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #8B95A1 !important;
        padding: 0.6rem 1.5rem !important;
        border-radius: 10px !important;
        border: none !important;
        background: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #191F28 !important;
        background: #F2F4F6 !important;
        border: none !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding: 0.5rem 0 0 0 !important;
    }
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* ── 섹션 ── */
    .section-wrapper {
        background: #FFFFFF;
        border-radius: 16px;
        margin-bottom: 1rem;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .section-header {
        padding: 1rem 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .section-label {
        font-size: 0.95rem;
        font-weight: 700;
        color: #191F28;
    }
    .section-badge {
        font-size: 0.72rem;
        background: #F2F4F6;
        color: #6B7684;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
    }

    /* ── 버튼 ── */
    .stDownloadButton > button {
        background: #3182F6 !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        padding: 0.7rem 1.75rem !important;
        transition: background 0.2s !important;
    }
    .stDownloadButton > button:hover {
        background: #1B64DA !important;
    }

    /* ── 파일 업로더: 내부 텍스트 숨기고 한글화 ── */
    .stFileUploader label {
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        color: #191F28 !important;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        background: #FFFFFF !important;
        border: 2px dashed #D1D6DB !important;
        border-radius: 16px !important;
        transition: border-color 0.2s !important;
        position: relative !important;
        min-height: 100px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #3182F6 !important;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"] > div,
    .stFileUploader [data-testid="stFileUploaderDropzone"] > section,
    .stFileUploader [data-testid="stFileUploaderDropzone"] > span {
        visibility: hidden !important;
        position: absolute !important;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"] > input[type="file"] {
        position: absolute !important;
        inset: 0 !important;
        opacity: 0 !important;
        cursor: pointer !important;
        z-index: 2 !important;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"]::after {
        content: "파일을 여기에 끌어놓거나 클릭하세요" !important;
        visibility: visible !important;
        position: absolute !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        color: #8B95A1 !important;
        pointer-events: none !important;
        z-index: 1 !important;
    }

    /* ── 기타 ── */
    .stAlert { border-radius: 12px !important; }
    .stDataFrame {
        border: none !important;
        border-radius: 16px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
        overflow: hidden;
    }
    div[data-testid="stMetric"] { display: none; }

    .empty-state {
        text-align: center;
        padding: 6rem 2rem;
    }
    .empty-state-icon {
        font-size: 3.5rem;
        margin-bottom: 1.25rem;
        opacity: 0.12;
    }
    .empty-state-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #191F28;
        margin-bottom: 0.5rem;
    }
    .empty-state-text {
        font-size: 0.88rem;
        font-weight: 400;
        color: #8B95A1;
        line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)


# ── 헤더 ──
st.markdown("""
<div class="toss-header">
    <div class="toss-header-title">Brand Analytics</div>
    <div class="toss-header-sub">브랜드 입점현황 · 매출실적 통합 분석 대시보드</div>
</div>
""", unsafe_allow_html=True)

# ── 서울 날씨 (Open-Meteo API) ──
@st.cache_data(ttl=600)
def fetch_seoul_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=37.5665&longitude=126.978"
        "&current=temperature_2m,weathercode"
        "&hourly=temperature_2m"
        "&forecast_days=1"
        "&timezone=Asia/Seoul"
    )
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    return resp.json()

WMO_ICONS = {
    0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
    45: "🌫️", 48: "🌫️",
    51: "🌦️", 53: "🌦️", 55: "🌧️",
    61: "🌧️", 63: "🌧️", 65: "🌧️",
    71: "🌨️", 73: "🌨️", 75: "🌨️",
    80: "🌦️", 81: "🌧️", 82: "🌧️",
    95: "⛈️", 96: "⛈️", 99: "⛈️",
}

try:
    weather = fetch_seoul_weather()
    current_temp = weather["current"]["temperature_2m"]
    weather_code = weather["current"].get("weathercode", 0)
    weather_icon = WMO_ICONS.get(weather_code, "🌡️")

    hourly_times = weather["hourly"]["time"]
    hourly_temps = weather["hourly"]["temperature_2m"]
    hour_labels = [datetime.fromisoformat(t).strftime("%H시") for t in hourly_times]

    st.markdown(f"""
    <div class="toss-card" style="display:flex; align-items:center; justify-content:space-between;">
        <div>
            <div class="toss-card-title">서울 현재 날씨</div>
            <div class="toss-card-desc" style="margin-bottom:0;">Open-Meteo · 10분마다 갱신</div>
        </div>
        <div style="font-size:2rem; line-height:1;">
            {weather_icon} <span style="font-size:1.75rem; font-weight:800; color:#191F28;">{current_temp}°C</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="toss-card"><div class="toss-card-title">오늘 시간별 기온</div><div class="toss-card-desc">서울 (37.57°N, 126.98°E)</div>', unsafe_allow_html=True)
    df_weather = pd.DataFrame({"시간": hour_labels, "기온(°C)": hourly_temps})
    fig_w = px.area(df_weather, x="시간", y="기온(°C)",
                    color_discrete_sequence=[TOSS_BLUE])
    fig_w.update_traces(
        line=dict(width=2.5),
        fillcolor="rgba(49,130,246,0.08)",
        hovertemplate="%{x}<br><b>%{y}°C</b><extra></extra>",
    )
    fig_w.update_layout(
        font=dict(family="Pretendard, sans-serif", size=12, color="#191F28"),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=10, b=30), height=240,
        xaxis=dict(gridcolor="#F2F4F6", tickfont=dict(size=10, color="#6B7684")),
        yaxis=dict(gridcolor="#F2F4F6", tickfont=dict(size=11, color="#6B7684"), title=None),
    )
    st.plotly_chart(fig_w, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

except Exception:
    st.info("날씨 정보를 불러올 수 없습니다. 인터넷 연결을 확인해주세요.")


# ── 업로드 ──
col_up1, col_up2 = st.columns(2, gap="medium")
with col_up1:
    file_entry = st.file_uploader("입점현황 (.xlsx)", type=["xlsx", "xls"], key="entry")
    if file_entry:
        st.markdown(f'<div style="background:#E8F7EE;border-radius:10px;padding:0.6rem 1rem;margin-top:-0.5rem;font-size:0.8rem;font-weight:600;color:#00875A;">&#10003; {file_entry.name} 업로드 완료</div>', unsafe_allow_html=True)
with col_up2:
    file_sales = st.file_uploader("매출실적 (.xlsx)", type=["xlsx", "xls"], key="sales")
    if file_sales:
        st.markdown(f'<div style="background:#E8F7EE;border-radius:10px;padding:0.6rem 1rem;margin-top:-0.5rem;font-size:0.8rem;font-weight:600;color:#00875A;">&#10003; {file_sales.name} 업로드 완료</div>', unsafe_allow_html=True)

if file_entry is None or file_sales is None:
    st.markdown("""
    <div class="toss-card empty-state">
        <div class="empty-state-icon">&#128202;</div>
        <div class="empty-state-title">엑셀 파일 2개를 업로드해주세요</div>
        <div class="empty-state-text">
            브랜드 입점현황과 매출실적 파일을 업로드하면<br>
            자동으로 병합하여 분석 대시보드를 생성합니다.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df_entry = pd.read_excel(file_entry)
df_sales = pd.read_excel(file_sales)

merge_key = None
common_cols = list(set(df_entry.columns) & set(df_sales.columns))
if common_cols:
    id_cols = [c for c in common_cols if "ID" in c or "id" in c or "Id" in c]
    merge_key = id_cols[0] if id_cols else common_cols[0]

if merge_key is None:
    st.error("두 파일에 공통 컬럼이 없어 병합할 수 없습니다.")
    st.stop()

merged = pd.merge(df_sales, df_entry, on=merge_key, how="left")

st.markdown(f"""
<div class="toss-status">
    <div class="dot"></div>
    병합 완료 — Key: <b>{merge_key}</b> | <b>{len(merged):,}</b> rows × <b>{len(merged.columns)}</b> columns
</div>
""", unsafe_allow_html=True)

# ── 컬럼 자동 감지 ──
def find_col(df, keywords, exclude=None):
    for c in df.columns:
        if any(k in c for k in keywords):
            if exclude and any(e in c for e in exclude):
                continue
            return c
    return None

brand_col = find_col(merged, ["브랜드명"], ["영", "한"]) or find_col(merged, ["브랜드명"])
sales_col = find_col(merged, ["총매출", "매출"])
profit_col = find_col(merged, ["순이익"])
channel_col = "채널" if "채널" in merged.columns else None
period_col = find_col(merged, ["기간"])
category_col = find_col(merged, ["카테고리"])
status_col = find_col(merged, ["입점상태"])
order_col = find_col(merged, ["주문건수"])
return_rate_col = find_col(merged, ["반품률"])
grade_col = find_col(merged, ["계약등급", "등급"])
style_col = find_col(merged, ["스타일"])
repurchase_col = find_col(merged, ["재구매"])

# ── 사이드바 필터 ──
with st.sidebar:
    st.markdown('<div class="sidebar-brand">Brand Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">필터 설정</div>', unsafe_allow_html=True)

    brands = sorted(merged[brand_col].dropna().unique()) if brand_col else []
    selected_brands = st.multiselect("브랜드", brands, default=brands)

    if channel_col:
        channels = sorted(merged[channel_col].dropna().unique())
        selected_channels = st.multiselect("채널", channels, default=channels)
    else:
        selected_channels = []

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    if status_col:
        statuses = sorted(merged[status_col].dropna().unique())
        selected_statuses = st.multiselect("입점상태", statuses, default=statuses)
    else:
        selected_statuses = None

    if grade_col:
        grades = sorted(merged[grade_col].dropna().unique())
        selected_grades = st.multiselect("계약등급", grades, default=grades)
    else:
        selected_grades = None

filtered = merged.copy()
if brand_col and selected_brands:
    filtered = filtered[filtered[brand_col].isin(selected_brands)]
if channel_col and selected_channels:
    filtered = filtered[filtered[channel_col].isin(selected_channels)]
if status_col and selected_statuses is not None:
    filtered = filtered[filtered[status_col].isin(selected_statuses)]
if grade_col and selected_grades is not None:
    filtered = filtered[filtered[grade_col].isin(selected_grades)]


# ── 차트 공통 스타일 ──
def styled_chart(fig, height=400):
    fig.update_layout(
        font=dict(family="Pretendard, sans-serif", size=12, color="#191F28"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=30),
        title=None,
        legend=dict(font=dict(size=12, color="#4E5968"), bgcolor="rgba(0,0,0,0)"),
        coloraxis_showscale=False,
        height=height,
    )
    fig.update_xaxes(
        gridcolor="#F2F4F6", zerolinecolor="#E5E8EB",
        title_font=dict(size=12, color="#6B7684"),
        tickfont=dict(size=11, color="#4E5968"),
    )
    fig.update_yaxes(
        gridcolor="#F2F4F6", zerolinecolor="#E5E8EB",
        title_font=dict(size=12, color="#6B7684"),
        tickfont=dict(size=11, color="#4E5968"),
    )
    return fig


# ── KPI ──
total_sales = filtered[sales_col].sum() if sales_col else 0
total_orders = filtered[order_col].sum() if order_col else 0
total_profit = filtered[profit_col].sum() if profit_col else 0
brand_count = filtered[brand_col].nunique() if brand_col else 0
avg_order_value = total_sales / total_orders if total_orders > 0 else 0
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-label">총 매출</div>
        <div class="kpi-value">{total_sales/1e8:,.1f}<span class="kpi-unit">억원</span></div>
        <div class="kpi-sub">건당 평균 {avg_order_value:,.0f}원</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">총 주문</div>
        <div class="kpi-value">{total_orders:,.0f}<span class="kpi-unit">건</span></div>
        <div class="kpi-sub">{brand_count}개 브랜드 합산</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">순이익</div>
        <div class="kpi-value">{total_profit/1e8:,.1f}<span class="kpi-unit">억원</span></div>
        <div class="kpi-sub">마진율 {profit_margin:.1f}%</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">브랜드</div>
        <div class="kpi-value">{brand_count}<span class="kpi-unit">개</span></div>
        <div class="kpi-sub">현재 필터 기준</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── 탭 ──
tab1, tab2, tab3, tab4 = st.tabs(["매출 분석", "채널 분석", "포트폴리오", "원본 데이터"])

# ── TAB 1: 매출 분석 ──
with tab1:
    col_l, col_r = st.columns([1, 1], gap="medium")

    with col_l:
        st.markdown('<div class="toss-card"><div class="toss-card-title">브랜드별 매출 TOP 12</div><div class="toss-card-desc">총 매출 기준 상위 12개 브랜드</div>', unsafe_allow_html=True)
        if brand_col and sales_col:
            brand_sales = (filtered.groupby(brand_col)[sales_col].sum()
                           .reset_index().sort_values(sales_col, ascending=True).tail(12))
            fig = px.bar(brand_sales, y=brand_col, x=sales_col, orientation="h")
            fig.update_traces(marker_color=TOSS_BLUE, marker_line_width=0)
            st.plotly_chart(styled_chart(fig, 420), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="toss-card"><div class="toss-card-title">브랜드별 순이익 TOP 12</div><div class="toss-card-desc">순이익 기준 상위 12개 브랜드</div>', unsafe_allow_html=True)
        if brand_col and profit_col:
            brand_profit = (filtered.groupby(brand_col)[profit_col].sum()
                            .reset_index().sort_values(profit_col, ascending=True).tail(12))
            fig2 = px.bar(brand_profit, y=brand_col, x=profit_col, orientation="h")
            fig2.update_traces(marker_color="#00B386", marker_line_width=0)
            st.plotly_chart(styled_chart(fig2, 420), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if period_col and sales_col and brand_col:
        st.markdown('<div class="toss-card"><div class="toss-card-title">월별 매출 추이</div><div class="toss-card-desc">매출 상위 5개 브랜드의 월간 트렌드</div>', unsafe_allow_html=True)
        top5 = filtered.groupby(brand_col)[sales_col].sum().nlargest(5).index.tolist()
        monthly = (filtered[filtered[brand_col].isin(top5)]
                   .groupby([period_col, brand_col])[sales_col].sum().reset_index())
        fig3 = px.line(monthly, x=period_col, y=sales_col, color=brand_col,
                       markers=True, color_discrete_sequence=CHART_COLORS)
        fig3.update_traces(line=dict(width=2.5), marker=dict(size=7))
        st.plotly_chart(styled_chart(fig3, 380), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if brand_col and sales_col and profit_col and order_col:
        st.markdown('<div class="toss-card"><div class="toss-card-title">매출 vs 순이익</div><div class="toss-card-desc">버블 크기 = 주문건수</div>', unsafe_allow_html=True)
        scatter_df = (filtered.groupby(brand_col)
                      .agg({sales_col: "sum", profit_col: "sum", order_col: "sum"})
                      .reset_index())
        fig_sc = px.scatter(scatter_df, x=sales_col, y=profit_col, size=order_col,
                            hover_name=brand_col, color=brand_col,
                            color_discrete_sequence=CHART_COLORS)
        fig_sc.update_traces(marker=dict(opacity=0.85, line=dict(width=1.5, color="#FFFFFF")))
        fig_sc.update_layout(showlegend=False)
        st.plotly_chart(styled_chart(fig_sc, 420), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ── TAB 2: 채널 분석 ──
with tab2:
    if channel_col and sales_col:
        col_l2, col_r2 = st.columns([1, 1], gap="medium")

        with col_l2:
            st.markdown('<div class="toss-card"><div class="toss-card-title">채널별 매출 비중</div><div class="toss-card-desc">전체 매출 대비 채널 점유율</div>', unsafe_allow_html=True)
            ch_sales = (filtered.groupby(channel_col)[sales_col].sum()
                        .reset_index().sort_values(sales_col, ascending=False))
            fig4 = px.pie(ch_sales, names=channel_col, values=sales_col,
                          hole=0.55, color_discrete_sequence=CHART_COLORS)
            fig4.update_traces(
                textinfo="label+percent", textfont_size=12, textfont_color="#191F28",
                hovertemplate="<b>%{label}</b><br>%{value:,.0f}원<br>%{percent}",
                marker=dict(line=dict(color="#FFFFFF", width=3)),
            )
            st.plotly_chart(styled_chart(fig4, 400), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_r2:
            if order_col:
                st.markdown('<div class="toss-card"><div class="toss-card-title">채널별 주문건수</div><div class="toss-card-desc">각 채널의 총 주문 수</div>', unsafe_allow_html=True)
                ch_orders = (filtered.groupby(channel_col)[order_col].sum()
                             .reset_index().sort_values(order_col, ascending=True))
                fig5 = px.bar(ch_orders, y=channel_col, x=order_col, orientation="h",
                              color=channel_col, color_discrete_sequence=CHART_COLORS)
                fig5.update_layout(showlegend=False)
                st.plotly_chart(styled_chart(fig5, 400), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        col_l3, col_r3 = st.columns([1, 1], gap="medium")
        with col_l3:
            if return_rate_col:
                st.markdown('<div class="toss-card"><div class="toss-card-title">채널별 반품률</div><div class="toss-card-desc">평균 반품률 (%)</div>', unsafe_allow_html=True)
                ch_return = (filtered.groupby(channel_col)[return_rate_col].mean()
                             .reset_index().sort_values(return_rate_col, ascending=True))
                fig6 = px.bar(ch_return, y=channel_col, x=return_rate_col, orientation="h")
                fig6.update_traces(marker_color="#F04452")
                st.plotly_chart(styled_chart(fig6, 340), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with col_r3:
            if repurchase_col:
                st.markdown('<div class="toss-card"><div class="toss-card-title">채널별 재구매율</div><div class="toss-card-desc">평균 재구매율 (%)</div>', unsafe_allow_html=True)
                ch_repurchase = (filtered.groupby(channel_col)[repurchase_col].mean()
                                 .reset_index().sort_values(repurchase_col, ascending=True))
                fig_rep = px.bar(ch_repurchase, y=channel_col, x=repurchase_col, orientation="h")
                fig_rep.update_traces(marker_color="#00B386")
                st.plotly_chart(styled_chart(fig_rep, 340), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)


# ── TAB 3: 포트폴리오 ──
with tab3:
    col_l4, col_r4 = st.columns([1, 1], gap="medium")

    with col_l4:
        if status_col:
            st.markdown('<div class="toss-card"><div class="toss-card-title">입점상태 분포</div><div class="toss-card-desc">브랜드 수 기준</div>', unsafe_allow_html=True)
            status_counts = filtered.groupby(status_col)[merge_key].nunique().reset_index()
            status_counts.columns = [status_col, "count"]
            fig7 = px.pie(status_counts, names=status_col, values="count",
                          hole=0.55, color_discrete_sequence=CHART_COLORS)
            fig7.update_traces(
                textinfo="label+value+percent", textfont_size=12, textfont_color="#191F28",
                marker=dict(line=dict(color="#FFFFFF", width=3)),
            )
            st.plotly_chart(styled_chart(fig7, 380), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_r4:
        if grade_col:
            st.markdown('<div class="toss-card"><div class="toss-card-title">계약등급별 브랜드 수</div><div class="toss-card-desc">등급 분포</div>', unsafe_allow_html=True)
            grade_counts = filtered.groupby(grade_col)[merge_key].nunique().reset_index()
            grade_counts.columns = [grade_col, "count"]
            fig8 = px.bar(grade_counts, x=grade_col, y="count",
                          color=grade_col, color_discrete_sequence=CHART_COLORS)
            fig8.update_layout(showlegend=False)
            st.plotly_chart(styled_chart(fig8, 380), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    col_l5, col_r5 = st.columns([1, 1], gap="medium")

    with col_l5:
        if category_col and sales_col:
            st.markdown('<div class="toss-card"><div class="toss-card-title">카테고리별 매출</div><div class="toss-card-desc">상품 카테고리 기준</div>', unsafe_allow_html=True)
            cat_sales = (filtered.groupby(category_col)[sales_col].sum()
                         .reset_index().sort_values(sales_col, ascending=True))
            fig9 = px.bar(cat_sales, y=category_col, x=sales_col, orientation="h",
                          color=category_col, color_discrete_sequence=CHART_COLORS)
            fig9.update_layout(showlegend=False)
            st.plotly_chart(styled_chart(fig9, 400), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_r5:
        if style_col and sales_col:
            st.markdown('<div class="toss-card"><div class="toss-card-title">스타일별 매출</div><div class="toss-card-desc">패션 스타일 기준</div>', unsafe_allow_html=True)
            style_sales = (filtered.groupby(style_col)[sales_col].sum()
                           .reset_index().sort_values(sales_col, ascending=True))
            fig10 = px.bar(style_sales, y=style_col, x=sales_col, orientation="h",
                           color=style_col, color_discrete_sequence=CHART_COLORS)
            fig10.update_layout(showlegend=False)
            st.plotly_chart(styled_chart(fig10, 400), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    if category_col and brand_col and sales_col:
        st.markdown('<div class="toss-card"><div class="toss-card-title">카테고리 × 브랜드 히트맵</div><div class="toss-card-desc">매출 상위 10개 브랜드 기준</div>', unsafe_allow_html=True)
        heat_data = (filtered.groupby([category_col, brand_col])[sales_col].sum().reset_index())
        top_brands = heat_data.groupby(brand_col)[sales_col].sum().nlargest(10).index.tolist()
        heat_data = heat_data[heat_data[brand_col].isin(top_brands)]
        heat_pivot = heat_data.pivot_table(index=category_col, columns=brand_col,
                                           values=sales_col, fill_value=0)
        fig_heat = px.imshow(heat_pivot, color_continuous_scale="Blues", aspect="auto")
        fig_heat.update_layout(coloraxis_showscale=True)
        fig_heat.update_traces(texttemplate="%{z:,.0f}", textfont_size=9)
        st.plotly_chart(styled_chart(fig_heat, 420), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ── TAB 4: 원본 데이터 ──
with tab4:
    st.markdown(f"""
    <div class="section-wrapper">
        <div class="section-header">
            <span class="section-label">병합 데이터</span>
            <span class="section-badge">{len(filtered):,} rows</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(filtered, use_container_width=True, height=520)

    csv = filtered.to_csv(index=False).encode("utf-8-sig")
    st.download_button("CSV 다운로드", csv, "brand_analytics_export.csv", "text/csv")
