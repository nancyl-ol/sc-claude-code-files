"""
Business Metrics Calculation Module

This module contains functions for calculating various business metrics
including revenue, growth rates, product performance, and customer experience metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple


def calculate_total_revenue(sales_data: pd.DataFrame) -> float:
    """
    Calculate total revenue from sales data.

    Parameters
    ----------
    sales_data : DataFrame
        Sales dataset with price column

    Returns
    -------
    float
        Total revenue
    """
    return sales_data['price'].sum()


def calculate_revenue_growth(current_revenue: float, previous_revenue: float) -> float:
    """
    Calculate revenue growth rate as a percentage.

    Parameters
    ----------
    current_revenue : float
        Revenue for current period
    previous_revenue : float
        Revenue for previous period

    Returns
    -------
    float
        Revenue growth rate as a decimal (e.g., 0.05 for 5% growth)
    """
    if previous_revenue == 0:
        return 0.0

    return (current_revenue - previous_revenue) / previous_revenue


def calculate_monthly_growth(sales_data: pd.DataFrame) -> pd.Series:
    """
    Calculate month-over-month revenue growth rates.

    Parameters
    ----------
    sales_data : DataFrame
        Sales dataset with month and price columns

    Returns
    -------
    Series
        Monthly growth rates indexed by month
    """
    monthly_revenue = sales_data.groupby('month')['price'].sum()
    monthly_growth = monthly_revenue.pct_change()

    return monthly_growth


def calculate_average_monthly_growth(monthly_growth: pd.Series) -> float:
    """
    Calculate average monthly growth rate.

    Parameters
    ----------
    monthly_growth : Series
        Monthly growth rates

    Returns
    -------
    float
        Average monthly growth rate
    """
    return monthly_growth.mean()


def calculate_average_order_value(sales_data: pd.DataFrame) -> float:
    """
    Calculate average order value (AOV).

    Parameters
    ----------
    sales_data : DataFrame
        Sales dataset with order_id and price columns

    Returns
    -------
    float
        Average order value
    """
    order_totals = sales_data.groupby('order_id')['price'].sum()
    return order_totals.mean()


def calculate_aov_growth(current_aov: float, previous_aov: float) -> float:
    """
    Calculate growth in average order value.

    Parameters
    ----------
    current_aov : float
        Current period AOV
    previous_aov : float
        Previous period AOV

    Returns
    -------
    float
        AOV growth rate as a decimal
    """
    if previous_aov == 0:
        return 0.0

    return (current_aov - previous_aov) / previous_aov


def calculate_total_orders(sales_data: pd.DataFrame) -> int:
    """
    Calculate total number of unique orders.

    Parameters
    ----------
    sales_data : DataFrame
        Sales dataset with order_id column

    Returns
    -------
    int
        Total number of orders
    """
    return sales_data['order_id'].nunique()


def calculate_order_growth(current_orders: int, previous_orders: int) -> float:
    """
    Calculate growth in number of orders.

    Parameters
    ----------
    current_orders : int
        Current period order count
    previous_orders : int
        Previous period order count

    Returns
    -------
    float
        Order growth rate as a decimal
    """
    if previous_orders == 0:
        return 0.0

    return (current_orders - previous_orders) / previous_orders


def get_monthly_revenue(sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Get monthly revenue data.

    Parameters
    ----------
    sales_data : DataFrame
        Sales dataset with year, month, and price columns

    Returns
    -------
    DataFrame
        Monthly revenue data with year, month, and price columns
    """
    monthly_revenue = sales_data.groupby(['year', 'month'])['price'].sum().reset_index()
    return monthly_revenue


def get_product_category_sales(
    sales_data: pd.DataFrame,
    products: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate sales by product category.

    Parameters
    ----------
    sales_data : DataFrame
        Sales dataset with product_id and price columns
    products : DataFrame
        Products dataset with product_id and product_category_name columns

    Returns
    -------
    DataFrame
        Sales by product category, sorted by revenue descending
    """
    # Merge sales with product categories
    sales_categories = pd.merge(
        left=products[['product_id', 'product_category_name']],
        right=sales_data[['product_id', 'price']],
        on='product_id'
    )

    # Group by category and sum revenue
    category_sales = (
        sales_categories
        .groupby('product_category_name')['price']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    return category_sales


def get_sales_by_state(
    sales_data: pd.DataFrame,
    orders: pd.DataFrame,
    customers: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate sales by customer state.

    Parameters
    ----------
    sales_data : DataFrame
        Sales dataset with order_id and price columns
    orders : DataFrame
        Orders dataset with order_id and customer_id columns
    customers : DataFrame
        Customers dataset with customer_id and customer_state columns

    Returns
    -------
    DataFrame
        Sales by state, sorted by revenue descending
    """
    # Merge sales with customers
    sales_customers = pd.merge(
        left=sales_data[['order_id', 'price']],
        right=orders[['order_id', 'customer_id']],
        on='order_id'
    )

    sales_states = pd.merge(
        left=sales_customers,
        right=customers[['customer_id', 'customer_state']],
        on='customer_id'
    )

    # Group by state and sum revenue
    state_sales = (
        sales_states
        .groupby('customer_state')['price']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    return state_sales


def calculate_average_delivery_time(sales_data: pd.DataFrame) -> float:
    """
    Calculate average delivery time in days.

    Parameters
    ----------
    sales_data : DataFrame
        Sales dataset with delivery_speed column

    Returns
    -------
    float
        Average delivery time in days
    """
    return sales_data['delivery_speed'].mean()


def calculate_average_review_score(
    sales_data: pd.DataFrame,
    reviews: pd.DataFrame
) -> float:
    """
    Calculate average review score.

    Parameters
    ----------
    sales_data : DataFrame
        Sales dataset with order_id column
    reviews : DataFrame
        Reviews dataset with order_id and review_score columns

    Returns
    -------
    float
        Average review score
    """
    # Merge sales with reviews
    sales_with_reviews = pd.merge(
        sales_data[['order_id']],
        reviews[['order_id', 'review_score']],
        on='order_id'
    )

    return sales_with_reviews['review_score'].mean()


def get_review_score_distribution(
    sales_data: pd.DataFrame,
    reviews: pd.DataFrame
) -> pd.Series:
    """
    Get distribution of review scores.

    Parameters
    ----------
    sales_data : DataFrame
        Sales dataset with order_id column
    reviews : DataFrame
        Reviews dataset with order_id and review_score columns

    Returns
    -------
    Series
        Normalized distribution of review scores
    """
    # Merge sales with reviews
    sales_with_reviews = pd.merge(
        sales_data[['order_id']],
        reviews[['order_id', 'review_score']],
        on='order_id'
    )

    # Get unique reviews per order
    unique_reviews = sales_with_reviews[['order_id', 'review_score']].drop_duplicates()

    return unique_reviews['review_score'].value_counts(normalize=True).sort_index()


def get_review_by_delivery_time(
    sales_data: pd.DataFrame,
    reviews: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate average review score by delivery time category.

    Parameters
    ----------
    sales_data : DataFrame
        Sales dataset with order_id and delivery_time columns
    reviews : DataFrame
        Reviews dataset with order_id and review_score columns

    Returns
    -------
    DataFrame
        Average review score by delivery time category
    """
    # Merge sales with reviews
    sales_with_reviews = pd.merge(
        sales_data[['order_id', 'delivery_time']],
        reviews[['order_id', 'review_score']],
        on='order_id'
    )

    # Get unique reviews per order
    unique_reviews = sales_with_reviews[['order_id', 'delivery_time', 'review_score']].drop_duplicates()

    # Group by delivery time
    review_by_delivery = (
        unique_reviews
        .groupby('delivery_time')['review_score']
        .mean()
        .reset_index()
    )

    return review_by_delivery


def get_order_status_distribution(
    orders: pd.DataFrame,
    year: Optional[int] = None
) -> pd.Series:
    """
    Get distribution of order statuses.

    Parameters
    ----------
    orders : DataFrame
        Orders dataset with order_status and order_purchase_timestamp columns
    year : int, optional
        Year to filter by

    Returns
    -------
    Series
        Normalized distribution of order statuses
    """
    df = orders.copy()

    # Add year column if filtering
    if year is not None:
        df['year'] = pd.to_datetime(df['order_purchase_timestamp']).dt.year
        df = df[df['year'] == year]

    return df['order_status'].value_counts(normalize=True)


def generate_revenue_summary(
    current_sales: pd.DataFrame,
    previous_sales: pd.DataFrame
) -> Dict[str, float]:
    """
    Generate a comprehensive revenue summary comparing two periods.

    Parameters
    ----------
    current_sales : DataFrame
        Sales data for current period
    previous_sales : DataFrame
        Sales data for previous period

    Returns
    -------
    dict
        Dictionary containing revenue metrics and comparisons
    """
    current_revenue = calculate_total_revenue(current_sales)
    previous_revenue = calculate_total_revenue(previous_sales)
    revenue_growth = calculate_revenue_growth(current_revenue, previous_revenue)

    current_aov = calculate_average_order_value(current_sales)
    previous_aov = calculate_average_order_value(previous_sales)
    aov_growth = calculate_aov_growth(current_aov, previous_aov)

    current_orders = calculate_total_orders(current_sales)
    previous_orders = calculate_total_orders(previous_sales)
    order_growth = calculate_order_growth(current_orders, previous_orders)

    monthly_growth = calculate_monthly_growth(current_sales)
    avg_monthly_growth = calculate_average_monthly_growth(monthly_growth)

    return {
        'current_revenue': current_revenue,
        'previous_revenue': previous_revenue,
        'revenue_growth': revenue_growth,
        'current_aov': current_aov,
        'previous_aov': previous_aov,
        'aov_growth': aov_growth,
        'current_orders': current_orders,
        'previous_orders': previous_orders,
        'order_growth': order_growth,
        'avg_monthly_growth': avg_monthly_growth
    }
