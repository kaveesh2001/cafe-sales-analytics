import os
import sys


# =========================================================
# ADD PROJECT ROOT TO PYTHON PATH
# =========================================================

project_root = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(
    0,
    project_root
)


# =========================================================
# IMPORT LIBRARIES
# =========================================================

import pandas as pd
import streamlit as st
import plotly.express as px


# =========================================================
# IMPORT PROJECT MODULES
# =========================================================

from analytics.sales_analyzer import SalesAnalyzer

from pos import show_pos_page
from open_orders import show_open_orders_page
from orders import show_order_history
from products import show_product_management


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="My Café | POS & Analytics",
    page_icon="☕",
    layout="wide"
)


# =========================================================
# IMAGE URLS
# =========================================================

HERO_IMAGE = (
    "https://images.unsplash.com/"
    "photo-1759244328512-e4a9128150f4"
    "?auto=format&fit=crop&w=1800&q=85"
)

COFFEE_IMAGE = (
    "https://images.unsplash.com/"
    "photo-1525629545813-e4e7ba89e506"
    "?auto=format&fit=crop&w=900&q=85"
)

BURGER_IMAGE = (
    "https://images.unsplash.com/"
    "photo-1515215316771-2742baa337f4"
    "?auto=format&fit=crop&w=900&q=85"
)

CAFE_IMAGE = (
    "https://images.unsplash.com/"
    "photo-1554118811-1e0d58224f24"
    "?auto=format&fit=crop&w=900&q=85"
)


# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    section[data-testid="stSidebar"] {
        border-right: 1px solid #e5e7eb;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }

    div[data-testid="stPlotlyChart"] {
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 0.35rem;
        background: white;
    }

    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 1rem;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    .stButton > button {
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CREATE ANALYZER
# =========================================================

sales_analyzer = SalesAnalyzer()


# =========================================================
# MAIN NAVIGATION
# =========================================================

navigation_options = [
    "📊 Analytics Dashboard",
    "🛒 POS",
    "📋 Open Orders",
    "🧾 Order History",
    "🍔 Product Management"
]


# =========================================================
# NAVIGATION SESSION STATE
# =========================================================

if "navigation_page" not in st.session_state:

    st.session_state.navigation_page = (
        "📊 Analytics Dashboard"
    )


# =========================================================
# GO TO POS REQUEST
# =========================================================

if st.session_state.get(
    "go_to_pos",
    False
):

    st.session_state.navigation_page = (
        "🛒 POS"
    )

    st.session_state.go_to_pos = False


# =========================================================
# SELECTED NAVIGATION INDEX
# =========================================================

selected_index = navigation_options.index(
    st.session_state.navigation_page
)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

page = st.sidebar.radio(
    "Navigation",
    navigation_options,
    index=selected_index
)


# =========================================================
# KEEP MANUAL NAVIGATION IN SESSION STATE
# =========================================================

if page != st.session_state.navigation_page:

    st.session_state.navigation_page = page


# =========================================================
# POS PAGE
# =========================================================

if page == "🛒 POS":

    show_pos_page()

    st.stop()


# =========================================================
# OPEN ORDERS PAGE
# =========================================================

if page == "📋 Open Orders":

    show_open_orders_page()

    st.stop()


# =========================================================
# ORDER HISTORY PAGE
# =========================================================

if page == "🧾 Order History":

    show_order_history()

    st.stop()


# =========================================================
# PRODUCT MANAGEMENT PAGE
# =========================================================

if page == "🍔 Product Management":

    show_product_management()

    st.stop()


# =========================================================
# ANALYTICS DASHBOARD
# =========================================================


# =========================================================
# HERO SECTION
# =========================================================

st.html(
    f"""
    <style>

    .hero-container {{
        position: relative;
        min-height: 360px;
        border-radius: 22px;
        overflow: hidden;
        margin-bottom: 1.8rem;

        background-image:
            linear-gradient(
                90deg,
                rgba(0, 0, 0, 0.72),
                rgba(0, 0, 0, 0.35),
                rgba(0, 0, 0, 0.05)
            ),
            url("{HERO_IMAGE}");

        background-size: cover;
        background-position: center;

        display: flex;
        align-items: center;
    }}

    .hero-content {{
        padding: 3rem;
        max-width: 720px;
        color: white;
    }}

    .hero-small {{
        font-size: 0.95rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        opacity: 0.85;
        margin-bottom: 0.7rem;
    }}

    .hero-title {{
        font-size: 3.2rem;
        font-weight: 800;
        line-height: 1.05;
        margin-bottom: 0.8rem;
    }}

    .hero-description {{
        font-size: 1.08rem;
        line-height: 1.6;
        opacity: 0.92;
        margin-bottom: 0;
    }}

    </style>

    <div class="hero-container">

        <div class="hero-content">

            <div class="hero-small">
                WELCOME TO MY CAFÉ
            </div>

            <div class="hero-title">
                Smart Café<br>
                Management Dashboard
            </div>

            <div class="hero-description">
                Manage daily sales, monitor customer orders,
                track products and understand your café
                performance from one place.
            </div>

        </div>

    </div>
    """
)


# =========================================================
# CAFÉ OVERVIEW
# =========================================================

st.markdown(
    """
    <div style="
        font-size: 1.45rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    ">
        ☕ Café Overview
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        color: #6b7280;
        margin-bottom: 1rem;
    ">
        A quick look at your café operations and performance.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# GET SALES DATA
# =========================================================

dataframe = sales_analyzer.get_sales_data()


# =========================================================
# CHECK DATA
# =========================================================

if dataframe.empty:

    st.warning(
        "No completed sales data available yet."
    )

    st.info(
        "Create and complete a sale from the POS "
        "to start seeing analytics."
    )

    st.markdown(
        """
        <div style="
            font-size: 1.45rem;
            font-weight: 700;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
        ">
            ✨ Café Highlights
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            color: #6b7280;
            margin-bottom: 1rem;
        ">
            Explore some of the main areas of your café system.
        </div>
        """,
        unsafe_allow_html=True
    )

    photo_col1, photo_col2, photo_col3 = st.columns(3)


    # -----------------------------------------------------
    # COFFEE
    # -----------------------------------------------------

    with photo_col1:

        st.image(
            COFFEE_IMAGE,
            use_container_width=True
        )

        st.html(
            """
            <div style="
                padding: 0.9rem 1rem 1rem 1rem;
            ">

                <div style="
                    font-size: 1.05rem;
                    font-weight: 700;
                    margin-bottom: 0.2rem;
                ">
                    ☕ Coffee & Beverages
                </div>

                <div style="
                    font-size: 0.88rem;
                    color: #6b7280;
                ">
                    Monitor beverage sales and customer demand.
                </div>

            </div>
            """
        )


    # -----------------------------------------------------
    # FOOD
    # -----------------------------------------------------

    with photo_col2:

        st.image(
            BURGER_IMAGE,
            use_container_width=True
        )

        st.html(
            """
            <div style="
                padding: 0.9rem 1rem 1rem 1rem;
            ">

                <div style="
                    font-size: 1.05rem;
                    font-weight: 700;
                    margin-bottom: 0.2rem;
                ">
                    🍔 Food & Meals
                </div>

                <div style="
                    font-size: 0.88rem;
                    color: #6b7280;
                ">
                    Track popular food products and revenue.
                </div>

            </div>
            """
        )


    # -----------------------------------------------------
    # CAFÉ
    # -----------------------------------------------------

    with photo_col3:

        st.image(
            CAFE_IMAGE,
            use_container_width=True
        )

        st.html(
            """
            <div style="
                padding: 0.9rem 1rem 1rem 1rem;
            ">

                <div style="
                    font-size: 1.05rem;
                    font-weight: 700;
                    margin-bottom: 0.2rem;
                ">
                    🏪 Café Operations
                </div>

                <div style="
                    font-size: 0.88rem;
                    color: #6b7280;
                ">
                    Manage your café from one central system.
                </div>

            </div>
            """
        )

    st.stop()


# =========================================================
# CONVERT DATE COLUMN
# =========================================================

dataframe["order_date"] = pd.to_datetime(
    dataframe["order_date"]
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.markdown("---")

st.sidebar.title(
    "🔎 Dashboard Filters"
)

st.sidebar.caption(
    "Explore sales performance using filters."
)


# =========================================================
# DATE RANGE
# =========================================================

min_date = dataframe["order_date"].min()

max_date = dataframe["order_date"].max()

date_range = st.sidebar.date_input(
    "📅 Date Range",
    value=(
        min_date.date(),
        max_date.date()
    )
)


# =========================================================
# CATEGORY
# =========================================================

categories = sorted(
    dataframe["category"]
    .dropna()
    .unique()
    .tolist()
)

selected_categories = st.sidebar.multiselect(
    "📂 Category",
    options=categories,
    default=categories
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_dataframe = dataframe.copy()


# =========================================================
# DATE FILTER
# =========================================================

if len(date_range) == 2:

    start_date = pd.to_datetime(
        date_range[0]
    )

    end_date = pd.to_datetime(
        date_range[1]
    )

    end_date = (
        end_date
        + pd.Timedelta(days=1)
    )

    filtered_dataframe = filtered_dataframe[
        (
            filtered_dataframe["order_date"]
            >= start_date
        )
        &
        (
            filtered_dataframe["order_date"]
            < end_date
        )
    ]


# =========================================================
# CATEGORY FILTER
# =========================================================

if selected_categories:

    filtered_dataframe = filtered_dataframe[
        filtered_dataframe["category"].isin(
            selected_categories
        )
    ]

else:

    filtered_dataframe = filtered_dataframe.iloc[0:0]


# =========================================================
# CHECK FILTERED DATA
# =========================================================

if filtered_dataframe.empty:

    st.warning(
        "No sales data available for the selected filters."
    )

    st.stop()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_revenue = sales_analyzer.get_total_revenue(
    filtered_dataframe
)

total_orders = sales_analyzer.get_total_orders(
    filtered_dataframe
)

average_order_value = (
    sales_analyzer.get_average_order_value(
        filtered_dataframe
    )
)

best_product, quantity_sold = (
    sales_analyzer.get_best_selling_product(
        filtered_dataframe
    )
)


# =========================================================
# KPI SECTION
# =========================================================

st.markdown(
    """
    <div style="
        font-size: 1.45rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    ">
        📌 Key Performance Indicators
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        color: #6b7280;
        margin-bottom: 1rem;
    ">
        A quick snapshot of your café performance.
    </div>
    """,
    unsafe_allow_html=True
)

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)


# =========================================================
# KPI 1
# =========================================================

with kpi_col1:

    st.html(
        f"""
        <div style="
            background:white;
            border:1px solid #e5e7eb;
            border-radius:18px;

            padding:1.25rem;

            min-height:145px;

            box-shadow:
                0 5px 18px
                rgba(0,0,0,0.05);

            margin-bottom:0.5rem;
        ">

            <div style="
                font-size:0.9rem;
                color:#6b7280;
                margin-bottom:0.45rem;
            ">
                💰 Total Revenue
            </div>

            <div style="
                font-size:1.55rem;
                font-weight:750;
                color:#111827;

                margin-bottom:0.35rem;

                word-break:break-word;
            ">
                Rs. {total_revenue:,.2f}
            </div>

            <div style="
                font-size:0.8rem;
                color:#9ca3af;
            ">
                Revenue from completed orders
            </div>

        </div>
        """
    )


# =========================================================
# KPI 2
# =========================================================

with kpi_col2:

    st.html(
        f"""
        <div style="
            background:white;
            border:1px solid #e5e7eb;
            border-radius:18px;

            padding:1.25rem;

            min-height:145px;

            box-shadow:
                0 5px 18px
                rgba(0,0,0,0.05);

            margin-bottom:0.5rem;
        ">

            <div style="
                font-size:0.9rem;
                color:#6b7280;
                margin-bottom:0.45rem;
            ">
                🧾 Total Orders
            </div>

            <div style="
                font-size:1.55rem;
                font-weight:750;
                color:#111827;

                margin-bottom:0.35rem;
            ">
                {total_orders}
            </div>

            <div style="
                font-size:0.8rem;
                color:#9ca3af;
            ">
                Completed customer orders
            </div>

        </div>
        """
    )


# =========================================================
# KPI 3
# =========================================================

with kpi_col3:

    st.html(
        f"""
        <div style="
            background:white;
            border:1px solid #e5e7eb;
            border-radius:18px;

            padding:1.25rem;

            min-height:145px;

            box-shadow:
                0 5px 18px
                rgba(0,0,0,0.05);

            margin-bottom:0.5rem;
        ">

            <div style="
                font-size:0.9rem;
                color:#6b7280;
                margin-bottom:0.45rem;
            ">
                🛒 Average Order Value
            </div>

            <div style="
                font-size:1.55rem;
                font-weight:750;
                color:#111827;

                margin-bottom:0.35rem;

                word-break:break-word;
            ">
                Rs. {average_order_value:,.2f}
            </div>

            <div style="
                font-size:0.8rem;
                color:#9ca3af;
            ">
                Average revenue per order
            </div>

        </div>
        """
    )


# =========================================================
# KPI 4
# =========================================================

with kpi_col4:

    st.html(
        f"""
        <div style="
            background:white;
            border:1px solid #e5e7eb;
            border-radius:18px;

            padding:1.25rem;

            min-height:145px;

            box-shadow:
                0 5px 18px
                rgba(0,0,0,0.05);

            margin-bottom:0.5rem;
        ">

            <div style="
                font-size:0.9rem;
                color:#6b7280;
                margin-bottom:0.45rem;
            ">
                ⭐ Best-Selling Product
            </div>

            <div style="
                font-size:1.55rem;
                font-weight:750;
                color:#111827;

                margin-bottom:0.35rem;

                word-break:break-word;
            ">
                {best_product}
            </div>

            <div style="
                font-size:0.8rem;
                color:#9ca3af;
            ">
                {quantity_sold} units sold
            </div>

        </div>
        """
    )


# =========================================================
# CAFÉ HIGHLIGHTS
# =========================================================

st.markdown(
    """
    <div style="
        font-size:1.45rem;
        font-weight:700;

        margin-top:1.5rem;
        margin-bottom:0.8rem;
    ">
        ✨ Café Highlights
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        color:#6b7280;
        margin-bottom:1rem;
    ">
        A visual snapshot of the café experience.
    </div>
    """,
    unsafe_allow_html=True
)

photo_col1, photo_col2, photo_col3 = st.columns(3)


# =========================================================
# COFFEE CARD
# =========================================================

with photo_col1:

    st.image(
        COFFEE_IMAGE,
        use_container_width=True
    )

    st.html(
        """
        <div style="
            padding:0.9rem 1rem 1rem 1rem;
        ">

            <div style="
                font-size:1.05rem;
                font-weight:700;
                margin-bottom:0.2rem;
            ">
                ☕ Coffee & Beverages
            </div>

            <div style="
                font-size:0.88rem;
                color:#6b7280;
            ">
                Track beverage demand and revenue
                throughout the day.
            </div>

        </div>
        """
    )


# =========================================================
# FOOD CARD
# =========================================================

with photo_col2:

    st.image(
        BURGER_IMAGE,
        use_container_width=True
    )

    st.html(
        """
        <div style="
            padding:0.9rem 1rem 1rem 1rem;
        ">

            <div style="
                font-size:1.05rem;
                font-weight:700;
                margin-bottom:0.2rem;
            ">
                🍔 Food & Meals
            </div>

            <div style="
                font-size:0.88rem;
                color:#6b7280;
            ">
                Understand which products generate
                the most sales.
            </div>

        </div>
        """
    )


# =========================================================
# CAFÉ CARD
# =========================================================

with photo_col3:

    st.image(
        CAFE_IMAGE,
        use_container_width=True
    )

    st.html(
        """
        <div style="
            padding:0.9rem 1rem 1rem 1rem;
        ">

            <div style="
                font-size:1.05rem;
                font-weight:700;
                margin-bottom:0.2rem;
            ">
                🏪 Café Experience
            </div>

            <div style="
                font-size:0.88rem;
                color:#6b7280;
            ">
                Connect POS operations with
                business analytics.
            </div>

        </div>
        """
    )


# =========================================================
# SALES OVERVIEW
# =========================================================

st.markdown(
    """
    <div style="
        font-size:1.45rem;
        font-weight:700;

        margin-top:1.5rem;
        margin-bottom:0.8rem;
    ">
        📊 Sales Overview
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        color:#6b7280;
        margin-bottom:1rem;
    ">
        Understand how your revenue changes across
        categories and dates.
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# =========================================================
# REVENUE BY CATEGORY
# =========================================================

with col1:

    category_data = (
        sales_analyzer
        .get_category_analysis(
            filtered_dataframe
        )
        .reset_index()
    )

    category_chart = px.bar(
        category_data,
        x="category",
        y="total_revenue",
        title="Revenue by Product Category",
        labels={
            "category": "Category",
            "total_revenue": "Revenue (Rs.)"
        },
        text="total_revenue"
    )

    category_chart.update_traces(
        texttemplate="Rs. %{text:.2f}",
        textposition="outside"
    )

    category_chart.update_layout(
        xaxis_title="Category",
        yaxis_title="Revenue (Rs.)",

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    st.plotly_chart(
        category_chart,
        width="stretch"
    )


# =========================================================
# DAILY REVENUE
# =========================================================

with col2:

    daily_data = (
        sales_analyzer.get_daily_sales(
            filtered_dataframe
        )
    )

    daily_chart = px.line(
        daily_data,
        x="order_date",
        y="subtotal",
        markers=True,
        title="Daily Revenue Trend",
        labels={
            "order_date": "Date",
            "subtotal": "Revenue (Rs.)"
        }
    )

    daily_chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Revenue (Rs.)",

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    st.plotly_chart(
        daily_chart,
        width="stretch"
    )


# =========================================================
# SALES ACTIVITY
# =========================================================

st.markdown(
    """
    <div style="
        font-size:1.45rem;
        font-weight:700;

        margin-top:1.5rem;
        margin-bottom:0.8rem;
    ">
        🕐 Sales Activity
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        color:#6b7280;
        margin-bottom:1rem;
    ">
        Identify the busiest sales periods of the day.
    </div>
    """,
    unsafe_allow_html=True
)

hourly_data = (
    sales_analyzer.get_hourly_sales(
        filtered_dataframe
    )
)

hourly_data["hour_label"] = (
    hourly_data["hour"].astype(str)
    + ":00"
)

hourly_chart = px.bar(
    hourly_data,
    x="hour_label",
    y="quantity",
    title="Sales Quantity by Hour",
    labels={
        "hour_label": "Hour",
        "quantity": "Items Sold"
    },
    text="quantity"
)

hourly_chart.update_traces(
    textposition="outside"
)

hourly_chart.update_layout(
    xaxis_title="Hour",
    yaxis_title="Items Sold",

    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)

st.plotly_chart(
    hourly_chart,
    width="stretch"
)


# =========================================================
# PRODUCT PERFORMANCE
# =========================================================

st.markdown(
    """
    <div style="
        font-size:1.45rem;
        font-weight:700;

        margin-top:1.5rem;
        margin-bottom:0.8rem;
    ">
        🍔 Product Performance
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        color:#6b7280;
        margin-bottom:1rem;
    ">
        Compare products by units sold and generated revenue.
    </div>
    """,
    unsafe_allow_html=True
)

product_data = (
    sales_analyzer
    .get_product_performance(
        filtered_dataframe
    )
    .reset_index()
)

col1, col2 = st.columns(2)


# =========================================================
# QUANTITY SOLD
# =========================================================

with col1:

    product_quantity_chart = px.bar(
        product_data,
        x="product_name",
        y="total_quantity",
        title="Quantity Sold by Product",
        labels={
            "product_name": "Product",
            "total_quantity": "Quantity Sold"
        },
        text="total_quantity"
    )

    product_quantity_chart.update_traces(
        textposition="outside"
    )

    product_quantity_chart.update_layout(
        xaxis_title="Product",
        yaxis_title="Quantity Sold",

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    st.plotly_chart(
        product_quantity_chart,
        width="stretch"
    )


# =========================================================
# REVENUE BY PRODUCT
# =========================================================

with col2:

    product_revenue_data = (
        product_data
        .sort_values(
            "total_revenue",
            ascending=False
        )
    )

    product_revenue_chart = px.bar(
        product_revenue_data,
        x="product_name",
        y="total_revenue",
        title="Revenue by Product",
        labels={
            "product_name": "Product",
            "total_revenue": "Revenue (Rs.)"
        },
        text="total_revenue"
    )

    product_revenue_chart.update_traces(
        texttemplate="Rs. %{text:.2f}",
        textposition="outside"
    )

    product_revenue_chart.update_layout(
        xaxis_title="Product",
        yaxis_title="Revenue (Rs.)",

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    st.plotly_chart(
        product_revenue_chart,
        width="stretch"
    )


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

st.markdown(
    """
    <div style="
        font-size:1.45rem;
        font-weight:700;

        margin-top:1.5rem;
        margin-bottom:0.8rem;
    ">
        💡 Business Insights
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        color:#6b7280;
        margin-bottom:1rem;
    ">
        Key patterns identified from your sales data.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TOP CATEGORY
# =========================================================

top_category = "N/A"

top_category_revenue = 0.0


if not category_data.empty:

    top_category_row = (
        category_data
        .sort_values(
            "total_revenue",
            ascending=False
        )
        .iloc[0]
    )

    top_category = (
        top_category_row["category"]
    )

    top_category_revenue = float(
        top_category_row["total_revenue"]
    )


# =========================================================
# PEAK HOUR
# =========================================================

peak_hour = "N/A"

peak_hour_quantity = 0


if not hourly_data.empty:

    peak_hour_row = (
        hourly_data
        .sort_values(
            "quantity",
            ascending=False
        )
        .iloc[0]
    )

    peak_hour = (
        str(
            peak_hour_row["hour"]
        )
        + ":00"
    )

    peak_hour_quantity = int(
        peak_hour_row["quantity"]
    )


# =========================================================
# BUSINESS INSIGHT CARDS
# =========================================================

insight_col1, insight_col2, insight_col3, insight_col4 = (
    st.columns(4)
)


# =========================================================
# REVENUE INSIGHT
# =========================================================

with insight_col1:

    st.html(
        f"""
        <div style="
            background:white;

            border:1px solid #e5e7eb;

            border-radius:18px;

            padding:1.2rem;

            min-height:155px;

            box-shadow:
                0 5px 18px
                rgba(0,0,0,0.04);

            margin-bottom:1rem;
        ">

            <div style="
                font-size:1.7rem;
                margin-bottom:0.45rem;
            ">
                💰
            </div>

            <div style="
                font-size:0.9rem;
                color:#6b7280;
                margin-bottom:0.3rem;
            ">
                Total Revenue
            </div>

            <div style="
                font-size:1.25rem;
                font-weight:750;
                color:#111827;
                margin-bottom:0.25rem;
                word-break:break-word;
            ">
                Rs. {total_revenue:,.2f}
            </div>

            <div style="
                font-size:0.8rem;
                color:#9ca3af;
                line-height:1.45;
            ">
                Revenue generated from completed
                customer orders.
            </div>

        </div>
        """
    )


# =========================================================
# BEST SELLER INSIGHT
# =========================================================

with insight_col2:

    st.html(
        f"""
        <div style="
            background:white;

            border:1px solid #e5e7eb;

            border-radius:18px;

            padding:1.2rem;

            min-height:155px;

            box-shadow:
                0 5px 18px
                rgba(0,0,0,0.04);

            margin-bottom:1rem;
        ">

            <div style="
                font-size:1.7rem;
                margin-bottom:0.45rem;
            ">
                🍔
            </div>

            <div style="
                font-size:0.9rem;
                color:#6b7280;
                margin-bottom:0.3rem;
            ">
                Best Seller
            </div>

            <div style="
                font-size:1.25rem;
                font-weight:750;
                color:#111827;
                margin-bottom:0.25rem;
                word-break:break-word;
            ">
                {best_product}
            </div>

            <div style="
                font-size:0.8rem;
                color:#9ca3af;
                line-height:1.45;
            ">
                {quantity_sold} units sold
                during the selected period.
            </div>

        </div>
        """
    )


# =========================================================
# TOP CATEGORY INSIGHT
# =========================================================

with insight_col3:

    st.html(
        f"""
        <div style="
            background:white;

            border:1px solid #e5e7eb;

            border-radius:18px;

            padding:1.2rem;

            min-height:155px;

            box-shadow:
                0 5px 18px
                rgba(0,0,0,0.04);

            margin-bottom:1rem;
        ">

            <div style="
                font-size:1.7rem;
                margin-bottom:0.45rem;
            ">
                📂
            </div>

            <div style="
                font-size:0.9rem;
                color:#6b7280;
                margin-bottom:0.3rem;
            ">
                Top Revenue Category
            </div>

            <div style="
                font-size:1.25rem;
                font-weight:750;
                color:#111827;
                margin-bottom:0.25rem;
                word-break:break-word;
            ">
                {top_category}
            </div>

            <div style="
                font-size:0.8rem;
                color:#9ca3af;
                line-height:1.45;
            ">
                Rs. {top_category_revenue:,.2f}
                revenue generated.
            </div>

        </div>
        """
    )


# =========================================================
# PEAK HOUR INSIGHT
# =========================================================

with insight_col4:

    st.html(
        f"""
        <div style="
            background:white;

            border:1px solid #e5e7eb;

            border-radius:18px;

            padding:1.2rem;

            min-height:155px;

            box-shadow:
                0 5px 18px
                rgba(0,0,0,0.04);

            margin-bottom:1rem;
        ">

            <div style="
                font-size:1.7rem;
                margin-bottom:0.45rem;
            ">
                🕐
            </div>

            <div style="
                font-size:0.9rem;
                color:#6b7280;
                margin-bottom:0.3rem;
            ">
                Peak Sales Hour
            </div>

            <div style="
                font-size:1.25rem;
                font-weight:750;
                color:#111827;
                margin-bottom:0.25rem;
            ">
                {peak_hour}
            </div>

            <div style="
                font-size:0.8rem;
                color:#9ca3af;
                line-height:1.45;
            ">
                {peak_hour_quantity} items sold
                around this time.
            </div>

        </div>
        """
    )


# =========================================================
# DETAILED BUSINESS INSIGHTS
# =========================================================

with st.expander(
    "💬 View Detailed Business Insights"
):

    insights = (
        sales_analyzer.generate_business_insights(
            filtered_dataframe
        )
    )


    if insights:

        for insight in insights:

            st.info(
                f"💡 {insight}"
            )

    else:

        st.info(
            "No additional business insights available."
        )


# =========================================================
# DETAILED SALES DATA
# =========================================================

with st.expander(
    "📋 View Detailed Sales Data"
):

    st.caption(
        f"Showing {len(filtered_dataframe)} "
        f"sales records based on the selected filters."
    )


    st.dataframe(
        filtered_dataframe,
        width="stretch",
        hide_index=True
    )


# =========================================================
# FOOTER
# =========================================================

st.html(
    """
    <div style="
        text-align:center;

        color:#9ca3af;

        padding:2rem 0 1rem 0;

        font-size:0.85rem;
    ">

        ☕ My Café POS & Analytics System

        <br>

        Smart Sales Management & Business Insights

    </div>
    """
)