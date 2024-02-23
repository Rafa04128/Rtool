import tkinter as tk
from tkinter import ttk
from btc_Cal import BTCCalculator
from profit_Cal import ProfitabilityCalculator
from password_manager import PasswordManager
from PIL import Image, ImageTk

def create_app_one(notebook):
    # Create a frame for App One
    frame_one = ttk.Frame(notebook)

    # Create instances of the calculators
    btc_calculator = BTCCalculator(tk.Entry(frame_one), tk.Entry(frame_one), tk.Entry(frame_one), tk.Label(frame_one))
    profitability_calculator = ProfitabilityCalculator(tk.Entry(frame_one), tk.Entry(frame_one), tk.Entry(frame_one),
                                                       tk.Entry(frame_one), tk.Label(frame_one))
    
    initial_live_btc_price = btc_calculator.get_live_btc_price()
    if initial_live_btc_price is not None:
        btc_calculator.current_btc_price_entry.insert(0, initial_live_btc_price)
    # Labels and entry widgets for App One (BTC Value Calculation)
    labels_entries_app_one = [
        (tk.Label(frame_one, text="Current BTC Price ($):"), btc_calculator.current_btc_price_entry),
        (tk.Label(frame_one, text="Amount in Dollars:"), btc_calculator.amount_entry),
        (tk.Label(frame_one, text="Target BTC Price ($):"), btc_calculator.target_btc_price_entry),
    ]

    # Arrange widgets for App One
    for i, (label, entry) in enumerate(labels_entries_app_one):
        label.grid(row=i, column=0, padx=10, pady=10)
        entry.grid(row=i, column=1, padx=10, pady=10)

    tk.Button(frame_one, text="Calculate BTC Value", command=btc_calculator.calculate_btc_value).grid(row=i + 1, column=0, columnspan=2, pady=20)
    btc_calculator.result_label.grid(row=i + 2, column=0, columnspan=2, padx=10, pady=10)

    # Labels and entry widgets for Profitability Calculation
    labels_entries_profitability = [
        (tk.Label(frame_one, text="Hash Rate (TH/s):"), profitability_calculator.hash_rate_entry),
        (tk.Label(frame_one, text="Power Consumption (W):"), profitability_calculator.power_consumption_entry),
        (tk.Label(frame_one, text="Electricity Cost ($/kWh):"), profitability_calculator.electricity_cost_entry),
        (tk.Label(frame_one, text="Current BTC Price ($):"), profitability_calculator.current_btc_price_entry),
    ]

    # Arrange widgets for Profitability Calculation
    for i, (label, entry) in enumerate(labels_entries_profitability, start=i + 3):
        label.grid(row=i, column=0, padx=10, pady=10)
        entry.grid(row=i, column=1, padx=10, pady=10)

    tk.Button(frame_one, text="Calculate Profitability", command=profitability_calculator.calculate_profitability).grid(row=i + 1, column=0, columnspan=2, pady=20)
    profitability_calculator.result_label.grid(row=i + 2, column=0, columnspan=2, padx=10, pady=10)

    # Add the frame to the notebook
    notebook.add(frame_one, text="Mining")


def create_app_two(notebook):
    # Create a frame for App Two (Password Manager)
    frame_two = ttk.Frame(notebook)

    # Create an instance of the Password Manager
    password_manager = PasswordManager(frame_two, root)

    # Labels and entry widgets for Password Manager
    labels_entries_password_manager = [
        (tk.Label(frame_two, text=""), password_manager.service_entry),
        (tk.Label(frame_two, text=""), password_manager.username_entry),
        (tk.Label(frame_two, text=""), password_manager.password_entry),
    ]

    # Arrange widgets for Password Manager
    for i, (label, entry) in enumerate(labels_entries_password_manager, start=1):
        label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")

    

    # Add the frame to the notebook
    notebook.add(frame_two, text="Password Manager")

def create_app_three():
    return None

# Create the main window
root = tk.Tk()
root.title("Tool")
icon_path = r"C:\Users\LINES\Desktop\project\rtool\favicon.png"
icon_image = Image.open(icon_path)
tk_image = ImageTk.PhotoImage(icon_image)

root.iconphoto(True, tk_image)
# Create a notebook (tabbed interface) to switch between apps
notebook = ttk.Notebook(root)

# Add tabs for each app
create_app_one(notebook)
create_app_two(notebook)
#create_app_three(notebook)

# Arrange widgets using the grid layout
notebook.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

# Configure column weights for resizing
root.grid_columnconfigure(0, weight=1)

# Run the Tkinter event loop
root.mainloop()