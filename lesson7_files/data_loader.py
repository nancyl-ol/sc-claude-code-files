"""
Data Loading and Processing Module

This module handles loading and processing e-commerce data from CSV files.
It includes functions for data cleaning, transformation, and filtering.
"""

import pandas as pd
from typing import Optional, Tuple


def load_raw_data(data_dir: str = 'ecommerce_data') -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load all raw e-commerce datasets from CSV files.

    Parameters
    ----------
    data_dir : str, default='ecommerce_data'
        Directory path containing the CSV files

    Returns
    -------
    tuple of DataFrames
        (orders, order_items, products, customers, reviews)
    """
    orders = pd.read_csv(f'{data_dir}/orders_dataset.csv')
    order_items = pd.read_csv(f'{data_dir}/order_items_dataset.csv')
    products = pd.read_csv(f'{data_dir}/products_dataset.csv')
    customers = pd.read_csv(f'{data_dir}/customers_dataset.csv')
    reviews = pd.read_csv(f'{data_dir}/order_reviews_dataset.csv')

    return orders, order_items, products, customers, reviews


def create_sales_dataset(orders: pd.DataFrame, order_items: pd.DataFrame) -> pd.DataFrame:
    """
    Create a combined sales dataset by merging orders and order items.

    Parameters
    ----------
    orders : DataFrame
        Orders dataset containing order information
    order_items : DataFrame
        Order items dataset containing product and pricing information

    Returns
    -------
    DataFrame
        Merged sales dataset with order and item details
    """
    sales_data = pd.merge(
        left=order_items[['order_id', 'order_item_id', 'product_id', 'price']],
        right=orders[['order_id', 'order_status', 'order_purchase_timestamp', 'order_delivered_customer_date']],
        on='order_id'
    )

    return sales_data


def filter_delivered_orders(sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Filter sales data to include only delivered orders.

    Parameters
    ----------
    sales_data : DataFrame
        Combined sales dataset

    Returns
    -------
    DataFrame
        Sales data filtered to delivered orders only
    """
    sales_delivered = sales_data[sales_data['order_status'] == 'delivered'].copy()

    return sales_delivered


def add_temporal_columns(sales_delivered: pd.DataFrame) -> pd.DataFrame:
    """
    Add temporal columns (month, year) to the sales dataset.

    Parameters
    ----------
    sales_delivered : DataFrame
        Sales data with delivered orders

    Returns
    -------
    DataFrame
        Sales data with added temporal columns
    """
    df = sales_delivered.copy()

    # Convert timestamp to datetime
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

    # Extract month and year
    df['month'] = df['order_purchase_timestamp'].dt.month
    df['year'] = df['order_purchase_timestamp'].dt.year

    return df


def filter_by_date_range(
    sales_data: pd.DataFrame,
    year: Optional[int] = None,
    month: Optional[int] = None
) -> pd.DataFrame:
    """
    Filter sales data by year and optionally by month.

    Parameters
    ----------
    sales_data : DataFrame
        Sales dataset with temporal columns
    year : int, optional
        Year to filter by
    month : int, optional
        Month to filter by (1-12). Only used if year is also specified.

    Returns
    -------
    DataFrame
        Filtered sales data
    """
    df = sales_data.copy()

    if year is not None:
        df = df[df['year'] == year]

    if month is not None and year is not None:
        df = df[df['month'] == month]

    return df


def add_delivery_metrics(sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Add delivery-related metrics to the sales dataset.

    Parameters
    ----------
    sales_data : DataFrame
        Sales dataset with order timestamps

    Returns
    -------
    DataFrame
        Sales data with delivery metrics added
    """
    df = sales_data.copy()

    # Ensure datetime columns
    df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

    # Calculate delivery speed in days
    df['delivery_speed'] = (
        df['order_delivered_customer_date'] - df['order_purchase_timestamp']
    ).dt.days

    return df


def categorize_delivery_speed(days: int) -> str:
    """
    Categorize delivery speed into time ranges.

    Parameters
    ----------
    days : int
        Number of days for delivery

    Returns
    -------
    str
        Delivery time category
    """
    if days <= 3:
        return '1-3 days'
    elif days <= 7:
        return '4-7 days'
    else:
        return '8+ days'


def add_delivery_categories(sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Add categorized delivery time column to the dataset.

    Parameters
    ----------
    sales_data : DataFrame
        Sales dataset with delivery_speed column

    Returns
    -------
    DataFrame
        Sales data with delivery_time category added
    """
    df = sales_data.copy()
    df['delivery_time'] = df['delivery_speed'].apply(categorize_delivery_speed)

    return df


def prepare_sales_data(
    data_dir: str = 'ecommerce_data',
    year: Optional[int] = None,
    month: Optional[int] = None,
    include_delivery_metrics: bool = True
) -> pd.DataFrame:
    """
    Complete pipeline to load, process, and prepare sales data.

    This is the main function to use for data preparation. It loads raw data,
    filters for delivered orders, adds temporal columns, filters by date range,
    and optionally adds delivery metrics.

    Parameters
    ----------
    data_dir : str, default='ecommerce_data'
        Directory containing CSV files
    year : int, optional
        Year to filter data by
    month : int, optional
        Month to filter data by (requires year)
    include_delivery_metrics : bool, default=True
        Whether to include delivery speed metrics

    Returns
    -------
    DataFrame
        Processed sales dataset ready for analysis
    """
    # Load raw data
    orders, order_items, _, _, _ = load_raw_data(data_dir)

    # Create sales dataset
    sales_data = create_sales_dataset(orders, order_items)

    # Filter to delivered orders
    sales_delivered = filter_delivered_orders(sales_data)

    # Add temporal columns
    sales_delivered = add_temporal_columns(sales_delivered)

    # Filter by date range if specified
    if year is not None:
        sales_delivered = filter_by_date_range(sales_delivered, year, month)

    # Add delivery metrics if requested
    if include_delivery_metrics:
        sales_delivered = add_delivery_metrics(sales_delivered)
        sales_delivered = add_delivery_categories(sales_delivered)

    return sales_delivered
