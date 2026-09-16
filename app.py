import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Configuration (Industry Level UI)
st.set_page_config(
    page_title="Project FORESIGHT - Inventory Intelligence",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .metric-box { padding: 15px; border-radius: 8px; background-color: #f0f2f6; margin-bottom: 10px; }
    .stAlert { border-radius: 8px; }
    </style>
""", unsafe_allowed_html=True)

# 2. Data Loading Pipeline (Optimized with Cache)
@st.cache_data
def load_production_data():
    # Jupyter notebook se banei hui processed file load karna
    df = pd.read_csv("foresight_final_processed.csv")
    return df

try:
    df = load_production_data()
except FileNotFoundError:
    st.error("🚨 Error: 'foresight_final_processed.csv' nahi mili! Pehle Jupyter notebook ke saare cells run karein.")
    st.stop()

# 3. Sidebar Control Panel (What-If Scenarios)
st.sidebar.header("⚙️ Supply Chain Stress Test")
st.sidebar.markdown("Simulate sudden market changes to test inventory resilience.")

# Demand Surge Slider (What-if analysis)
demand_multiplier = st.sidebar.slider(
    "Simulate Demand Surge (Festival/Promo Season)", 
    min_value=1.0, max_value=2.5, value=1.0, step=0.1
)

# Apply what-if logic if user slides the value
if demand_multiplier > 1.0:
    df['Predicted_Demand'] = (df['Predicted_Demand'] * demand_multiplier).round().astype(int)
    # Recalculate status based on new high demand
    df['Inventory_Status'] = np.where(df['Quantity'] <= df['Reorder_Point'], '⚠️ REORDER NOW', '✅ STOCK OPTIMAL')
    df['Inventory_Status'] = np.where(df['Quantity'] > (df['Reorder_Point'] * 3), '🚨 OVERSTOCK RISK', df['Inventory_Status'])

# Filter by Risk Status
st.sidebar.subheader("🎯 Filter Dashboard")
status_filter = st.sidebar.multiselect(
    "Select Inventory Status to View:",
    options=df['Inventory_Status'].unique(),
    default=df['Inventory_Status'].unique()
)
filtered_df = df[df['inventory_status'].isin(status_filter)] if 'inventory_status' in df.columns else df[df['Inventory_Status'].isin(status_filter)]

# 4. Main Executive KPI Banner
st.title("🔮 Project FORESIGHT")
st.subheader("AI-Powered Demand & Inventory Intelligence Platform")
st.markdown("---")

# Calculating business metrics dynamically
total_skus = filtered_df['Product_ID'].nunique()
reorder_count = filtered_df[filtered_df['Inventory_Status'] == '⚠️ REORDER NOW'].shape[0]
overstock_count = filtered_df[filtered_df['Inventory_Status'] == '🚨 OVERSTOCK RISK'].shape[0]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="📊 Total Monitored SKUs", value=f"{total_skus:,}")
with col2:
    st.metric(label="⚠️ Critical Reorder Alerts", value=f"{reorder_count:,}", delta="Action Required", delta_color="inverse" if reorder_count > 0 else "normal")
with col3:
    st.metric(label="🚨 Overstock Risks Detected", value=f"{overstock_count:,}", delta="Capital Tied Up", delta_color="off")

st.markdown("---")

# 5. Interactive Visualizations (Analytics Layout)
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📈 Inventory Risk Distribution")
    status_counts = filtered_df['Inventory_Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    fig_pie = px.pie(status_counts, values='Count', names='Status', 
                     color='Status',
                     color_discrete_map={'✅ STOCK OPTIMAL':'#2ca02c', '⚠️ REORDER NOW':'#ff7f0e', '🚨 OVERSTOCK RISK':'#d62728'},
                     hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

with chart_col2:
    st.subheader("🛍️ Stock Levels: Actual vs Predicted Demand")
    # Top 15 products ka comparison plot
    top_products = filtered_df.groupby('Product_ID')[['Quantity', 'Predicted_Demand']].sum().reset_index().head(15)
    fig_bar = px.bar(top_products, x='Product_ID', y=['Quantity', 'Predicted_Demand'],
                     barmode='group',
                     labels={'value': 'Units', 'variable': 'Metric'},
                     title="Top 15 Products Stock Comparison")
    st.plotly_chart(fig_bar, use_container_width=True)

# 6. Actionable Operational Table & Export
st.markdown("---")
st.subheader("📋 Actionable Procurement & Replenishment Sheet")
st.markdown("Use this list for daily purchasing approvals and operational stock sorting.")

# Relevant columns showcase for business managers
display_cols = ['Product_ID', 'Quantity', 'Predicted_Demand', 'Safety_Stock', 'Reorder_Point', 'Inventory_Status']
st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)

# Enterprise Export to CSV Feature
@st.cache_data
def convert_df_to_csv(dataframe):
    return dataframe[display_cols].to_csv(index=False).encode('utf-8')

csv_data = convert_df_to_csv(filtered_df)

st.download_button(
    label="📥 Export Procurement Action Plan to CSV",
    data=csv_data,
    file_name="foresight_replenishment_report.csv",
    mime="text/csv",
    use_container_width=True
)
