import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# News API key (replace with your own key)
NEWS_API_KEY = '7e82ca805a4a46cbacee1c77a36c9028'

# Function to get exchange rates
def get_exchange_rates(app_id, base_currency, target_currencies):
    url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}"

    try:
        # Make a GET request to the Open Exchange Rates API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)

        # Parse the JSON response
        data = response.json()

        # Get the exchange rates for the specified base currency
        rates = data.get('rates', {})
        base_currency_rate = rates.get(base_currency)

        return rates

    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return None

# Function to get historical exchange rates
def get_historical_exchange_rates(app_id, base_currency, target_currency, start_date, end_date):
    url = f"https://openexchangerates.org/api/time-series.json?app_id={app_id}"

    try:
        # Make a GET request to the Open Exchange Rates API
        response = requests.get(url, params={'base': base_currency, 'symbols': target_currency, 'start_date': start_date, 'end_date': end_date})
        response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)

        # Parse the JSON response
        data = response.json()

        # Get the historical exchange rates
        historical_rates = data.get('rates', {}).get(target_currency, {})

        return historical_rates

    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return None

# Streamlit app
def main():
    st.title("Mugare's Currency Exchange Rate")

    open_exchange_rates_app_id = '8a686f8a051342eca20744c1941b7b6c'
    base_currency = 'USD'

    # Fetch exchange rates
    rates = get_exchange_rates(open_exchange_rates_app_id, base_currency, [])

    if rates:
        # Filter options
        st.sidebar.header("Filters")

        # Date range selector
        start_date = st.sidebar.date_input("Start Date", min_value=datetime(2000, 1, 1))
        end_date = st.sidebar.date_input("End Date", max_value=datetime.now(), value=datetime.now())

        # Currencies selector
        selected_currencies = st.sidebar.multiselect("Select Currencies", list(rates.keys()), default=list(rates.keys()))

        # Filter data based on selections
        filtered_rates = {currency: rate for currency, rate in rates.items() if currency in selected_currencies}

        # Display exchange rates
        st.subheader("Exchange Rates")
        st.write(pd.DataFrame(list(filtered_rates.items()), columns=['Currency', 'Exchange Rate']))

        # Display bar chart
        st.subheader(f'Exchange Rates for {base_currency}')
        df_bar = pd.DataFrame({'Currency': list(filtered_rates.keys()), 'Exchange Rate': list(filtered_rates.values())})
        st.bar_chart(df_bar.set_index('Currency'))

        # Display line chart
        st.subheader(f'Exchange Rates Over Time ({base_currency} to {", ".join(selected_currencies)})')
        df_line = pd.DataFrame({'Currency': list(filtered_rates.keys()), 'Exchange Rate': list(filtered_rates.values())})
        st.line_chart(df_line.set_index('Currency'))

       
        # Currency Converter
        st.sidebar.header("Currency Converter")
        amount = st.sidebar.number_input("Enter Amount", value=1.0, step=0.01)
        from_currency = st.sidebar.selectbox("From Currency", list(rates.keys()), index=selected_currencies.index(base_currency))
        to_currency = st.sidebar.selectbox("To Currency", list(rates.keys()), index=0)
        converted_amount = amount * (rates[to_currency] / rates[from_currency])
        st.sidebar.text(f"Converted Amount: {converted_amount:.2f} {to_currency}")

        # User Authentication
        st.sidebar.header("User Authentication")
        username = st.sidebar.text_input("Username", "Joemugare", key="username_key")
        password = st.sidebar.text_input("Password", "", type="password")
        login_button = st.sidebar.button("Login")

        if login_button:
        # Simple authentication (replace with a more secure method in a real application)
          if username == "Joemugare" and password == "Qunta729":
            st.sidebar.success("Login successful! Welcome, user.")
          else:
            st.sidebar.error("Login failed. Please check your credentials.")


        # Additional chart: Horizontal Bar Chart
        st.subheader("Horizontal Bar Chart of Exchange Rates")
        df_horizontal_bar = pd.DataFrame({'Currency': list(filtered_rates.keys()), 'Exchange Rate': list(filtered_rates.values())})
        st.bar_chart(df_horizontal_bar.set_index('Currency'), use_container_width=True)

if __name__ == '__main__':
    main()
