import os
import json
import random
import threading
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Data Files
STOCK_FILE = "tusec_stocks.json"
USER_FILE = "users.json"

# Default Stock Prices
STOCKS = {
    "TREDT Trading Company": 987.0,
    "Royal Trading Company": 712.0,
    "TREDT Industries": 219.0,
    "Union Technologies Inc.": 354.0,
    "TREDT Minerals Corp": 123.0,
    "Atlas Munitions Corp": 242.0,
    "New World Million & Co.": 156.0,
    "Swadeshi Printing & Publishing Co.": 231.0,
    "Continental Electrodynamics Inc.": 341.0,
    "Imperial Bank of TREDT": 134.0
}

# Load stock data
def load_stock_data():
    if os.path.exists(STOCK_FILE):
        with open(STOCK_FILE, "r") as f:
            return json.load(f)
    return STOCKS

# Save stock data
def save_stock_data(data):
    with open(STOCK_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Load user data
def load_user_data():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return []

# Save user data
def save_user_data(data):
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Load initial data
stock_data = load_stock_data()
users = load_user_data()
price_history = {company: [price] for company, price in stock_data.items()}

def update_stock_prices():
    global stock_data, price_history
    for company in stock_data:
        change = random.uniform(-5, 5)
        stock_data[company] = round(stock_data[company] * (1 + change / 100), 2)
        price_history[company].append(stock_data[company])
        if len(price_history[company]) > 50:
            price_history[company].pop(0)
    save_stock_data(stock_data)
    update_treeview()
    update_user_treeview()
    root.after(2000, update_stock_prices)

def update_treeview():
    for item in tree.get_children():
        tree.delete(item)
    for company, price in stock_data.items():
        tree.insert("", tk.END, values=(company, f"{price} TC"))

def plot_stock(company):
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='black')
    ax.set_facecolor("black")
    
    def update(frame):
        ax.clear()
        ax.set_facecolor("black")
        ax.plot(price_history[company], marker='o', linestyle='-', color='lime')
        ax.set_xlabel("Time", color='white')
        ax.set_ylabel("Stock Price (TREDT Credits)", color='white')
        ax.set_title(f"{company} Stock Price Over Time", color='white')
        ax.grid(True, color='gray')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
    
    ani = FuncAnimation(fig, update, interval=2000)
    plt.show()

def register_user():
    name = simpledialog.askstring("Register", "Enter Full Name:")
    position = simpledialog.askstring("Register", "Enter Position (PPM, APM, GM):")
    user_id = simpledialog.askstring("Register", "Enter Unique ID:")
    password = simpledialog.askstring("Register", "Enter Password:", show="*")

    if position not in ["PPM", "APM", "GM"]:
        messagebox.showerror("Error", "Invalid position!")
        return

    if not name or not position or not user_id or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    for user in users:
        if user["id"] == user_id:
            messagebox.showerror("Error", "User ID already exists!")
            return

    users.append({"name": name, "position": position, "id": user_id, "password": password, "portfolio": {}})
    save_user_data(users)
    update_user_treeview()
    messagebox.showinfo("Success", "User Registered Successfully!")

def buy_stock():
    user_id = simpledialog.askstring("Buy Stock", "Enter Your User ID:")
    for user in users:
        if user["id"] == user_id:
            company = simpledialog.askstring("Buy Stock", "Enter Company Name:")
            if company not in stock_data:
                messagebox.showerror("Error", "Company does not exist!")
                return
            qty = simpledialog.askinteger("Buy Stock", "Enter Quantity:")
            user["portfolio"][company] = user["portfolio"].get(company, 0) + qty
            save_user_data(users)
            messagebox.showinfo("Success", f"Purchased {qty} shares of {company}!")
            return
    messagebox.showerror("Error", "User ID not found!")

def update_user_treeview():
    for item in user_tree.get_children():
        user_tree.delete(item)
    for user in users:
        holdings = ", ".join([f"{k}: {v}" for k, v in user["portfolio"].items()]) or "No stocks owned"
        user_tree.insert("", tk.END, values=(user["name"], holdings))

root = tk.Tk()
root.title("TUSEC Stock Viewer")
root.geometry("1000x600")

top_frame = ttk.Frame(root)
top_frame.pack(fill=tk.BOTH, expand=True)

tree = ttk.Treeview(top_frame, columns=("Company", "Stock Price"), show="headings")
tree.heading("Company", text="Company")
tree.heading("Stock Price", text="Stock Price (TREDT Credits)")
tree.pack(fill=tk.BOTH, expand=True)

tree.bind("<Double-1>", lambda event: plot_stock(tree.item(tree.selection(), "values")[0]))

bottom_frame = ttk.Frame(root)
bottom_frame.pack(fill=tk.BOTH, expand=True)

user_tree = ttk.Treeview(bottom_frame, columns=("Name", "Portfolio"), show="headings")
user_tree.heading("Name", text="TUSEC Traders")
user_tree.heading("Portfolio", text="Portfolio")
user_tree.pack(fill=tk.BOTH, expand=True)

btn_register = ttk.Button(root, text="Register User", command=register_user)
btn_register.pack(side=tk.LEFT)

btn_buy = ttk.Button(root, text="Buy Stock", command=buy_stock)
btn_buy.pack(side=tk.LEFT)

update_treeview()
update_user_treeview()
update_stock_prices()
root.mainloop()