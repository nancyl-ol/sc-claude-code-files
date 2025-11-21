# E-Commerce Sales Analysis - Refactored

A professional, maintainable business intelligence framework for e-commerce sales data with configurable time periods and reusable business metrics calculations.

## Overview

This project transforms a basic exploratory data analysis into a professional, well-documented analytical framework. The refactored solution provides:

- **Interactive Dashboard**: Professional Streamlit dashboard with real-time filtering and visualizations
- **Configurable Analysis**: Easily analyze any time period or compare different years
- **Modular Architecture**: Reusable data loading and metrics calculation modules
- **Professional Visualizations**: Business-oriented charts with proper formatting and labels
- **Comprehensive Documentation**: Clear structure with table of contents and data dictionary
- **Clean Code**: Well-documented functions with docstrings and consistent naming

## Project Structure

```
lesson7_files/
├── dashboard.py             # Streamlit dashboard application
├── EDA_Refactored.ipynb     # Main refactored analysis notebook
├── EDA.ipynb                # Original analysis notebook (for reference)
├── data_loader.py           # Data loading and processing module
├── business_metrics.py      # Business metrics calculation module
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── ecommerce_data/         # Data directory
    ├── orders_dataset.csv
    ├── order_items_dataset.csv
    ├── products_dataset.csv
    ├── customers_dataset.csv
    ├── order_reviews_dataset.csv
    └── order_payments_dataset.csv
```

## Features

### 1. Interactive Streamlit Dashboard
- **Real-time Filtering**: Date range selector for dynamic data exploration
- **KPI Cards**: Total Revenue, Monthly Growth, Average Order Value, and Total Orders with trend indicators
- **Professional Charts**:
  - Revenue trend line chart comparing current vs previous period
  - Top 10 product categories bar chart with blue gradient
  - US choropleth map showing revenue by state
  - Delivery time vs satisfaction score chart
- **Performance Metrics**: Average delivery time and review score cards with stars
- **Responsive Layout**: Professional 2x2 grid layout with uniform card heights

### 2. Configurable Analysis Framework
- Set analysis year, comparison year, and month filters
- Flexible time period analysis without code changes
- Automatic handling of missing data periods

### 3. Comprehensive Business Metrics
- **Revenue Analysis**: Total revenue, growth rates, average order value
- **Product Performance**: Category analysis, revenue share, top performers
- **Geographic Insights**: State-level revenue and order analysis
- **Customer Satisfaction**: Review scores, satisfaction distribution
- **Delivery Performance**: Delivery times, speed categorization

### 4. Professional Visualizations
- Monthly revenue trend charts
- Product category performance bars
- Interactive geographic heatmaps
- Customer satisfaction distributions
- Consistent color schemes and formatting

### 5. Automated Summary
- Executive summary with key findings
- Performance benchmarking across time periods
- Automated insights generation

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Jupyter Notebook or JupyterLab

### Installation Steps

1. **Clone or download the project files**

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure data files are in place**:
   - Place CSV files in the `ecommerce_data/` directory
   - Verify all required files are present (see Project Structure above)

4. **Launch the application**:

   **Option A: Streamlit Dashboard (Recommended)**
   ```bash
   streamlit run dashboard.py
   ```
   The dashboard will open in your default browser at `http://localhost:8501`

   **Option B: Jupyter Notebook**
   ```bash
   jupyter notebook EDA_Refactored.ipynb
   ```

## Usage Guide

### Running the Streamlit Dashboard

1. **Start the dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

2. **Use the date range filter**:
   - Click on the date range selector in the top-right corner
   - Select start and end dates to filter the data
   - The dashboard will automatically update all visualizations

3. **Explore the visualizations**:
   - **KPI Cards**: View key metrics with trend indicators (green for positive, red for negative)
   - **Revenue Trend**: Compare current period (solid line) vs previous period (dashed line)
   - **Top Categories**: See the top 10 product categories by revenue
   - **State Map**: Hover over states to see revenue by location
   - **Delivery Analysis**: Understand how delivery time affects customer satisfaction
   - **Performance Cards**: Check average delivery time and review scores

4. **Interpret the metrics**:
   - All currency values are formatted (e.g., $300K, $2M)
   - Trend indicators show percentage change vs previous period
   - Review scores are displayed with star ratings

### Running the Analysis Notebook

1. **Open the refactored notebook**: `EDA_Refactored.ipynb`

2. **Configure analysis parameters** in the Configuration section (Section 3):
   ```python
   ANALYSIS_YEAR = 2023        # Year to analyze
   COMPARISON_YEAR = 2022      # Year to compare against
   ANALYSIS_MONTH = None       # Set to specific month (1-12) or None for full year
   DATA_DIR = 'ecommerce_data' # Directory containing CSV files
   ```

3. **Run all cells** to generate the complete analysis:
   - Click "Cell" > "Run All" in the menu, or
   - Use the keyboard shortcut: Shift+Enter to run cells sequentially

4. **Navigate the notebook**:
   - Use the Table of Contents to jump to specific sections
   - Review the Data Dictionary to understand column definitions
   - Examine visualizations and metrics in each analysis section
   - Read the Executive Summary for key findings

### Advanced Configuration

#### Analyzing Specific Time Periods
```python
# Analyze only Q4 2023
ANALYSIS_YEAR = 2023
ANALYSIS_MONTH = 10  # October, or 11 for November, 12 for December
```

#### Custom Data Paths
```python
# Use different data location
DATA_DIR = '/path/to/your/data/'
```

### Module Usage

The refactored code uses a function-based approach for maximum flexibility and reusability.

#### Data Loading Module

```python
import data_loader

# Load raw datasets
orders, order_items, products, customers, reviews = data_loader.load_raw_data('ecommerce_data')

# Prepare sales data with full pipeline
sales_data = data_loader.prepare_sales_data(
    data_dir='ecommerce_data',
    year=2023,
    month=None,  # None for full year, or 1-12 for specific month
    include_delivery_metrics=True
)

# Advanced: Use individual functions for custom workflows
sales = data_loader.create_sales_dataset(orders, order_items)
sales_delivered = data_loader.filter_delivered_orders(sales)
sales_with_dates = data_loader.add_temporal_columns(sales_delivered)
sales_filtered = data_loader.filter_by_date_range(sales_with_dates, year=2023)
```

#### Business Metrics Module

```python
import business_metrics

# Revenue metrics
total_revenue = business_metrics.calculate_total_revenue(sales_data)
revenue_growth = business_metrics.calculate_revenue_growth(current_revenue, previous_revenue)
avg_order_value = business_metrics.calculate_average_order_value(sales_data)

# Product analysis
category_sales = business_metrics.get_product_category_sales(sales_data, products)

# Geographic analysis
state_sales = business_metrics.get_sales_by_state(sales_data, orders, customers)

# Customer experience metrics
avg_delivery = business_metrics.calculate_average_delivery_time(sales_data)
avg_review = business_metrics.calculate_average_review_score(sales_data, reviews)

# Comprehensive summary
summary = business_metrics.generate_revenue_summary(current_sales, previous_sales)
```

## Key Business Metrics

### Revenue Metrics
- **Total Revenue**: Sum of all delivered order item prices
- **Revenue Growth Rate**: Year-over-year percentage change
- **Average Order Value (AOV)**: Average total value per order
- **Monthly Growth Trends**: Month-over-month performance

### Product Performance
- **Category Revenue**: Revenue by product category
- **Market Share**: Percentage of total revenue by category
- **Category Diversity**: Distribution across product lines

### Geographic Analysis
- **State Performance**: Revenue and order count by state
- **Market Penetration**: Number of active markets
- **Regional AOV**: Average order value by geographic region

### Customer Experience
- **Review Scores**: Average satisfaction rating (1-5 scale)
- **Satisfaction Distribution**: Percentage of high/low ratings
- **Delivery Performance**: Average delivery time and speed metrics

## Output Examples

### Console Output
```
BUSINESS METRICS SUMMARY - 2023
============================================================

REVENUE PERFORMANCE:
  Total Revenue: $3,360,294.74
  Total Orders: 4,635
  Average Order Value: $724.98
  Revenue Growth: -2.5%

CUSTOMER SATISFACTION:
  Average Review Score: 4.10/5.0
  High Satisfaction (4+): 84.2%

DELIVERY PERFORMANCE:
  Average Delivery Time: 8.0 days
  Fast Delivery (≤3 days): 28.5%
```

### Generated Visualizations
- Monthly revenue trend line charts
- Top product category horizontal bar charts
- Interactive US state choropleth maps
- Customer satisfaction distribution charts

## Customization Options

### Adding New Metrics
1. Add new functions to `business_metrics.py` with proper docstrings
2. Follow the existing naming convention (e.g., `calculate_*` for metrics, `get_*` for aggregations)
3. Update the notebook to call and display new metrics

Example:
```python
def calculate_customer_lifetime_value(sales_data: pd.DataFrame) -> float:
    """
    Calculate average customer lifetime value.

    Parameters
    ----------
    sales_data : DataFrame
        Sales dataset with customer_id and price columns

    Returns
    -------
    float
        Average customer lifetime value
    """
    customer_revenue = sales_data.groupby('customer_id')['price'].sum()
    return customer_revenue.mean()
```

### Custom Visualizations
Add visualization cells to the notebook following the existing pattern:
```python
# Example: Custom visualization
plt.figure(figsize=(12, 6))
# Your visualization code
plt.title('Your Chart Title', fontsize=14, fontweight='bold')
plt.xlabel('X Label', fontsize=12)
plt.ylabel('Y Label', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### Data Source Modifications
- Modify `data_loader.py` functions to handle different CSV structures
- Update column mappings in the individual functions
- Add new data validation and cleaning functions

## Troubleshooting

### Common Issues

1. **Module Import Errors**:
   - Ensure all files are in the same directory
   - Check Python path configuration

2. **Missing Data Files**:
   - Verify CSV files are in the `ecommerce_data/` directory
   - Check file naming matches expected patterns

3. **Empty Results**:
   - Verify date filters match available data
   - Check order status filtering

4. **Visualization Issues**:
   - Ensure all required packages are installed
   - Check Plotly version compatibility for interactive maps

### Performance Optimization
- For large datasets, consider chunked processing in `data_loader.py`
- Use data sampling for initial exploration
- Cache processed datasets for repeated analysis

## Future Enhancements

### Potential Extensions
- ✅ Interactive Streamlit dashboard (completed!)
- Predictive analytics and forecasting
- Customer segmentation analysis
- Time series analysis with trend decomposition
- Cohort analysis
- Export functionality (PDF reports, PowerPoint presentations)
- Dashboard features:
  - Export charts as images
  - Download filtered data as CSV
  - Email report scheduling
  - Custom metric definitions

### Advanced Analytics Ideas
- Machine learning model integration for predictions
- Advanced statistical analysis and hypothesis testing
- Anomaly detection for unusual sales patterns
- Recommendation engine for product cross-selling

## Contributing

To extend this analysis framework:

1. Follow the existing code structure and documentation patterns
2. Add comprehensive docstrings to new functions
3. Include unit tests for new business logic
4. Update this README with new features

## License

This project is provided as-is for educational and business analysis purposes.

---

**Note**: This framework is designed to be easily maintained and extended for ongoing business intelligence needs. The modular architecture ensures that updates to data sources or metric calculations can be made without affecting the overall analysis structure.