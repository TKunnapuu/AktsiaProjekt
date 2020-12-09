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


    täna = datetime.today()
    period = ""
    interval = ""
    if (variable.get() == "Päev"):
        period = "1d"
        interval = "2m"
    elif (variable.get() == "Nädal"):
        period = "5d"
        interval = "15m"
    elif (variable.get() == "Kuu"):
        period = "1mo"
        interval = "60m"
    elif (variable.get() == "Aasta"):
        period = "1y"
        interval = "1d"
    yf.pdr_override()

    data = yf.download(
        tickers=vaadeldavAktsia,
        period=period,
        interval=interval,
        group_by='ticker',
        auto_adjust=True,
        prepost=False,
        threads=True,
    ).to_csv("info.csv")

    f = open("info.csv")
    aktsiaInfo = []

    for line in f:
        info = line.strip().split(",")
        aktsiaInfo.append(info)

    f.close()

    päevad = []
    hinnad = []

    aktsiaInfo.pop(0)

    for p in aktsiaInfo:
        päevad.append(p[0])
        try:
            hinnad.append(round(float(p[4]), 5))
        except:
            hinnad.append(hinnad[-1])

    kohandatud_päevad = []

    if (variable.get() == "Päev"):  # X telje väärtuste loomine
        for el in päevad:
            kohandatud_päevad.append((el.split(" ")[1]).split("-")[0][:-3])
        hind = hinnad[-1]
        openHind = aktsia.get_info()["previousClose"]
    else:
        #Ajutine
        kohandatud_päevad = päevad
        hind = hinnad[-1]
        openHind = hinnad[1]

       # elif (variable.get() == "Nädal"):
       #     for el in päevad:
       #         el = el.split(" ")[1]
       # elif (variable.get() == "Kuu"):
       #     for el in päevad:
       #         el = el.split(" ")[1]
       # elif (variable.get() == "Aasta"):
       #     for el in päevad:
       #         el = el.split(" ")[1]




    ah.config(text=round(hind,2))
    ah1v = round(hind - openHind,2)
    if ah1v < 0:
        ah1.config(text=round(hind - openHind, 2), fg = "red")
        ah2.config(text="(" + str(round(round(hind - openHind, 2) / hind * 100, 2)) + "%)",fg = "red")
    else:
        ah1.config(text=round(hind - openHind,2),fg = "green")
        ah2.config(text="("+str(round(round(hind - openHind,2)/hind*100,2))+"%)", fg = "green")

    data1 = {"Päevad": kohandatud_päevad,
             "Hinnad": hinnad}

    df1 = DataFrame(data1, columns=["Päevad", "Hinnad"])

    fig = plt.figure(figsize=(15, 2))
    plt.margins(x=0)
    ax = fig.add_subplot(1, 1, 1)

    #Tee x telg
    xteljed = []
    for i in range(9,16,1):
        for j in range(0,59):
            if j < 10:
                j = str(0)+str(j)
            if i == 9 and int(j) < 30:
                print("")
            elif i == 9:
                xteljed.append("0"+str(i)+":"+str(j))
            else:
                xteljed.append(str(i)+":"+str(j))


    xväärtused = []



    if (variable.get() == "Päev"):
        for i in range(len(xteljed)):
            xväärtused.append(aktsia.get_info()["previousClose"])
        ax.plot(xteljed,xväärtused)
    #else:  #TODO
    #    for i in range(len(xteljed)):
    #        xväärtused.append(hinnad[1])
    #    ax.plot(xteljed,xväärtused)

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
ah = tk.Label(frame2 ,text = 0.0, font = tkFont.Font(size = 18))
ah1 = tk.Label(frame2, text= "("+str(0.0)+"%)", font = tkFont.Font(size = 18))
ah2 = tk.Label(frame2, text= "("+str(0.0)+"%)", font = tkFont.Font(size = 18))


an.grid(row = 0, column = 0, columnspan = 3, sticky = tk.W,padx = 5, pady = 5)
ah.grid(row = 1, column = 0, sticky = tk.W,padx = 5, pady = 5)
ah1.grid(row = 1, column = 1 ,sticky = tk.W ,padx = 5, pady= 5)
ah2.grid(row = 1, column = 2 ,sticky = tk.W ,padx = 5, pady= 5)

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
