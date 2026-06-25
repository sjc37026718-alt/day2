import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Brand Analytics", page_icon="◼", layout="wide")

# ── 차트 팔레트: 채도 높고 명확하게 구분되는 색상 ──
CHART_COLORS = ["#2563EB", "#DC2626", "#059669", "#D97706", "#7C3AED",
                "#DB2777", "#0891B2", "#4F46E5", "#CA8A04", "#0D9488",
                "#E11D48", "#2DD4BF", "#6366F1", "#EA580C", "#8B5CF6"]

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Pretendard', 'IBM Plex Sans KR', -apple-system, sans-serif !important; }

    .block-container {
        padding: 1.5rem 2.5rem 3rem 2.5rem !important;
        max-width: 1440px !important;
    }

    /* ── 헤더 ── */
    .dash-header {
        display: flex;
        align-items: center;
        gap: 0.9rem;
        padding-bottom: 1.25rem;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #1E293B;
    }
    .dash-logo {
        width: 36px; height: 36px;
        background: #1E293B;
        border-radius: 6px;
        display: flex; align-items: center; justify-content: center;
        color: white; font-weight: 700; font-size: 0.85rem;
        flex-shrink: 0;
    }
    .dash-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0F172A;
    }
    .dash-subtitle {
        font-size: 0.8rem;
        color: #475569;
        font-weight: 400;
        margin-top: 1px;
    }

    /* ── 업로드 영역 ── */
    .upload-section {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.25rem;
    }
    .upload-section-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: #334155;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.75rem;
    }

    /* ── 상태 바 ── */
    .status-bar {
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-size: 0.8rem;
        color: #14532D;
        font-weight: 500;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .status-bar .dot {
        width: 8px; height: 8px;
        background: #22C55E;
        border-radius: 50%;
        flex-shrink: 0;
    }

    /* ── KPI 카드 ── */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.25rem 1.4rem;
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 4px; height: 100%;
    }
    .kpi-card:nth-child(1)::before { background: #2563EB; }
    .kpi-card:nth-child(2)::before { background: #7C3AED; }
    .kpi-card:nth-child(3)::before { background: #059669; }
    .kpi-card:nth-child(4)::before { background: #D97706; }
    .kpi-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #64748B;
        margin-bottom: 0.5rem;
        letter-spacing: 0.2px;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
    }
    .kpi-unit {
        font-size: 0.9rem;
        font-weight: 600;
        color: #334155;
        margin-left: 3px;
    }
    .kpi-sub {
        font-size: 0.72rem;
        color: #64748B;
        font-weight: 500;
        margin-top: 0.4rem;
    }

    /* ── 차트 카드 ── */
    .chart-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.25rem 1.5rem 1rem 1.5rem;
        margin-bottom: 0.75rem;
    }
    .chart-card-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.25rem;
    }
    .chart-card-desc {
        font-size: 0.7rem;
        color: #64748B;
        font-weight: 400;
        margin-bottom: 0.5rem;
    }

    /* ── 탭 ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 2px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #94A3B8 !important;
        padding: 0.7rem 1.5rem !important;
        border-bottom: 2px solid transparent !important;
        background: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #0F172A !important;
        border-bottom: 2px solid #2563EB !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding: 1.25rem 0 0 0 !important;
    }

    /* ── 사이드바 ── */
    section[data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #1E293B !important;
    }
    .sidebar-brand {
        font-size: 0.9rem;
        font-weight: 700;
        color: #0F172A !important;
        margin-bottom: 0.25rem;
    }
    .sidebar-section {
        font-size: 0.7rem;
        font-weight: 700;
        color: #94A3B8 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 1.25rem;
        margin-bottom: 0.5rem;
        padding-bottom: 0.35rem;
        border-bottom: 1px solid #F1F5F9;
    }
    .sidebar-divider {
        border-top: 1px solid #F1F5F9;
        margin: 0.75rem 0;
    }

    /* ── 섹션 ── */
    .section-wrapper {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        margin-bottom: 0.75rem;
        overflow: hidden;
    }
    .section-header {
        padding: 0.9rem 1.25rem;
        border-bottom: 1px solid #F1F5F9;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .section-label {
        font-size: 0.85rem;
        font-weight: 700;
        color: #0F172A;
    }
    .section-badge {
        font-size: 0.7rem;
        background: #F1F5F9;
        color: #475569;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-weight: 600;
    }

    /* ── 버튼 ── */
    .stDownloadButton > button {
        background: #1E293B !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.5rem !important;
    }
    .stDownloadButton > button:hover {
        background: #334155 !important;
    }

    /* ── 기타 ── */
    .stFileUploader > div { border-radius: 8px !important; }
    .stFileUploader label { font-size: 0.8rem !important; font-weight: 600 !important; color: #334155 !important; }
    .stAlert { border-radius: 8px !important; }
    .stDataFrame { border: 1px solid #E2E8F0 !important; border-radius: 8px !important; }

    div[data-testid="stMetric"] { display: none; }

    .empty-state {
        text-align: center;
        padding: 5rem 2rem;
    }
    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.15;
    }
    .empty-state-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    .empty-state-text {
        font-size: 0.85rem;
        font-weight: 400;
        color: #64748B;
        line-height: 1.7;
    }
</style>
""", unsafe_allow_html=True)


# ── 헤더 ──
st.markdown("""
<div class="dash-header">
    <div class="dash-logo">BA</div>
    <div>
        <div class="dash-title">Brand Analytics</div>
        <div class="dash-subtitle">브랜드 입점현황 · 매출실적 통합 분석 대시보드</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── 업로드 ──
st.markdown('<div class="upload-section"><div class="upload-section-title">데이터 업로드</div>', unsafe_allow_html=True)
col_up1, col_up2 = st.columns(2, gap="medium")
with col_up1:
    file_entry = st.file_uploader("입점현황 (.xlsx)", type=["xlsx", "xls"], key="entry")
with col_up2:
    file_sales = st.file_uploader("매출실적 (.xlsx)", type=["xlsx", "xls"], key="sales")
st.markdown('</div>', unsafe_allow_html=True)

if file_entry is None or file_sales is None:
    st.markdown("""
    <div class="empty-state">
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
<div class="status-bar">
    <div class="dot"></div>
    병합 완료 &nbsp;—&nbsp; Key: <b>{merge_key}</b> &nbsp;|&nbsp;
    <b>{len(merged):,}</b> rows &times; <b>{len(merged.columns)}</b> columns
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
        font=dict(family="Pretendard, sans-serif", size=12, color="#1E293B"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=30),
        title=None,
        legend=dict(font=dict(size=12, color="#334155"), bgcolor="rgba(0,0,0,0)"),
        coloraxis_showscale=False,
        height=height,
    )
    fig.update_xaxes(
        gridcolor="#F1F5F9", zerolinecolor="#E2E8F0",
        title_font=dict(size=12, color="#475569"),
        tickfont=dict(size=11, color="#334155"),
    )
    fig.update_yaxes(
        gridcolor="#F1F5F9", zerolinecolor="#E2E8F0",
        title_font=dict(size=12, color="#475569"),
        tickfont=dict(size=11, color="#334155"),
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
        st.markdown('<div class="chart-card"><div class="chart-card-title">브랜드별 매출 TOP 12</div><div class="chart-card-desc">총 매출 기준 상위 12개 브랜드</div>', unsafe_allow_html=True)
        if brand_col and sales_col:
            brand_sales = (filtered.groupby(brand_col)[sales_col].sum()
                           .reset_index().sort_values(sales_col, ascending=True).tail(12))
            fig = px.bar(brand_sales, y=brand_col, x=sales_col, orientation="h")
            fig.update_traces(marker_color="#2563EB", marker_line_width=0)
            st.plotly_chart(styled_chart(fig, 420), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="chart-card"><div class="chart-card-title">브랜드별 순이익 TOP 12</div><div class="chart-card-desc">순이익 기준 상위 12개 브랜드</div>', unsafe_allow_html=True)
        if brand_col and profit_col:
            brand_profit = (filtered.groupby(brand_col)[profit_col].sum()
                            .reset_index().sort_values(profit_col, ascending=True).tail(12))
            fig2 = px.bar(brand_profit, y=brand_col, x=profit_col, orientation="h")
            fig2.update_traces(marker_color="#059669", marker_line_width=0)
            st.plotly_chart(styled_chart(fig2, 420), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if period_col and sales_col and brand_col:
        st.markdown('<div class="chart-card"><div class="chart-card-title">월별 매출 추이</div><div class="chart-card-desc">매출 상위 5개 브랜드의 월간 트렌드</div>', unsafe_allow_html=True)
        top5 = filtered.groupby(brand_col)[sales_col].sum().nlargest(5).index.tolist()
        monthly = (filtered[filtered[brand_col].isin(top5)]
                   .groupby([period_col, brand_col])[sales_col].sum().reset_index())
        fig3 = px.line(monthly, x=period_col, y=sales_col, color=brand_col,
                       markers=True, color_discrete_sequence=CHART_COLORS)
        fig3.update_traces(line=dict(width=2.5), marker=dict(size=7))
        st.plotly_chart(styled_chart(fig3, 380), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if brand_col and sales_col and profit_col and order_col:
        st.markdown('<div class="chart-card"><div class="chart-card-title">매출 vs 순이익</div><div class="chart-card-desc">버블 크기 = 주문건수</div>', unsafe_allow_html=True)
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
            st.markdown('<div class="chart-card"><div class="chart-card-title">채널별 매출 비중</div><div class="chart-card-desc">전체 매출 대비 채널 점유율</div>', unsafe_allow_html=True)
            ch_sales = (filtered.groupby(channel_col)[sales_col].sum()
                        .reset_index().sort_values(sales_col, ascending=False))
            fig4 = px.pie(ch_sales, names=channel_col, values=sales_col,
                          hole=0.5, color_discrete_sequence=CHART_COLORS)
            fig4.update_traces(
                textinfo="label+percent", textfont_size=12, textfont_color="#1E293B",
                hovertemplate="<b>%{label}</b><br>%{value:,.0f}원<br>%{percent}",
                marker=dict(line=dict(color="#FFFFFF", width=2)),
            )
            st.plotly_chart(styled_chart(fig4, 400), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_r2:
            if order_col:
                st.markdown('<div class="chart-card"><div class="chart-card-title">채널별 주문건수</div><div class="chart-card-desc">각 채널의 총 주문 수</div>', unsafe_allow_html=True)
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
                st.markdown('<div class="chart-card"><div class="chart-card-title">채널별 반품률</div><div class="chart-card-desc">평균 반품률 (%)</div>', unsafe_allow_html=True)
                ch_return = (filtered.groupby(channel_col)[return_rate_col].mean()
                             .reset_index().sort_values(return_rate_col, ascending=True))
                fig6 = px.bar(ch_return, y=channel_col, x=return_rate_col, orientation="h")
                fig6.update_traces(marker_color="#DC2626")
                st.plotly_chart(styled_chart(fig6, 340), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with col_r3:
            if repurchase_col:
                st.markdown('<div class="chart-card"><div class="chart-card-title">채널별 재구매율</div><div class="chart-card-desc">평균 재구매율 (%)</div>', unsafe_allow_html=True)
                ch_repurchase = (filtered.groupby(channel_col)[repurchase_col].mean()
                                 .reset_index().sort_values(repurchase_col, ascending=True))
                fig_rep = px.bar(ch_repurchase, y=channel_col, x=repurchase_col, orientation="h")
                fig_rep.update_traces(marker_color="#059669")
                st.plotly_chart(styled_chart(fig_rep, 340), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)


# ── TAB 3: 포트폴리오 ──
with tab3:
    col_l4, col_r4 = st.columns([1, 1], gap="medium")

    with col_l4:
        if status_col:
            st.markdown('<div class="chart-card"><div class="chart-card-title">입점상태 분포</div><div class="chart-card-desc">브랜드 수 기준</div>', unsafe_allow_html=True)
            status_counts = filtered.groupby(status_col)[merge_key].nunique().reset_index()
            status_counts.columns = [status_col, "count"]
            fig7 = px.pie(status_counts, names=status_col, values="count",
                          hole=0.5, color_discrete_sequence=CHART_COLORS)
            fig7.update_traces(
                textinfo="label+value+percent", textfont_size=12, textfont_color="#1E293B",
                marker=dict(line=dict(color="#FFFFFF", width=2)),
            )
            st.plotly_chart(styled_chart(fig7, 380), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_r4:
        if grade_col:
            st.markdown('<div class="chart-card"><div class="chart-card-title">계약등급별 브랜드 수</div><div class="chart-card-desc">등급 분포</div>', unsafe_allow_html=True)
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
            st.markdown('<div class="chart-card"><div class="chart-card-title">카테고리별 매출</div><div class="chart-card-desc">상품 카테고리 기준</div>', unsafe_allow_html=True)
            cat_sales = (filtered.groupby(category_col)[sales_col].sum()
                         .reset_index().sort_values(sales_col, ascending=True))
            fig9 = px.bar(cat_sales, y=category_col, x=sales_col, orientation="h",
                          color=category_col, color_discrete_sequence=CHART_COLORS)
            fig9.update_layout(showlegend=False)
            st.plotly_chart(styled_chart(fig9, 400), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_r5:
        if style_col and sales_col:
            st.markdown('<div class="chart-card"><div class="chart-card-title">스타일별 매출</div><div class="chart-card-desc">패션 스타일 기준</div>', unsafe_allow_html=True)
            style_sales = (filtered.groupby(style_col)[sales_col].sum()
                           .reset_index().sort_values(sales_col, ascending=True))
            fig10 = px.bar(style_sales, y=style_col, x=sales_col, orientation="h",
                           color=style_col, color_discrete_sequence=CHART_COLORS)
            fig10.update_layout(showlegend=False)
            st.plotly_chart(styled_chart(fig10, 400), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    if category_col and brand_col and sales_col:
        st.markdown('<div class="chart-card"><div class="chart-card-title">카테고리 × 브랜드 히트맵</div><div class="chart-card-desc">매출 상위 10개 브랜드 기준</div>', unsafe_allow_html=True)
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
