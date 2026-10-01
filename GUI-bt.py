import tkinter as tk
from tkinter import ttk
from strategies import STRATEGIES
from tkcalendar import DateEntry

TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NFLX", "SPY", "QQQ", "GLD", "XOM"]
STRAT = list(STRATEGIES)

root = tk.Tk()
root.title("Backtester")
root.geometry("900x400")

# gui grid
left = ttk.Frame(root, padding=10)
left.grid(row=0, column=0, sticky="ns")

# ticker selection
ttk.Label(left, text="Ticker:").grid(row=0, column=0, sticky="w", pady=4)
ticker_var = tk.StringVar(value=TICKERS[0])
ticker_box = ttk.Combobox(left, textvariable=ticker_var, values=TICKERS, width=12)
ticker_box.grid(row=0, column=1, pady=4)
# Start date
ttk.Label(left, text="Start:").grid(row=1, column=0, sticky="w", pady=4)
start_entry = DateEntry(left,width=12,date_pattern="yyyy-mm-dd",year=2015,month=1,day=1)
start_entry.grid(row=1,column=1,pady=4)

# End date
ttk.Label(left, text="End:").grid(row=2, column=0, sticky="w", pady=4)
end_entry = DateEntry(left, width=12, date_pattern="yyyy-mm-dd")
end_entry.grid(row=2,column=1,pady=4)

# Strat selection
ttk.Label(left, text="Strategy:").grid(row=3, column=0, sticky="w", pady=4)
strat_var = tk.StringVar(value=STRAT[0])
strat_box = ttk.Combobox(left, textvariable=strat_var,
                         values=STRAT, state="readonly",width=20) # state ensures fields are not editable
strat_box.grid(row=3, column=1, pady=4)


root.mainloop()
