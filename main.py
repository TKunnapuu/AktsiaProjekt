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
raam = tk.Tk()

raam.geometry("1300x800")
raam.pack_propagate(0)
raam.resizable(0, 0)
# This is the frame for the Treeview

frame1 = tk.LabelFrame(raam, text="AAPL data")
frame1.place(x=300, y=100, height=350, width=750)
frame2 = tk.LabelFrame(raam, text="Lisainfo")
frame2.place(height = 1300, width = 300)
frame3 = tk.LabelFrame(raam, text="Aktsiad")
frame3.place(x=1050,y=0,height = 1300, width = 250)

variable = tk.StringVar(raam)
variable.set("Päev") # default value

w = tk.OptionMenu(raam, variable, "Päev", "Nädal", "Kuu", "Aasta")
w.place(x=350, y = 60)

l1 = tk.Entry(frame3,width = "200").pack()
l2 = tk.Entry(frame3,width= "200").pack()
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
plt.tight_layout()

ax.set_xticks([])

graafik = FigureCanvasTkAgg(fig, frame1)
graafik.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)


raam.mainloop()