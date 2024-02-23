import requests

class BTCCalculator:
    def __init__(self, current_btc_price_entry, amount_entry, target_btc_price_entry, result_label):
        self.current_btc_price_entry = current_btc_price_entry
        self.amount_entry = amount_entry
        self.target_btc_price_entry = target_btc_price_entry
        self.result_label = result_label

    def get_live_btc_price(self):
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data['bitcoin']['usd']
            else:
                print(f"Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching live BTC price: {e}")
            return None

    def calculate_btc_value(self):
        current_btc_price = float(self.get_live_btc_price())
        amount_in_dollars = float(self.amount_entry.get())
        target_btc_price = float(self.target_btc_price_entry.get())

        btc_amount = amount_in_dollars / current_btc_price
        target_value = btc_amount * target_btc_price

        result_text = f"BTC Amount: {btc_amount:.8f} BTC\nTarget Value: ${target_value:.2f}"
        self.result_label.config(text=result_text)