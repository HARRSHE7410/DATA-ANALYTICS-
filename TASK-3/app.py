import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Deep-Dive Interactive BI Dashboard",
    layout="wide",
    page_icon="📊"
)

DARK_BG = "#0E1117"
DARK_TEXT = "#FFFFFF"
HIGHLIGHT = "#FFA54B"

st.markdown(
    f"""
    <style>
    .main {{background-color: {DARK_BG}; color: {DARK_TEXT};}}
    .stMetric-value {{color: {HIGHLIGHT};}}
    footer {{visibility: visible; color: {DARK_TEXT};}}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        text-align:center;
        font-size:40px;
        font-weight:bold;
        background: linear-gradient(90deg, #FF4B4B, #FFA500, #00FFAA, #FF4B4B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: slidebg 5s linear infinite;
    ">
        Deep-Dive Customer Analytics Dashboard
    </div>
    <style>
    @keyframes slidebg {
        0% {background-position:0%;}
        100% {background-position:200%;}
    }
    </style>
    """, unsafe_allow_html=True
)
st.markdown("<hr style='border:2px solid #FFA54B'>", unsafe_allow_html=True)

np.random.seed(42)
users = 500
data = pd.DataFrame({
    "user_id": range(1, users + 1),
    "signup_month": np.random.choice(pd.date_range("2024-01-01", periods=6, freq="MS").strftime("%Y-%m"), users),
    "visited": 1,
    "signed_up": np.random.choice([0, 1], users, p=[0.3, 0.7]),
    "purchased": np.random.choice([0, 1], users, p=[0.45, 0.55]),
    "revenue": np.random.randint(100, 2000, users),
    "churned": np.random.choice([0, 1], users, p=[0.25, 0.75]),
    "segment": np.random.choice(["Low Value", "Mid Value", "High Value"], users)
})

st.sidebar.header(" Filters")
segment_filter = st.sidebar.multiselect("Customer Segment", options=data["segment"].unique(), default=data["segment"].unique())
month_filter = st.sidebar.multiselect("Signup Month", options=data["signup_month"].unique(), default=data["signup_month"].unique())
purchase_filter = st.sidebar.selectbox("Purchase Status", options=["All", "Purchased Only", "Not Purchased Only"])

filtered_data = data[
    (data["segment"].isin(segment_filter)) &
    (data["signup_month"].isin(month_filter))
]

if purchase_filter == "Purchased Only":
    filtered_data = filtered_data[filtered_data["purchased"] == 1]
elif purchase_filter == "Not Purchased Only":
    filtered_data = filtered_data[filtered_data["purchased"] == 0]

orders = filtered_data[filtered_data["purchased"] == 1]

def calculate_kpis(df, orders_df):
    conv_rate = orders_df.shape[0] / df.shape[0] if df.shape[0] > 0 else 0
    churn_rate = df["churned"].sum() / df.shape[0] if df.shape[0] > 0 else 0
    aov = orders_df["revenue"].mean() if not orders_df.empty else 0
    avg_orders = orders_df.shape[0] / orders_df["user_id"].nunique() if not orders_df.empty else 0
    clv = aov * avg_orders
    return conv_rate, churn_rate, aov, clv

conversion_rate, churn_rate, aov, clv = calculate_kpis(filtered_data, orders)

funnel = pd.DataFrame({
    "Stage": ["Visited", "Signed Up", "Purchased"],
    "Users": [
        filtered_data["visited"].sum(),
        filtered_data["signed_up"].sum(),
        filtered_data["purchased"].sum()
    ]
})
funnel["Drop-off %"] = funnel["Users"].pct_change().fillna(0).apply(lambda x: f"{-x*100:.1f}%" if x<0 else "0%")

cohort = filtered_data.groupby("signup_month")["purchased"].mean().reset_index()

segment_analysis = filtered_data.groupby("segment")["revenue"].mean().reset_index()

tab1, tab2, tab3, tab4 = st.tabs(["Funnel Analysis", "Cohort Analysis", "Segment Analysis", "KPIs & Insights"])

with tab1:
    st.subheader("Funnel Analysis")
    fig = go.Figure(go.Funnel(
        y=funnel["Stage"],
        x=funnel["Users"],
        textinfo="value+percent initial"
    ))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"**Drop-off Details:** {funnel[['Stage','Drop-off %']].to_html(index=False)}", unsafe_allow_html=True)

with tab2:
    st.subheader("Cohort Conversion Rate")
    fig = go.Figure(go.Scatter(
        x=cohort["signup_month"],
        y=cohort["purchased"],
        mode="lines+markers+text",
        text=[f"{v:.1%}" for v in cohort["purchased"]],
        textposition="top center"
    ))
    fig.update_layout(yaxis_title="Conversion Rate", xaxis_title="Signup Month")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("Shows how signup month affects likelihood of purchase.")

with tab3:
    st.subheader(" Revenue by Customer Segment")
    fig = go.Figure(go.Bar(
        x=segment_analysis["segment"],
        y=segment_analysis["revenue"],
        marker_color=["#DD653D","#FFA500","#00FFAA"]
    ))
    fig.update_layout(yaxis_title="Avg Revenue", xaxis_title="Segment")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("High-value segments generate more revenue per customer.")

with tab4:
    st.subheader(" Key KPIs & Insights")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Conversion Rate", f"{conversion_rate:.2%}")
    col2.metric("Churn Rate", f"{churn_rate:.2%}")
    col3.metric("Average Order Value", f"₹{aov:,.0f}")
    col4.metric("Customer Lifetime Value", f"₹{clv:,.0f}")

    st.markdown("---")
    st.markdown("###  Insights")
    if conversion_rate < 0.4:
        st.markdown("- Conversion rate is low. Consider improving signup flow or promotional campaigns.")
    else:
        st.markdown("- Conversion rate is healthy. Keep monitoring trends.")

    if churn_rate > 0.3:
        st.markdown("- High churn detected. Focus on retention strategies.")
    else:
        st.markdown("- Customer retention is good.")

st.markdown("<hr style='border:1px solid #DD653D'>",unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#FFFFFF'>© 2025 Deep-Dive Analytics Dashboard. All rights reserved.</p>", unsafe_allow_html=True)

