import numpy as np
import pandas as pd
import streamlit as st

from app.dashboard_table_loader import load_dashboard_table
from app.utils import (
    PRICE_BUCKET_LABELS,
    REVIEW_SENTIMENT_LABELS,
    REVIEW_SIGNAL_LABELS,
    get_available_columns,
    map_display_series,
    rename_display_columns,
    require_processed_data,
    safe_column,
)

REQUIRED_V2_COLUMNS = [
    "release_year",
    "owners_mid",
    "total_reviews",
    "positive_rate",
    "review_log",
    "has_reviews",
    "is_free",
    "has_discount",
    "platform_count",
    "price_bucket",
    "review_signal",
    "review_sentiment",
]

TABLE_COLUMNS = [
    "Name",
    "release_year",
    "price_bucket",
    "owners_mid",
    "total_reviews",
    "positive_rate",
    "platform_count",
    "Genres",
    "Tags",
]
PRICE_BUCKET_ORDER = ["free", "budget", "mid", "premium", "luxury"]
REVIEW_SIGNAL_ORDER = ["no_signal", "very_low", "low", "medium", "high"]
REVIEW_SENTIMENT_ORDER = ["no_reviews", "weak", "mixed", "strong"]
PLATFORM_COUNT_ORDER = [0, 1, 2, 3]
MAX_SCATTER_POINTS = 5000
SCATTER_RANDOM_STATE = 42
GEN_CMD = "python scripts/generate_dashboard_tables.py --input data/processed/steam_games_cleaned.csv --output-dir data/processed/dashboard_tables --top-n 30 --min-reviews 20"

RANKING_COLUMNS = [
    "AppID",
    "Name",
    "release_year",
    "price_bucket",
    "owners_mid",
    "total_reviews",
    "positive_rate",
    "supports_simplified_chinese",
    "Genres",
    "Tags",
    "heuristic_reason",
]
RANKING_COLUMN_LABELS = {
    "AppID": "AppID",
    "Name": "游戏名称",
    "release_year": "发行年份",
    "price_bucket": "价格分层",
    "owners_mid": "估计拥有者中位数",
    "total_reviews": "评论数",
    "positive_rate": "好评率",
    "supports_simplified_chinese": "是否支持简体中文",
    "Genres": "游戏类型",
    "Tags": "标签",
    "heuristic_reason": "启发式原因",
}
HEURISTIC_REASON_LABELS = {
    "high_rating_low_estimated_ownership": "高口碑低估计拥有者",
    "low_price_high_rating": "低价高口碑",
    "high_attention_low_rating": "高关注低口碑",
    "chinese_supported_high_rating_low_exposure": "已支持简中的高口碑低曝光候选",
    "missing_simplified_chinese_high_rating_attention": "未支持简中的高口碑高关注候选",
}


def _load_table(name: str) -> pd.DataFrame | None:
    df = load_dashboard_table(name)
    if df is None or df.empty:
        return None
    return df


def _show_missing_table_warning(table_name: str) -> None:
    st.warning("未检测到对应的后端榜单表。请先运行 generate_dashboard_tables.py 生成后端分析表。")
    st.code(GEN_CMD, language="bash")
    st.caption(f"缺失表：{table_name}.csv")


def _format_ranking_table(df: pd.DataFrame) -> pd.DataFrame:
    show_cols = [c for c in RANKING_COLUMNS if c in df.columns]
    out = df[show_cols].copy()

    if "release_year" in out.columns:
        out["release_year"] = pd.to_numeric(out["release_year"], errors="coerce").map(format_int)
    for c in ["owners_mid", "total_reviews"]:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce").map(format_int)
    if "positive_rate" in out.columns:
        out["positive_rate"] = pd.to_numeric(out["positive_rate"], errors="coerce").map(format_percent_safe)
    if "price_bucket" in out.columns:
        out["price_bucket"] = map_display_series(out["price_bucket"], PRICE_BUCKET_LABELS)
    if "supports_simplified_chinese" in out.columns:
        out["supports_simplified_chinese"] = out["supports_simplified_chinese"].map(lambda x: "是" if bool(x) else "否")
    if "heuristic_reason" in out.columns:
        out["heuristic_reason"] = out["heuristic_reason"].map(lambda x: HEURISTIC_REASON_LABELS.get(x, x))

    return out.rename(columns=RANKING_COLUMN_LABELS)


def _show_ranking_section(title: str, table_name: str, caption: str, max_rows: int = 30) -> bool:
    st.caption(title)
    backend_df = _load_table(table_name)
    if backend_df is not None:
        st.dataframe(_format_ranking_table(backend_df.head(max_rows)), use_container_width=True)
        st.caption(caption)
        return True

    _show_missing_table_warning(table_name)
    return False


def numeric_series(df: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(safe_column(df, column, np.nan), errors="coerce")


def format_int(value) -> str:
    if pd.isna(value):
        return "暂无"
    return f"{int(round(float(value))):,}"


def format_percent_safe(value) -> str:
    if pd.isna(value):
        return "暂无"
    return f"{float(value):.1%}"


def safe_share(mask: pd.Series) -> float:
    if len(mask) == 0:
        return np.nan
    return float(mask.fillna(False).mean())


def prepare_display_table(df: pd.DataFrame, sort_cols: list[str], ascending: list[bool], limit: int = 20) -> pd.DataFrame:
    if df.empty:
        return df

    out = df.copy()
    for col in ["owners_mid", "total_reviews", "positive_rate", "platform_count", "release_year"]:
        out[col] = numeric_series(out, col)

    out = out.sort_values(sort_cols, ascending=ascending, na_position="last").head(limit)
    show_cols = get_available_columns(out, TABLE_COLUMNS)
    if not show_cols:
        return pd.DataFrame()

    display_df = out[show_cols].copy()
    if "release_year" in display_df.columns:
        display_df["release_year"] = display_df["release_year"].map(format_int)
    if "owners_mid" in display_df.columns:
        display_df["owners_mid"] = display_df["owners_mid"].map(format_int)
    if "total_reviews" in display_df.columns:
        display_df["total_reviews"] = display_df["total_reviews"].map(format_int)
    if "positive_rate" in display_df.columns:
        display_df["positive_rate"] = display_df["positive_rate"].map(format_percent_safe)
    if "platform_count" in display_df.columns:
        display_df["platform_count"] = display_df["platform_count"].map(format_int)
    if "price_bucket" in display_df.columns:
        display_df["price_bucket"] = map_display_series(display_df["price_bucket"], PRICE_BUCKET_LABELS)

    return display_df


st.title("市场洞察")
st.info("此页面使用 V0.2 分析特征。")


df = require_processed_data()
missing_required = [col for col in REQUIRED_V2_COLUMNS if col not in df.columns]
if missing_required:
    st.error(
        "此页面需要 V0.2 分析特征。缺失列："
        + ", ".join(missing_required)
        + "。请重新运行数据流水线以生成处理后数据。"
    )
    st.stop()

filtered_df = df.copy()
st.sidebar.header("市场洞察筛选")
selected_years = None
selected_buckets = []
review_floor = 0
selected_platform_range = None

if filtered_df["release_year"].notna().any():
    valid_years = numeric_series(filtered_df, "release_year").dropna()
    if not valid_years.empty:
        y_min = int(valid_years.min())
        y_max = int(valid_years.max())
        selected_years = st.sidebar.slider("发行年份", min_value=y_min, max_value=y_max, value=(y_min, y_max))
        filtered_df = filtered_df[numeric_series(filtered_df, "release_year").between(*selected_years)]

bucket_options = sorted(filtered_df["price_bucket"].dropna().astype(str).unique().tolist())
bucket_options = [b for b in PRICE_BUCKET_ORDER if b in bucket_options] + [b for b in bucket_options if b not in PRICE_BUCKET_ORDER]
if bucket_options:
    bucket_labels = {x: PRICE_BUCKET_LABELS.get(x, x) for x in bucket_options}
    selected_bucket_labels = st.sidebar.multiselect(
        "价格分层",
        options=[bucket_labels[x] for x in bucket_options],
        default=[bucket_labels[x] for x in bucket_options],
    )
    selected_buckets = [k for k, v in bucket_labels.items() if v in selected_bucket_labels]
    if selected_buckets:
        filtered_df = filtered_df[filtered_df["price_bucket"].astype(str).isin(selected_buckets)]

has_reviews_opt = st.sidebar.selectbox("是否有评论", options=["全部", "是", "否"], index=0)
if has_reviews_opt != "全部":
    expected = has_reviews_opt == "是"
    filtered_df = filtered_df[safe_column(filtered_df, "has_reviews", False).fillna(False) == expected]

is_free_opt = st.sidebar.selectbox("是否免费", options=["全部", "免费", "付费"], index=0)
if is_free_opt != "全部":
    expected = is_free_opt == "免费"
    filtered_df = filtered_df[safe_column(filtered_df, "is_free", False).fillna(False) == expected]

platform_values = numeric_series(filtered_df, "platform_count").dropna()
if not platform_values.empty:
    p_min, p_max = int(platform_values.min()), int(platform_values.max())
    selected_platform_range = st.sidebar.slider("平台数量", min_value=p_min, max_value=p_max, value=(p_min, p_max))
    filtered_df = filtered_df[numeric_series(filtered_df, "platform_count").between(*selected_platform_range)]

reviews_values = numeric_series(filtered_df, "total_reviews").dropna()
if not reviews_values.empty:
    review_floor = st.sidebar.slider("最小评论数（total_reviews）", min_value=0, max_value=int(reviews_values.max()), value=0)
    filtered_df = filtered_df[numeric_series(filtered_df, "total_reviews").fillna(0) >= review_floor]

st.caption(
    "筛选摘要："
    f"{len(filtered_df):,} 款游戏 | "
    f"发行年份： {f'{selected_years[0]}–{selected_years[1]}' if selected_years else '全部'} | "
    f"价格分层： {', '.join(PRICE_BUCKET_LABELS.get(x, x) for x in selected_buckets) if selected_buckets else '全部'} | "
    f"最小评论数（total_reviews）: {review_floor:,}"
)

if filtered_df.empty:
    st.warning("当前筛选条件下没有匹配游戏，请放宽年份、最低评论数或价格分层条件。")
    st.stop()

st.subheader("关键 KPI")
k1, k2, k3, k4, k5, k6 = st.columns(6)
with_reviews = filtered_df[safe_column(filtered_df, "has_reviews", False).fillna(False)]
k1.metric("游戏总数", format_int(len(filtered_df)))
k2.metric("有评论的游戏数", format_int(safe_column(filtered_df, "has_reviews", False).fillna(False).sum()))
k3.metric("估计拥有者数量中位数（owners_mid）", format_int(numeric_series(filtered_df, "owners_mid").median()))
k4.metric("好评率中位数", format_percent_safe(numeric_series(with_reviews, "positive_rate").median()))
k5.metric("免费游戏占比", format_percent_safe(safe_share(safe_column(filtered_df, "is_free", False))))
k6.metric("折扣游戏占比", format_percent_safe(safe_share(safe_column(filtered_df, "has_discount", False))))
st.caption("KPI 基于当前筛选样本计算，并对缺失值进行稳健处理。")

selected_section = st.radio("选择分析板块", ["市场结构", "评论与热度", "排行榜"], horizontal=True)

if selected_section == "市场结构":
    st.subheader("市场结构")

    st.caption("按 release_year 的游戏数量：筛选后的年度分布。")
    st.caption("最近年份和未来年份的数据可能不完整。")
    year_counts = numeric_series(filtered_df, "release_year").dropna().astype(int).value_counts().sort_index()
    if not year_counts.empty:
        st.bar_chart(year_counts)
    else:
        st.info("当前筛选条件下无发行年份数据。")

    st.caption("价格分层分布：不同定价区间的游戏数量。")
    bucket_series = map_display_series(safe_column(filtered_df, "price_bucket", "未知"), PRICE_BUCKET_LABELS)
    bucket_order = [x for x in PRICE_BUCKET_ORDER if x in bucket_series.unique()]
    bucket_remainder = sorted([x for x in bucket_series.unique() if x not in bucket_order])
    bucket_counts = bucket_series.value_counts().reindex(bucket_order + bucket_remainder, fill_value=0)
    if not bucket_counts.empty:
        st.bar_chart(bucket_counts)
    else:
        st.info("当前筛选条件下无价格分层数据。")

    st.caption("估计拥有者分层分布")
    owners_dist = numeric_series(filtered_df, "owners_mid").dropna()
    if not owners_dist.empty:
        bins = [-0.1, 0, 10_000, 50_000, 100_000, 500_000, 1_000_000, 10_000_000, np.inf]
        labels = ["0", "1–10k", "10k–50k", "50k–100k", "100k–500k", "500k–1M", "1M–10M", "10M+"]
        owners_tier = pd.cut(owners_dist, bins=bins, labels=labels, include_lowest=True, right=True)
        st.bar_chart(owners_tier.value_counts(sort=False))
        st.caption("owners_mid 是拥有者区间中点估计值，不代表精确销量。")
    else:
        st.info("无可用于分布绘图的有效 owners_mid 数据。")

    st.caption("评论热度信号分布：来自 V0.2 特征的质量/规模分层。")
    signal_series = map_display_series(safe_column(filtered_df, "review_signal", "未知"), REVIEW_SIGNAL_LABELS)
    signal_order = [x for x in REVIEW_SIGNAL_ORDER if x in signal_series.unique()]
    signal_remainder = sorted([x for x in signal_series.unique() if x not in signal_order])
    signal_counts = signal_series.value_counts().reindex(signal_order + signal_remainder, fill_value=0)
    if not signal_counts.empty:
        st.bar_chart(signal_counts)
    else:
        st.info("当前筛选条件下无 review_signal 数据。")

    st.caption("口碑情绪分布：筛选后游戏的情绪分组数量。")
    sentiment_series = map_display_series(safe_column(filtered_df, "review_sentiment", "未知"), REVIEW_SENTIMENT_LABELS)
    sentiment_order = [x for x in REVIEW_SENTIMENT_ORDER if x in sentiment_series.unique()]
    sentiment_remainder = sorted([x for x in sentiment_series.unique() if x not in sentiment_order])
    sentiment_counts = sentiment_series.value_counts().reindex(sentiment_order + sentiment_remainder, fill_value=0)
    if not sentiment_counts.empty:
        st.bar_chart(sentiment_counts)
    else:
        st.info("当前筛选条件下无 review_sentiment 数据。")

if selected_section == "评论与热度":
    st.subheader("评论与热度")
    st.caption("为提升渲染速度，散点图默认展示抽样结果。")

    st.caption("有评论游戏的 owners_mid 与好评率关系：拥有者规模与口碑关系。")
    st.caption("好评率对有评论的游戏更有参考意义。")
    scatter_a = filtered_df[
        safe_column(filtered_df, "has_reviews", False).fillna(False)
        & numeric_series(filtered_df, "owners_mid").notna()
        & numeric_series(filtered_df, "positive_rate").notna()
    ][["owners_mid", "positive_rate"]].copy()
    if not scatter_a.empty:
        scatter_a["owners_mid"] = pd.to_numeric(scatter_a["owners_mid"], errors="coerce")
        scatter_a = scatter_a.dropna().sort_values("owners_mid")
        if len(scatter_a) > MAX_SCATTER_POINTS:
            scatter_a = scatter_a.sample(n=MAX_SCATTER_POINTS, random_state=SCATTER_RANDOM_STATE)
        scatter_a = scatter_a.rename(columns={"owners_mid": "拥有者中位估计", "positive_rate": "好评率"})
        st.scatter_chart(scatter_a, x="拥有者中位估计", y="好评率")
    else:
        st.info("当前筛选条件下无可用于 owners_mid vs positive_rate 的有效数据。")

    st.caption("有评论游戏的 review_log 与好评率关系：评论量信号与口碑关系。")
    scatter_b = filtered_df[
        safe_column(filtered_df, "has_reviews", False).fillna(False)
        & numeric_series(filtered_df, "review_log").notna()
        & numeric_series(filtered_df, "positive_rate").notna()
    ][["review_log", "positive_rate"]].copy()
    if not scatter_b.empty:
        scatter_b = scatter_b.dropna()
        if len(scatter_b) > MAX_SCATTER_POINTS:
            scatter_b = scatter_b.sample(n=MAX_SCATTER_POINTS, random_state=SCATTER_RANDOM_STATE)
        scatter_b = scatter_b.rename(columns={"review_log": "评论量对数", "positive_rate": "好评率"})
        st.scatter_chart(scatter_b, x="评论量对数", y="好评率")
    else:
        st.info("当前筛选条件下无可用于 review_log vs positive_rate 的有效数据。")

if selected_section == "排行榜":
    st.subheader("市场机会与榜单")
    st.info("本页榜单优先读取后端生成的透明启发式结果，用于市场观察和机会识别，不代表机器学习预测、因果结论或个性化推荐。")

    ranking_section = st.radio("选择榜单板块", ["热门榜单", "高口碑榜单", "机会识别", "本地化机会", "风险观察"], horizontal=True)

    if ranking_section == "热门榜单":
        owners_ok = _show_ranking_section(
            "按估计拥有者数量排序的热门游戏",
            "top_games_by_owners",
            "该榜单基于后端排序表生成，仅用于描述市场关注度和规模，不代表精确销量。owners_mid 为拥有者区间中点估计。",
        )
        reviews_ok = _show_ranking_section(
            "按评论数排序的热门游戏",
            "top_games_by_reviews",
            "该榜单基于后端排序表生成，仅用于描述市场关注度和规模，不代表精确销量。owners_mid 为拥有者区间中点估计。",
        )

        if not owners_ok:
            top_owners_df = prepare_display_table(filtered_df, ["owners_mid", "total_reviews"], [False, False], limit=20)
            if not top_owners_df.empty:
                st.dataframe(rename_display_columns(top_owners_df), use_container_width=True)
        if not reviews_ok:
            top_reviews_df = prepare_display_table(filtered_df, ["total_reviews", "owners_mid"], [False, False], limit=20)
            if not top_reviews_df.empty:
                st.dataframe(rename_display_columns(top_reviews_df), use_container_width=True)

    elif ranking_section == "高口碑榜单":
        st.caption("该榜单要求达到最低评论数门槛，以减少少量评论造成的极端好评率误导。")
        if not _show_ranking_section("高口碑游戏榜", "top_rated_games", "该榜单为后端启发式筛选结果，用于描述性口碑观察。"):
            min_reviews_for_rating = max(20, int(numeric_series(filtered_df, "total_reviews").median()) if numeric_series(filtered_df, "total_reviews").notna().any() else 20)
            top_rated = filtered_df[numeric_series(filtered_df, "total_reviews").fillna(0) >= min_reviews_for_rating].copy()
            top_rated_df = prepare_display_table(top_rated, ["positive_rate", "total_reviews"], [False, False], limit=20)
            if not top_rated_df.empty:
                st.dataframe(rename_display_columns(top_rated_df), use_container_width=True)

    elif ranking_section == "机会识别":
        hidden_ok = _show_ranking_section("小众精品候选", "hidden_gems", "小众精品候选基于高好评率、最低评论数门槛和相对较低的估计拥有者数量筛选，属于透明启发式规则。")
        price_ok = _show_ranking_section("低价高口碑候选", "low_price_high_rating", "低价高口碑候选用于观察免费或低价区间中口碑较好的游戏，不代表投资建议或预测结果。")
        if not hidden_ok:
            hidden_gems = filtered_df[(numeric_series(filtered_df, "positive_rate") >= 0.85) & (numeric_series(filtered_df, "total_reviews") >= 20)].copy()
            if not hidden_gems.empty:
                owner_cutoff = numeric_series(hidden_gems, "owners_mid").median()
                hidden_gems = hidden_gems[numeric_series(hidden_gems, "owners_mid") <= owner_cutoff]
            hidden_gems_df = prepare_display_table(hidden_gems, ["positive_rate", "total_reviews"], [False, False], limit=20)
            if not hidden_gems_df.empty:
                st.dataframe(rename_display_columns(hidden_gems_df), use_container_width=True)

    elif ranking_section == "本地化机会":
        _show_ranking_section("已支持简中的潜力游戏", "chinese_supported_potential", "该榜单用于观察已支持简体中文、口碑较好但曝光相对有限的游戏。")
        loc_df = _load_table("localization_opportunities")
        st.caption("未支持简中的本地化机会候选")
        if loc_df is None:
            _show_missing_table_warning("localization_opportunities")
        else:
            if "supports_simplified_chinese" in loc_df.columns:
                loc_df = loc_df[loc_df["supports_simplified_chinese"].astype(str).str.lower().isin(["false", "0", "no"])]
            st.dataframe(_format_ranking_table(loc_df.head(30)), use_container_width=True)
            st.caption("该榜单用于观察尚未支持简体中文、但口碑和关注度较高的游戏，可作为中文本地化机会的描述性线索。")

    elif ranking_section == "风险观察":
        _show_ranking_section("高关注低口碑风险榜", "high_attention_low_rating", "该榜单用于识别评论量较高但好评率偏低的游戏，帮助观察潜在争议或口碑风险，并非负面评价结论。")
