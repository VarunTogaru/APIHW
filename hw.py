import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def fetch_stock_info(symbol):
    url = "https://yfapi.net/v6/finance/quote"
    headers = {
        'x-api-key': "VbrpKoUQuW2YBqqAf6flm5uHhieyx27F3vTLIfi3"
    }
    querystring = {"symbols": symbol}

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def fetch_trending_stocks():
    url = "https://yfapi.net/v1/finance/trending/US"
    headers = {
        'x-api-key': "VbrpKoUQuW2YBqqAf6flm5uHhieyx27F3vTLIfi3"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching trending stocks: {response.status_code}")
        return None

def fetch_historical_data(symbol):
    url = f"https://yfapi.net/v8/finance/chart/{symbol}"
    headers = {
        'x-api-key': "VbrpKoUQuW2YBqqAf6flm5uHhieyx27F3vTLIfi3"
    }
    querystring = {
        "range": "5d",
        "interval": "1d"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def main():
    # User input for stock symbol
    user_symbol = input("Enter a stock symbol (e.g., AAPL): ").upper()

    # Fetch stock information
    stock_data = fetch_stock_info(user_symbol)

    if stock_data and 'quoteResponse' in stock_data and 'result' in stock_data['quoteResponse']:
        result = stock_data['quoteResponse']['result'][0]
        
        # Display stock information
        print(f"\nStock Information for {user_symbol}:")
        print(f"Full Name: {result.get('longName', 'N/A')}")
        print(f"Current Market Price: ${result.get('regularMarketPrice', 'N/A')}")
        
        target_price = result.get('targetMedianPrice')
        print(f"Average Target Price: {'Info not available' if target_price is None else f'${target_price:.2f}'}")
        
        fifty_two_week_high = result.get('fiftyTwoWeekHigh', 'N/A')
        print(f"52 Week High: ${fifty_two_week_high if isinstance(fifty_two_week_high, (int, float)) else 'N/A'}")
        
        fifty_two_week_low = result.get('fiftyTwoWeekLow', 'N/A')
        print(f"52 Week Low: ${fifty_two_week_low if isinstance(fifty_two_week_low, (int, float)) else 'N/A'}")

        # Fetch trending stocks
        trending_data = fetch_trending_stocks()
        trending_symbols = []
        if trending_data and 'finance' in trending_data and 'result' in trending_data['finance']:
            trending_quotes = trending_data['finance']['result'][0].get('quotes', [])
            print("\nTop 5 Trending Stocks:")
            for quote in trending_quotes[:5]:
                symbol = quote.get('symbol', 'N/A')
                print(f"- {symbol}")
                trending_symbols.append(symbol)
        else:
            print("Unable to fetch trending stocks data.")

        # Ensure we have 5 trending stock symbols, even if some are N/A
        trending_symbols.extend(['N/A'] * (5 - len(trending_symbols)))

        # Store data in DataFrame and save to CSV
        df = pd.DataFrame({
            'Ticker': [user_symbol],
            'Full Name': [result.get('longName', 'N/A')],
            'Current Market Price': [result.get('regularMarketPrice', 'N/A')],
            'Average Target Price': [target_price if target_price is not None else 'Info not available'],
            '52 Week High': [fifty_two_week_high],
            '52 Week Low': [fifty_two_week_low],
            'Trending Stock 1': [trending_symbols[0]],
            'Trending Stock 2': [trending_symbols[1]],
            'Trending Stock 3': [trending_symbols[2]],
            'Trending Stock 4': [trending_symbols[3]],
            'Trending Stock 5': [trending_symbols[4]]
        })

        df.to_csv(f"{user_symbol}_data.csv", index=False)
        print(f"\nData saved to {user_symbol}_data.csv")

        # Bonus: Plot historical data
        historical_data = fetch_historical_data(user_symbol)
        if historical_data and 'chart' in historical_data and 'result' in historical_data['chart']:
            timestamps = historical_data['chart']['result'][0]['timestamp']
            prices = historical_data['chart']['result'][0]['indicators']['quote'][0]['high']
            
            dates = [datetime.fromtimestamp(ts) for ts in timestamps]
            
            plt.figure(figsize=(10, 6))
            plt.plot(dates, prices)
            plt.title(f"{user_symbol} Stock Price (High) - Last 5 Days")
            plt.xlabel("Date")
            plt.ylabel("Price (USD)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"{user_symbol}_historical_chart.png")
            print(f"\nHistorical chart saved as {user_symbol}_historical_chart.png")
        else:
            print("Unable to fetch historical data for charting.")

    else:
        print(f"Error: Unable to fetch data for {user_symbol}")

if __name__ == "__main__":
    main()