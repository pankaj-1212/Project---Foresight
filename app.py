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

# 2. Custom CSS for Professional Look
css_style = """
<style>
.metric-box { padding: 15px; border-radius: 8px; background-color: #f0f2f6; margin-bottom: 10px; }
.stAlert { border-radius: 8px; }
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# 3. Data Loading Pipeline (Optimized with Cache)
@st.cache_data
def load_production_data():
    df = pd.read_csv("foresight_final_processed.csv")
    
    # Clean Column Names to handle casing issues dynamically
    df.columns = [col.strip() for col in df.columns]
    
    # Sahi column match karne ke liye custom mapping checking
    rename_dict = {}
    for col in df.columns:
        if col.lower() == 'inventory_status':
            rename_dict[col] = 'Inventory_Status'
        elif col.lower() == 'predicted_demand':
            rename_dict[col] = 'Predicted_Demand'
        elif col.lower() == 'safety_stock':
            rename_dict[col] = 'Safety_Stock'
        elif col.lower() == 'reorder_point':
            rename_dict[col] = 'Reorder_Point'
            
    if rename_dict:
        df = df.rename(columns=rename_dict)
        
    # Agar kisi wajah se column fir bhi nahi bana, toh yahan automatic logic safely fill kar dega
    if 'Inventory_Status' not in df.columns:
        conditions = [
            (df['Quantity'] <= df.get('Reorder_Point', df['Quantity'] * 0.5)),
            (df['Quantity'] > (df.get('Reorder_Point', df['Quantity'] * 0.5) * 3))
        ]
        choices = ['⚠️ REORDER NOW', '🚨 OVERSTOCK RISK']
        df['Inventory_Status'] = np.select(conditions, choices, default='✅ STOCK OPTIMAL')
        
    if 'Predicted_Demand' not in df.columns:
        df['Predicted_Demand'] = df['Quantity'].round().astype(int)
    if 'Safety_Stock' not in df.columns:
        df['Safety_Stock'] = (df['Quantity'] * 0.2).round().astype(int)
    if 'Reorder_Point' not in df.columns:
        df['Reorder_Point'] = (df['Quantity'] * 0.4).round().astype(int)
        
    return df

try:
    df = load_production_data()
except FileNotFoundError:
    st.error("🚨 Error: 'foresight_final_processed.csv' nahi mili! Pehle Jupyter notebook ke saare cells run karein.")
    st.stop()

# 4. Sidebar Control Panel (What-If Scenarios)
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
    df['Inventory_Status'] = np.where(df['Quantity'] <= df['Reorder_Point'], '⚠️ REORDER NOW', '✅ STOCK OPTIMAL')
    df['Inventory_Status'] = np.where(df['Quantity'] > (df['Reorder_Point'] * 3), '🚨 OVERSTOCK RISK', df['Inventory_Status'])

# Filter by Risk Status
st.sidebar.subheader("🎯 Filter Dashboard")
status_options = list(df['Inventory_Status'].unique())
status_filter = st.sidebar.multiselect(
    "Select Inventory Status to View:",
    options=status_options,
    default=status_options
)

filtered_df = df[df['Inventory_Status'].isin(status_filter)]

# 5. Main Executive KPI Banner
st.title("🔮 Project FORESIGHT")
st.subheader("AI-Powered Demand & Inventory Intelligence Platform")
st.markdown("---")

# Calculating business metrics dynamically
total_skus = filtered_df['Product_ID'].nunique()
reorder_count = len(filtered_df[filtered_df['Inventory_Status'] == '⚠️ REORDER NOW'])
overstock_count = len(filtered_df[filtered_df['Inventory_Status'] == '🚨 OVERSTOCK RISK'])

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="📊 Total Monitored SKUs", value=f"{total_skus:,}")
with col2:
    st.metric(label="⚠️ Critical Reorder Alerts", value=f"{reorder_count:,}", delta="Action Required" if reorder_count > 0 else "Normal", delta_color="inverse" if reorder_count > 0 else "normal")
with col3:
    st.metric(label="🚨 Overstock Risks Detected", value=f"{overstock_count:,}", delta="Capital Tied Up", delta_color="off")

st.markdown("---")

# 6. Interactive Visualizations (Analytics Layout)
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
    top_products = filtered_df.groupby('Product_ID')[['Quantity', 'Predicted_Demand']].sum().reset_index().head(15)
    fig_bar = px.bar(top_products, x='Product_ID', y=['Quantity', 'Predicted_Demand'],
                     barmode='group',
                     labels={'value': 'Units', 'variable': 'Metric'},
                     title="Top 15 Products Stock Comparison")
    st.plotly_chart(fig_bar, use_container_width=True)

# 7. Actionable Operational Table & Export
st.markdown("---")
st.subheader("📋 Actionable Procurement & Replenishment Sheet")
st.markdown("Use this list for daily purchasing approvals and operational stock sorting.")

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
