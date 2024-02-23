class ProfitabilityCalculator:
    def __init__(self, hash_rate_entry, power_consumption_entry, electricity_cost_entry,
                 current_btc_price_entry, result_label):
        self.hash_rate_entry = hash_rate_entry
        self.power_consumption_entry = power_consumption_entry
        self.electricity_cost_entry = electricity_cost_entry
        self.current_btc_price_entry = current_btc_price_entry
        self.result_label = result_label

    def calculate_profitability(self):
        try:
            hash_rate = float(self.hash_rate_entry.get())
            power_consumption = float(self.power_consumption_entry.get())
            electricity_cost = float(self.electricity_cost_entry.get())
            current_btc_price = float(self.current_btc_price_entry.get())

            daily_earnings = (hash_rate * 86400 / 10**12) * (current_btc_price - electricity_cost)
            weekly_earnings = daily_earnings * 7
            monthly_earnings = daily_earnings * 30

            self.result_label.config(text=f"Profitability:\n"
                                           f"Daily Earnings: ${daily_earnings:.2f}\n"
                                           f"Weekly Earnings: ${weekly_earnings:.2f}\n"
                                           f"Monthly Earnings: ${monthly_earnings:.2f}")
        except ValueError:
            self.result_label.config(text="Invalid input. Please enter valid numeric values.")