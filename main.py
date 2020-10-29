import pandas_datareader as pdr
import yfinance as yf
import tkinter as tk
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt



yf.pdr_override() # <== that's all it takes :-)

# download dataframe
data = pdr.get_data_yahoo("AAPL", start="2020-01-01", end="2020-10-29").to_csv("info.csv")



print(data)
root = tk.Tk()

root.geometry("1000x500")
root.pack_propagate(0)
root.resizable(0, 0)
# This is the frame for the Treeview
frame1 = tk.LabelFrame(root, text="AAPL data")
frame1.place(height=350, width=750)


f= open("info.csv")
aktsiaInfo = []
for line in f:
    info = line.strip().split(",")
    aktsiaInfo.append(info)

print(aktsiaInfo)

päevad = []
hinnad = []

aktsiaInfo.pop(0)

for p in aktsiaInfo:
    päevad.append(p[0])
    hinnad.append(round(float(p[4]),5))

print(päevad)
print(hinnad)

data1 = {"Päevad": päevad,
         "Hinnad": hinnad}

df1 = DataFrame(data1,columns=["Päevad","Hinnad"])

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(päevad,hinnad,color ="r")
graafik = FigureCanvasTkAgg(fig, root)
graafik.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)


root.mainloop()