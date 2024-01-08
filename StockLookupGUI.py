import tkinter as tk
from tkinter import messagebox
import requests
import yfinance as yf

class StockLookupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Lookup")

        # Create GUI elements
        self.label = tk.Label(root, text="Enter Stock Symbol or Company Name:")
        self.label.pack(pady=10)

        self.stock_entry = tk.Entry(root, width=40)
        self.stock_entry.pack(pady=10)

        self.search_button = tk.Button(root, text="Search", command=self.search_stock)
        self.search_button.pack(pady=10)

        # Display area for stock information
        self.result_text = tk.Text(root, height=10, width=60)
        self.result_text.config(state="disabled", bg="#dddddd")
        self.result_text.pack(pady=10)

        # Add a "Refresh" button
        self.refresh_button = tk.Button(root, text="Refresh", command=self.refresh)
        self.refresh_button.pack(pady=10)

    def search_stock(self):
        # Get user input
        stock_query = self.stock_entry.get().strip()

        if not stock_query:
            messagebox.showerror("Error", "Please enter a stock symbol or company name.")
            return

        try:
            # Lookup stock information
            stock_info = yf.Ticker(stock_query)
            info_str = f"Symbol: {stock_info.info['symbol']}\n" \
                       f"Name: {stock_info.info['longName']}\n" \
                       f"Open: {stock_info.info['open']}\n" \
                       f"Close: {stock_info.info['previousClose']}\n\n"

            # Fetch recent news headlines
            news_df = stock_info.news
            if not news_df.empty:
                info_str += "Recent News Headlines:\n"
                for index, row in news_df.head(3).iterrows():
                    info_str += f"{row['date']}: {row['title']}\n"
            else:
                info_str += "No recent news available."

            # Display the information
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", info_str)
            self.result_text.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching stock information: {e}")

    def refresh(self):
        # Clear the current results
        self.stock_entry.delete(0, "end")
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = StockLookupApp(root)
    root.mainloop()