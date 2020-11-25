import pandas_datareader as pdr
import yfinance as yf
import tkinter as tk
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import tkinter.font as tkFont

# esimese aktsia kuvamine programmi käivitudes
# x-telg korda
# informatsiooni juurde
# kujundus ilusamaks
# kood korda
# info automaatne uuendamine
# alerti tegemine
# hiir graafikul funktsionaalsus


def onClick(event):
    aktsia = event.widget.get()
    if (len(aktsia) < 1):
        print("klikkasid tühja")
    elif aktsia != frame1.cget("text"):
        print("klikkasid", aktsia)
        vaadeldavAktsia = aktsia
        vahetaGraafik(vaadeldavAktsia)


def caps(event):
    entryStringVars[entries.index(event.widget)].set(event.widget.get().upper())


def ajavahetus(event):
    print("Vahetasid ajavahemiku")
    print("Hetkel vaatan:", frame1.cget("text"))
    vahetaGraafik(frame1.cget("text"))


def salvesta(event):
    vaadeldavAktsia = event.widget.get()
    f = open("nimekiri.txt","w")

    for u in range(0,len(entryStringVars)):
        f.write(entryStringVars[u].get()+"\n")
    f.close()

    if (len(vaadeldavAktsia) < 1):
        print("Tühi")
    else:
        vahetaGraafik(vaadeldavAktsia)
        print(vaadeldavAktsia)
        raam.focus_set()


def vahetaGraafik(vaadeldavAktsia):
    print(variable.get())
    frame1.configure(text=vaadeldavAktsia)
    frame2.configure(text=vaadeldavAktsia)

    aktsia = yf.Ticker(vaadeldavAktsia)

    an.config(text = aktsia.get_info()["shortName"])
    hind = aktsia.get_info()["lastMarket"]
    if hind == None:
        hind = aktsia.get_info()["previousClose"]
    ah.config(text = hind)
    täna = datetime.today()
    period = ""
    interval = ""
    if (variable.get() == "Päev"):
        period = "1d"
        interval = "5m"
    elif (variable.get() == "Nädal"):
        period = "5d"
        interval = "15m"
    elif (variable.get() == "Kuu"):
        period = "1mo"
        interval = "90m"
    elif (variable.get() == "Aasta"):
        period = "1y"
        interval = "5d"
    yf.pdr_override()



    data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers=vaadeldavAktsia,

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

    ).to_csv("info.csv")
    f = open("info.csv")
    aktsiaInfo = []

    for line in f:
        info = line.strip().split(",")
        aktsiaInfo.append(info)

    f.close()
    print(aktsiaInfo)

    päevad = []
    hinnad = []

    aktsiaInfo.pop(0)

    for p in aktsiaInfo:
        päevad.append(p[0])
        hinnad.append(round(float(p[4]), 5))

    kohandatud_päevad = []

    if (variable.get() == "Päev"):
        for el in päevad:
            kohandatud_päevad.append((el.split(" ")[1]).split("-")[0][:-3])
    else:
        #Ajutine
        kohandatud_päevad = päevad

       # elif (variable.get() == "Nädal"):
       #     for el in päevad:
       #         el = el.split(" ")[1]
       # elif (variable.get() == "Kuu"):
       #     for el in päevad:
       #         el = el.split(" ")[1]
       # elif (variable.get() == "Aasta"):
       #     for el in päevad:
       #         el = el.split(" ")[1]

    print(päevad)
    print(hinnad)
    print(len(hinnad))

    data1 = {"Päevad": kohandatud_päevad,
             "Hinnad": hinnad}

    df1 = DataFrame(data1, columns=["Päevad", "Hinnad"])

    fig = plt.figure(figsize=(15, 2))
    plt.margins(x=0)
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(kohandatud_päevad, hinnad, color="r")
    plt.grid()
    if (variable.get() == "Päev"):
        ax.set_xticks(["10:00", "12:00", "14:00"])
    else:
        ax.set_xticks([])

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


#Lisainfo akna sisu
frame2 = tk.LabelFrame(raam, text="Lisainfo")
frame2.place(height=1300, width=300)

an = tk.Label(frame2 ,text = "", font = tkFont.Font(size = 15))
ah = tk.Label(frame2 ,text = 0.0, font = tkFont.Font(size = 20))

an.grid(row = 0,column = 0, sticky = "W",padx = 5, pady = 5)
ah.grid(row = 1,column = 0, sticky = "W",padx = 5, pady = 5)
###

frame3 = tk.LabelFrame(raam, text="Aktsiad")
frame3.place(x=1050, y=0, height=1300, width=250)

variable = tk.StringVar(raam)
variable.set("Päev")

w = tk.OptionMenu(raam, variable, "Päev", "Nädal", "Kuu", "Aasta", command=ajavahetus)
w.place(x=350, y=60)

entries = []
entryStringVars = []

#Nimekirja laadimine ja esimese aktsia kuvamine
f = open("nimekiri.txt")
vaadeldavAktsia =  ""
for i in range(25):
    var = tk.StringVar()
    l = tk.Entry(frame3, textvariable=var)
    l.bind("<Button-1>", onClick)
    l.bind("<Return>", salvesta)
    l.bind("<KeyRelease>", caps)
    entries.append(l)
    entryStringVars.append(var)
    var.set(f.readline().strip())
    if(len(vaadeldavAktsia) == 0):
        vaadeldavAktsia = var.get()
    l.grid(row=i, column=0, pady=5)

if(len(vaadeldavAktsia)) != 0:
    vahetaGraafik(vaadeldavAktsia)
f.close()

raam.mainloop()
