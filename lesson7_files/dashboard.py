"""
E-Commerce Sales Dashboard
A professional Streamlit dashboard for visualizing e-commerce sales data
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import data_loader
import business_metrics

# Page configuration
st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        height: 100%;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.5rem;
    }
    .metric-trend {
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    .trend-positive {
        color: #28a745;
    }
    .trend-negative {
        color: #dc3545;
    }
    .big-number {
        font-size: 3rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .stars {
        color: #ffc107;
        font-size: 2rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Constants
DATA_DIR = 'ecommerce_data'

@st.cache_data
def load_all_data():
    """Load all raw datasets"""
    orders, _, products, customers, reviews = data_loader.load_raw_data(DATA_DIR)
    return orders, products, customers, reviews

@st.cache_data
def prepare_filtered_data(year, month=None):
    """Prepare sales data for the selected year and optional month"""
    orders, products, customers, reviews = load_all_data()

    # Prepare sales data for current period
    sales_current = data_loader.prepare_sales_data(
        data_dir=DATA_DIR,
        year=year,
        month=month,
        include_delivery_metrics=True
    )

    # Prepare sales data for previous year
    sales_previous = data_loader.prepare_sales_data(
        data_dir=DATA_DIR,
        year=year - 1,
        month=month,
        include_delivery_metrics=True
    )

    return sales_current, sales_previous, orders, products, customers, reviews

def format_currency(value):
    """Format currency values as $300K or $2M"""
    if value >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"${value/1_000:.0f}K"
    else:
        return f"${value:.0f}"

def create_metric_card(label, value, trend=None, is_currency=True, is_percentage=False):
    """Create a metric card with trend indicator"""
    if is_currency:
        display_value = format_currency(value)
    elif is_percentage:
        display_value = f"{value:.2f}%"
    else:
        display_value = f"{value:,.0f}"

    trend_html = ""
    if trend is not None:
        trend_class = "trend-positive" if trend >= 0 else "trend-negative"
        trend_arrow = "↑" if trend >= 0 else "↓"
        trend_html = f'<div class="metric-trend {trend_class}">{trend_arrow} {abs(trend):.2f}%</div>'
    else:
        # Add empty div to maintain consistent card height
        trend_html = '<div class="metric-trend" style="visibility: hidden;">↑ 0.00%</div>'

    card_html = f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{display_value}</div>
        {trend_html}
    </div>
    """
    return card_html

def create_revenue_trend_chart(sales_current, sales_previous):
    """Create revenue trend line chart comparing current and previous periods"""
    # Aggregate by date
    current_daily = sales_current.groupby(sales_current['order_purchase_timestamp'].dt.date)['price'].sum().reset_index()
    current_daily.columns = ['date', 'revenue']
    current_daily = current_daily.sort_values('date')

    previous_daily = sales_previous.groupby(sales_previous['order_purchase_timestamp'].dt.date)['price'].sum().reset_index()
    previous_daily.columns = ['date', 'revenue']
    previous_daily = previous_daily.sort_values('date')

    # Create relative day index for overlay
    current_daily['day_index'] = range(len(current_daily))
    previous_daily['day_index'] = range(len(previous_daily))

    fig = go.Figure()

    # Previous period - dashed line (plot first so it's behind)
    fig.add_trace(go.Scatter(
        x=previous_daily['day_index'],
        y=previous_daily['revenue'],
        name='Previous Period',
        line=dict(color='#ff7f0e', width=2, dash='dash'),
        mode='lines',
        hovertemplate='Day %{x}<br>Revenue: $%{y:,.0f}<extra>Previous Period</extra>'
    ))

    # Current period - solid line (plot second so it's on top)
    fig.add_trace(go.Scatter(
        x=current_daily['day_index'],
        y=current_daily['revenue'],
        name='Current Period',
        line=dict(color='#1f77b4', width=2),
        mode='lines',
        hovertemplate='Day %{x}<br>Revenue: $%{y:,.0f}<extra>Current Period</extra>'
    ))

    # Calculate max revenue for y-axis
    max_revenue = max(current_daily['revenue'].max(), previous_daily['revenue'].max())

    fig.update_layout(
        title='Revenue Trend',
        xaxis_title='Day',
        yaxis_title='Revenue',
        hovermode='x unified',
        showlegend=True,
        height=400,
        yaxis=dict(
            gridcolor='rgba(128, 128, 128, 0.2)',
            tickformat='$,.0f',
            tickvals=[i for i in range(0, int(max_revenue) + 100000, 100000)],
            ticktext=[format_currency(i) for i in range(0, int(max_revenue) + 100000, 100000)]
        ),
        xaxis=dict(gridcolor='rgba(128, 128, 128, 0.2)'),
        plot_bgcolor='white'
    )

    return fig

def create_category_bar_chart(sales_data, products):
    """Create top 10 categories bar chart with blue gradient"""
    category_sales = business_metrics.get_product_category_sales(sales_data, products)
    top_10 = category_sales.head(10).sort_values('price', ascending=True)

    # Create blue gradient colors
    n_categories = len(top_10)
    colors = [f'rgba(65, 105, 225, {0.4 + (i / n_categories) * 0.6})' for i in range(n_categories)]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top_10['product_category_name'],
        x=top_10['price'],
        orientation='h',
        marker=dict(color=colors),
        text=[format_currency(val) for val in top_10['price']],
        textposition='outside',
        hovertemplate='%{y}<br>Revenue: $%{x:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title='Top 10 Product Categories',
        xaxis_title='Revenue',
        yaxis_title='',
        height=400,
        showlegend=False,
        xaxis=dict(
            tickformat='$,.0f',
            tickvals=[i for i in range(0, int(top_10['price'].max()) + 500000, 500000)],
            ticktext=[format_currency(i) for i in range(0, int(top_10['price'].max()) + 500000, 500000)]
        ),
        plot_bgcolor='white'
    )

    return fig

def create_state_choropleth(sales_data, orders, customers):
    """Create US choropleth map with blue gradient"""
    state_sales = business_metrics.get_sales_by_state(sales_data, orders, customers)

    fig = go.Figure(data=go.Choropleth(
        locations=state_sales['customer_state'],
        z=state_sales['price'],
        locationmode='USA-states',
        colorscale='Blues',
        colorbar_title="Revenue",
        hovertemplate='<b>%{location}</b><br>Revenue: $%{z:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title='Revenue by State',
        geo_scope='usa',
        height=400,
        margin=dict(l=0, r=0, t=40, b=0)
    )

    return fig

def create_delivery_satisfaction_chart(sales_data, reviews):
    """Create bar chart showing satisfaction vs delivery time"""
    review_by_delivery = business_metrics.get_review_by_delivery_time(sales_data, reviews)

    # Ensure proper ordering
    delivery_order = ['1-3 days', '4-7 days', '8+ days']
    review_by_delivery['delivery_time'] = pd.Categorical(
        review_by_delivery['delivery_time'],
        categories=delivery_order,
        ordered=True
    )
    review_by_delivery = review_by_delivery.sort_values('delivery_time')

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=review_by_delivery['delivery_time'],
        y=review_by_delivery['review_score'],
        marker=dict(color='#D8973C'),
        text=[f"{score:.2f}" for score in review_by_delivery['review_score']],
        textposition='outside',
        hovertemplate='%{x}<br>Avg Review: %{y:.2f}<extra></extra>'
    ))

    fig.update_layout(
        title='Average Review Score by Delivery Time',
        xaxis_title='Delivery Time',
        yaxis_title='Average Review Score',
        height=400,
        yaxis=dict(range=[0, 5], gridcolor='rgba(128, 128, 128, 0.2)'),
        showlegend=False,
        plot_bgcolor='white'
    )

    return fig

# Main app
def main():
    # Header with title and filters
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.title("E-Commerce Sales Dashboard")

    with col2:
        # Year dropdown
        available_years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
        selected_year = st.selectbox(
            "Year",
            options=available_years,
            index=available_years.index(2023) if 2023 in available_years else len(available_years) - 1,
            key="year_select"
        )

    with col3:
        # Month dropdown with "All Months" option
        month_options = ["All Months"] + [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        selected_month_str = st.selectbox(
            "Month",
            options=month_options,
            index=0,
            key="month_select"
        )

        # Convert month string to number
        if selected_month_str == "All Months":
            selected_month = None
        else:
            selected_month = month_options.index(selected_month_str)

    # Load filtered data
    sales_current, sales_previous, orders, products, customers, reviews = prepare_filtered_data(selected_year, selected_month)

    # Calculate metrics
    revenue_summary = business_metrics.generate_revenue_summary(sales_current, sales_previous)

    current_revenue = revenue_summary['current_revenue']
    revenue_growth = revenue_summary['revenue_growth'] * 100

    current_aov = revenue_summary['current_aov']
    aov_growth = revenue_summary['aov_growth'] * 100

    current_orders = revenue_summary['current_orders']
    order_growth = revenue_summary['order_growth'] * 100

    monthly_growth = revenue_summary['avg_monthly_growth'] * 100

    current_delivery_time = business_metrics.calculate_average_delivery_time(sales_current)
    previous_delivery_time = business_metrics.calculate_average_delivery_time(sales_previous) if len(sales_previous) > 0 else current_delivery_time
    delivery_trend = ((current_delivery_time - previous_delivery_time) / previous_delivery_time * 100) if previous_delivery_time > 0 else 0

    current_review_score = business_metrics.calculate_average_review_score(sales_current, reviews)

    st.markdown("<br>", unsafe_allow_html=True)

    # KPI Row - 4 cards
    kpi_cols = st.columns(4)

    with kpi_cols[0]:
        st.markdown(create_metric_card("Total Revenue", current_revenue, revenue_growth), unsafe_allow_html=True)

    with kpi_cols[1]:
        st.markdown(create_metric_card("Monthly Growth", monthly_growth, None, is_currency=False, is_percentage=True), unsafe_allow_html=True)

    with kpi_cols[2]:
        st.markdown(create_metric_card("Average Order Value", current_aov, aov_growth), unsafe_allow_html=True)

    with kpi_cols[3]:
        st.markdown(create_metric_card("Total Orders", current_orders, order_growth, is_currency=False), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts Grid - 2x2
    row1_cols = st.columns(2)

    with row1_cols[0]:
        # Revenue trend
        fig_revenue = create_revenue_trend_chart(sales_current, sales_previous)
        st.plotly_chart(fig_revenue, use_container_width=True)

    with row1_cols[1]:
        # Top categories
        fig_categories = create_category_bar_chart(sales_current, products)
        st.plotly_chart(fig_categories, use_container_width=True)

    row2_cols = st.columns(2)

    with row2_cols[0]:
        # State map
        fig_map = create_state_choropleth(sales_current, orders, customers)
        st.plotly_chart(fig_map, use_container_width=True)

    with row2_cols[1]:
        # Delivery satisfaction
        fig_delivery = create_delivery_satisfaction_chart(sales_current, reviews)
        st.plotly_chart(fig_delivery, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Bottom Row - 2 cards
    bottom_cols = st.columns(2)

    with bottom_cols[0]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average Delivery Time</div>
            <div class="metric-value">{current_delivery_time:.1f} days</div>
            <div class="metric-trend {'trend-positive' if delivery_trend < 0 else 'trend-negative'}">
                {'↓' if delivery_trend < 0 else '↑'} {abs(delivery_trend):.2f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    with bottom_cols[1]:
        stars = "★" * int(round(current_review_score))
        stars += "☆" * (5 - int(round(current_review_score)))

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average Review Score</div>
            <div class="metric-value">{current_review_score:.2f}</div>
            <div class="stars">{stars}</div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
