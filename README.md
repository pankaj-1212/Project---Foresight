# Project FORESIGHT – AI-Powered Demand & Supply Chain Intelligence Platform

Project FORESIGHT ek comprehensive end-to-end multi-tier production analytics environment hai jo enterprise supply chain management aur inventory pipelines ko dynamically track, validate aur forecast karne ke liye build kiya gaya hai.

## 🚀 System Components & Business Matrix
* **Data Sourcing Tier:** Direct programmatic cloud data ingestion layer using specific Kaggle API bindings inside a structured Jupyter Notebook sandbox.
* **ETL & Data Engineering:** Python (Pandas/NumPy standard data structures) layer ensuring clean data pipeline operations, structured type casting, and generation of the final `foresight_final_processed.csv`.
* **Predictive Architecture (Flask API Gateway):** Production-ready predictive backend architecture handling model inference orchestration logic.
* **Operational Frontend Portal (Streamlit Application):** Highly responsive UI controls ensuring rapid dynamic operational updates visualization.
* **Enterprise BI Suite (Advanced Power BI Engine):** Dual-page strategic metrics delivery engine engineered using customized clean corporate formatting guidelines.

---

## 📊 Power BI Semantic Layer Layout Mapping

Humara operational metrics suite 2 distinct reporting layouts control structures ko process karta hai:

### 1. Page 1: Strategic Business Insights
* **Revenue Metrics Tracking:** Monitors high-level commercial thresholds totaling \$1.99M in Gross Sales Amount fields.
* **Distribution Volume Control:** Displays core logistic volume processing across 24K registered item units.
* **Seasonal Time-Series View:** Optimized line visualizations mapping dynamic seasonal spikes chronologically from January to September.
* **Product Category Analytics:** High-impact Donut configuration segments showing market percentage split across core items (Cleats, Men's Footwear, Women's Apparel).

### 2. Page 2: Operational Inventory Alerts
* **Active Alert Calculation:** Uses specialized `REORDER NEEDED` system filtering logic to instantly aggregate low-stock warnings.
* **Dynamic Materialization Matrix (Table Visual):** High-level data grid mapping strict parameters for immediate warehouse adjustments: `Product_Name`, `Quantity` (Current Stock parameters), and `Safety_Stock`.
* **UX/UI Interface Polishing:** Modern clean dark background integration accented with 8-10px soft rounded borders bounding box visuals and micro-glow shadow matrices.

---

## 🛠️ System Deployment Guidelines

Ensure local framework initialization rules inside terminal environment blocks:

### 1. Library Dependencies Ingestion
```bash
pip install -r requirements.txt
```

### 2. Operational Server Gateway Startup
```bash
# Terminal 1: Initialize operational Flask model endpoint routing configurations
python app.py

# Terminal 2: Initialize responsive Streamlit client presentation portals
streamlit run main.py
```

### 3. Desktop BI Engine Analysis
Launch the fully configured `Project_Foresight_Dashboard.pbix` direct within Power BI Desktop sandbox environment to inspect local filters logic.