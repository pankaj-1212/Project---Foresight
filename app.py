import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration Set Up
st.set_page_config(page_title="Project FORESIGHT", page_icon="🔮", layout="wide")

st.title("🔮 Project FORESIGHT")
st.subheader("AI-Powered Demand Forecasting & Inventory Intelligence Platform")
st.markdown("---")

# 2. Load the final processed data
@st.cache_data
def load_data():
    data = pd.read_csv("foresight_final_processed.csv")
    return data

try:
    df = load_data()
    
    # 3. Sidebar Filters
    st.sidebar.header("Platform Navigation Filters")
    selected_category = st.sidebar.selectbox("Select Product Category", options=["All"] + list(df['Category'].unique()))
    
    if selected_category != "All":
        filtered_df = df[df['Category'] == selected_category]
    else:
        filtered_df = df

    # 4. Top Key Performance Indicators (KPIs) Metrics
    total_sales_val = filtered_df['Sales_Amount'].sum()
    total_items_sold = filtered_df['Quantity'].sum()
    avg_lead_time = filtered_df['Actual_Lead_Time'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Generated Revenue", f"${total_sales_val:,.2f}")
    col2.metric("Total Demand Volume (Units)", f"{total_items_sold:,}")
    col3.metric("Average Supplier Delivery Speed", f"{avg_lead_time:.1f} Days")
    
    st.markdown("---")

    # 5. Core Demand Forecasting Analytics Chart
    st.subheader("📊 Actual Historical Demand vs. AI-Predicted Demand Curve")
    
    monthly_trend = filtered_df.groupby('Month')[['Quantity', 'Predicted_Demand']].sum().reset_index()
    
    fig = px.line(monthly_trend, x='Month', y=['Quantity', 'Predicted_Demand'],
                  labels={'value': 'Units Sold / Predicted', 'Month': 'Month of Year'},
                  title=f"Demand Flow Chart for Category: {selected_category}",
                  markers=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")

    # 6. Inventory Intelligence Risk Assessment Console
    st.subheader("⚠️ Automated Stock Inventory Risk Monitoring Console")
    
    item_summary = filtered_df.groupby(['Product_ID', 'Product_Name']).agg(
        Current_Simulated_Stock=('Quantity', lambda x: int(x.mean() * 1.5)),
        Reorder_Threshold=('Reorder_Point', 'first'),
        Safety_Buffer=('Safety_Stock', 'first')
    ).reset_index()

    def assign_risk_status(row):
        if row['Current_Simulated_Stock'] <= row['Reorder_Threshold']:
            return "🚨 CRITICAL STOCKOUT RISK: REORDER NOW"
        elif row['Current_Simulated_Stock'] > (row['Reorder_Threshold'] * 2.5):
            return "⚠️ OVERSTOCK RISK: EXCESS HOLDING COSTS"
        else:
            return "✅ HEALTHY STOCK LEVEL"

    item_summary['System_Operational_Status'] = item_summary.apply(assign_risk_status, axis=1)
    
    st.dataframe(item_summary[['Product_ID', 'Product_Name', 'Current_Simulated_Stock', 'Reorder_Threshold', 'System_Operational_Status']], 
                 use_container_width=True, hide_index=True)

except FileNotFoundError:
    st.error("Error: Could not locate 'foresight_final_processed.csv'. Keep it in the same folder as app.py.")