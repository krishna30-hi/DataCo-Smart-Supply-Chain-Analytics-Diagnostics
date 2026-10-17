"""
export_results.py
------------------
Connects to your local MySQL database, runs every business-question
query from supply_chain_full_FINAL.sql, and writes each result set
into its own sheet of one Excel workbook.

SETUP (run once in a terminal/command prompt):
    pip install sqlalchemy pymysql pandas openpyxl

USAGE:
    python export_results.py
"""

from sqlalchemy import create_engine, text
import pandas as pd

# ------------------------------------------------------------
# 1. EDIT THESE to match your MySQL setup
# ------------------------------------------------------------
USER = "root"
PASSWORD = "MyNewPass2026"
HOST = "localhost"
PORT = 3306
DATABASE = "supply_chain_db"

engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

# ------------------------------------------------------------
# 2. Every query, with a short sheet name (max 31 chars for Excel)
# ------------------------------------------------------------
queries = {
    "Validation": """
        SELECT COUNT(*) AS total_records FROM supply_chain
    """,
    "Late Delivery Risk": """
        SELECT SUM(late_delivery_risk) AS late_risk_shipments, COUNT(*) AS total_shipments,
               ROUND(100 * SUM(late_delivery_risk) / COUNT(*), 1) AS late_delivery_risk_pct
        FROM supply_chain
    """,
    "Std Class Ship Duration": """
        SELECT shipping_mode, COUNT(*) AS shipment_count,
               ROUND(AVG(shipping_duration), 2) AS avg_shipping_duration_days
        FROM supply_chain WHERE shipping_mode = 'Standard Class' GROUP BY shipping_mode
    """,
    "Loss Orders": """
        SELECT SUM(CASE WHEN order_profit_per_order < 0 THEN 1 ELSE 0 END) AS loss_making_orders,
               COUNT(*) AS total_orders,
               ROUND(100 * SUM(CASE WHEN order_profit_per_order < 0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS loss_order_pct
        FROM supply_chain
    """,
    "Sales Summary": """
        SELECT MIN(sales) min_sale, MAX(sales) max_sale, ROUND(AVG(sales),2) avg_sale,
               ROUND(STDDEV(sales),2) std_sale, COUNT(*) total_orders
        FROM supply_chain
    """,
    "Monthly Sales": """
        SELECT order_month, order_month_name, ROUND(SUM(sales),2) total_sales
        FROM supply_chain GROUP BY order_month, order_month_name ORDER BY order_month
    """,
    "Yearly Sales": """
        SELECT order_year, ROUND(SUM(sales),2) total_sales, COUNT(*) order_count
        FROM supply_chain GROUP BY order_year ORDER BY order_year
    """,
    "Sales Category": """
        SELECT sales_category, ROUND(AVG(sales),2) avg_sales, ROUND(AVG(order_profit_per_order),2) avg_profit
        FROM supply_chain GROUP BY sales_category ORDER BY FIELD(sales_category,'Low','Medium','High')
    """,
    "Top Categories": """
        SELECT category_name, ROUND(SUM(sales),2) total_sales, COUNT(*) order_count
        FROM supply_chain GROUP BY category_name ORDER BY total_sales DESC LIMIT 10
    """,
    "Top Products": """
        SELECT product_name, ROUND(SUM(sales),2) total_sales
        FROM supply_chain GROUP BY product_name ORDER BY total_sales DESC LIMIT 10
    """,
    "Dept Sales": """
        SELECT department_name, ROUND(SUM(sales),2) total_sales, ROUND(SUM(order_profit_per_order),2) total_profit
        FROM supply_chain GROUP BY department_name ORDER BY total_sales DESC
    """,
    "Market Sales": """
        SELECT market, ROUND(SUM(sales),2) total_sales FROM supply_chain GROUP BY market ORDER BY total_sales DESC
    """,
    "Region Sales": """
        SELECT order_region, ROUND(SUM(sales),2) total_sales
        FROM supply_chain GROUP BY order_region ORDER BY total_sales DESC LIMIT 10
    """,
    "Country Sales": """
        SELECT order_country, ROUND(SUM(sales),2) total_sales
        FROM supply_chain GROUP BY order_country ORDER BY total_sales DESC LIMIT 10
    """,
    "Customer Segment": """
        SELECT customer_segment, ROUND(SUM(sales),2) total_sales, COUNT(DISTINCT customer_id) unique_customers
        FROM supply_chain GROUP BY customer_segment ORDER BY total_sales DESC
    """,
    "Top Customers": """
        SELECT customer_id, ROUND(SUM(sales),2) total_sales
        FROM supply_chain GROUP BY customer_id ORDER BY total_sales DESC LIMIT 10
    """,
    "Shipping Mode": """
        SELECT shipping_mode, COUNT(*) order_count FROM supply_chain GROUP BY shipping_mode ORDER BY order_count DESC
    """,
    "Delivery Status": """
        SELECT delivery_status, COUNT(*) order_count FROM supply_chain GROUP BY delivery_status ORDER BY order_count DESC
    """,
    "Shipping Performance": """
        SELECT shipping_performance, COUNT(*) order_count FROM supply_chain GROUP BY shipping_performance
    """,
    "Perf vs Delivery Status": """
        SELECT shipping_performance,
               SUM(delivery_status='Advance shipping') advance_shipping,
               SUM(delivery_status='Late delivery') late_delivery,
               SUM(delivery_status='Shipping canceled') shipping_canceled,
               SUM(delivery_status='Shipping on time') shipping_on_time
        FROM supply_chain GROUP BY shipping_performance
    """,
    "Late Risk Counts": """
        SELECT late_delivery_risk, COUNT(*) order_count FROM supply_chain GROUP BY late_delivery_risk
    """,
    "Order Status": """
        SELECT order_status, COUNT(*) order_count FROM supply_chain GROUP BY order_status ORDER BY order_count DESC
    """,
    "Fraud by Market": """
        SELECT market, COUNT(*) fraud_orders FROM supply_chain
        WHERE order_status='SUSPECTED_FRAUD' GROUP BY market ORDER BY fraud_orders DESC
    """,
    "Fraud by Shipping Mode": """
        SELECT shipping_mode, COUNT(*) fraud_orders FROM supply_chain
        WHERE order_status='SUSPECTED_FRAUD' GROUP BY shipping_mode ORDER BY fraud_orders DESC
    """,
    "Fraud by Segment": """
        SELECT customer_segment, COUNT(*) fraud_orders FROM supply_chain
        WHERE order_status='SUSPECTED_FRAUD' GROUP BY customer_segment ORDER BY fraud_orders DESC
    """,
    "Market x Segment": """
        SELECT market, customer_segment, ROUND(SUM(sales),2) total_sales, ROUND(SUM(order_profit_per_order),2) total_profit
        FROM supply_chain GROUP BY market, customer_segment ORDER BY market, total_sales DESC
    """,
    "Late Rate by Ship Mode": """
        SELECT shipping_mode, COUNT(*) total_orders, SUM(late_delivery_risk) late_orders,
               ROUND(100*SUM(late_delivery_risk)/COUNT(*),2) late_delivery_rate_pct
        FROM supply_chain GROUP BY shipping_mode ORDER BY late_delivery_rate_pct DESC
    """,
    "Worst Margin Categories": """
        SELECT category_name, ROUND(SUM(sales),2) total_sales, ROUND(SUM(order_profit_per_order),2) total_profit,
               ROUND(100*SUM(order_profit_per_order)/NULLIF(SUM(sales),0),2) margin_pct
        FROM supply_chain GROUP BY category_name ORDER BY total_profit ASC LIMIT 10
    """,
    "Customer 360": """
        SELECT customer_id, MAX(customer_segment) segment, MAX(market) primary_market,
               ROUND(SUM(sales),2) total_sales, COUNT(*) order_count,
               SUM(CASE WHEN order_status = 'SUSPECTED_FRAUD' THEN 1 ELSE 0 END) fraud_flags
        FROM supply_chain GROUP BY customer_id ORDER BY total_sales DESC LIMIT 20
    """,
}

# ------------------------------------------------------------
# 3. Run every query and write results to one Excel workbook
# ------------------------------------------------------------
output_file = "supply_chain_query_results.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    with engine.connect() as conn:
        for sheet_name, sql in queries.items():
            print(f"Running: {sheet_name} ...")
            df = pd.read_sql(text(sql), conn)
            # Excel sheet names max 31 characters
            safe_name = sheet_name[:31]
            df.to_excel(writer, sheet_name=safe_name, index=False)

print(f"\nDone. Saved to {output_file}")
PASSWORD = "MyNewPass2026"
