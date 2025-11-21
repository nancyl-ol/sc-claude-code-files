# FRED API Setup Guide

This application fetches real-time economic data from the Federal Reserve Economic Data (FRED) API.

## Getting Your FRED API Key

1. Visit the FRED API Key Request Page: https://fred.stlouisfed.org/docs/api/api_key.html

2. Click "Request API Key"

3. Sign in or create a free account with your email

4. Fill out the API key request form:
   - Provide your name and email
   - Describe your intended use (e.g., "Educational dashboard for economic indicators")

5. Submit the form and you'll receive your API key immediately

## Configuring Your Application

1. Open the `.env.local` file in the `fred-data` directory

2. Replace `your_fred_api_key_here` with your actual API key:
   ```
   NEXT_PUBLIC_FRED_API_KEY=your_actual_api_key_here
   ```

3. Save the file

4. The dev server will automatically reload and start fetching real data

## Data Series Used

The dashboard displays the following FRED data series:

- **CPI Growth Rate**: CPALTT01USM657N (Consumer Price Index for All Urban Consumers)
- **Unemployment Rate**: UNRATE (Unemployment Rate)
- **10-Year Treasury**: GS10 (10-Year Treasury Constant Maturity Rate)
- **3-Month Treasury**: TB3MS (3-Month Treasury Bill Secondary Market Rate)

All data is fetched for the last 5 years and updated in real-time.

## Troubleshooting

If you see "Loading economic data..." indefinitely:
- Check that your API key is correctly set in `.env.local`
- Verify the API key is valid at https://fred.stlouisfed.org/
- Check the browser console for any API errors
