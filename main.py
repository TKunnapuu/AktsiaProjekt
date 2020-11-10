import pandas_datareader as pdr
import yfinance as yf
import tkinter as tk
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def onClick(event):
    print("Tere")

def salvesta(event):
    print("Head aega")
    vaadeldavAktsia = event.widget.get()
    frame1.configure(text = vaadeldavAktsia)
    vahetaGraafik(vaadeldavAktsia)
    print(vaadeldavAktsia)
    raam.focus_set()

def vahetaGraafik(vaadeldavAktsia):
    print(variable.get())
    täna = datetime.today()
    period = ""
    interval = ""
    if(variable.get() == "Päev"):
        period = "1d"
        interval = "15m"
    elif(variable.get()== "Nädal"):
        period = "5d"
        interval = "30m"
    elif(variable.get()=="Kuu"):
        period = "1mo"
        interval = "90m"
    elif(variable.get()=="Aasta"):
        period = "1y"
        interval = "5d"
    yf.pdr_override()

    data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = vaadeldavAktsia,

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period=period,

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval=interval,

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by='ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust=True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost=False,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads=True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy=None
    ).to_csv("info.csv")
    f = open("info.csv")
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
        hinnad.append(round(float(p[4]), 5))

    print(päevad)
    print(hinnad)

    data1 = {"Päevad": päevad,
             "Hinnad": hinnad}

    df1 = DataFrame(data1, columns=["Päevad", "Hinnad"])

    fig = plt.figure(figsize=(15,2))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(päevad, hinnad, color="r")
    plt.grid()
    ax.set_xticks(päevad)
    for widget in frame1.winfo_children():
        widget.destroy()
    graafik = FigureCanvasTkAgg(fig, frame1)
    graafik.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)


raam = tk.Tk()

raam.geometry("1300x800")
raam.title("Aktsia projekt")
raam.pack_propagate(0)
raam.resizable(0, 0)
frame1 = tk.LabelFrame(raam, text="AAPL data")
frame1.place(x=300, y=100, height=350, width=750)
frame2 = tk.LabelFrame(raam, text="Lisainfo")
frame2.place(height = 1300, width = 300)
frame3 = tk.LabelFrame(raam, text="Aktsiad")
frame3.place(x=1050,y=0,height = 1300, width = 250)

variable = tk.StringVar(raam)
variable.set("Päev")

w = tk.OptionMenu(raam, variable, "Päev", "Nädal", "Kuu", "Aasta")
w.place(x=350, y = 60)



entries = []

for i in range(25):
    l = tk.Entry(frame3)
    l.bind("<Button-1>", onClick)
    l.bind("<Return>", salvesta)
    entries.append(l)
    l.grid(row=i, column=0, pady=5)


#for el in lx:
#    el = tk.Entry(frame3,textvariable = svx[c] ,width = "200")
#    el.bind("<Button-1>", onClick)
#    el.bind("<Return>", salvesta)
#    el.pack()
#    c+=1


    #l1 = tk.Entry(frame3,textvariable = sv ,width = "200")
    #l1.bind("<Button-1>", onClick)
    #l1.bind("<Return>", salvesta)
    #l1.pack()





raam.mainloop()