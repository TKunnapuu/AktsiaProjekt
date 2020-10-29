import pandas_datareader as pdr
import yfinance as yf
import tkinter as tk

yf.pdr_override() # <== that's all it takes :-)

# download dataframe
data = pdr.get_data_yahoo("SPY", start="2020-01-01", end="2020-04-30")



print(data)
root = tk.Tk()

root.geometry("500x500")
root.pack_propagate(0)
root.resizable(0, 0)
# This is the frame for the Treeview
frame1 = tk.LabelFrame(root, text="SPY data")
frame1.place(height=250, width=500)


root.mainloop()