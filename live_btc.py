import requests
import time

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data['bitcoin']['usd']
    else:
        print(f"Error: {response.status_code}")
        return None

def main():
    while True:
        btc_price = get_btc_price()
        
        if btc_price is not None:
            print(f"Bitcoin (BTC) Price: ${btc_price}")
        
        # Adjust the sleep duration based on how often you want to fetch the price
        time.sleep(60)  # Fetch the price every 60 seconds

if __name__ == "__main__":
    main()
