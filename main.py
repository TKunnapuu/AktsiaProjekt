import tkinter as tk
import tkinter.font as tkFont
from datetime import datetime

import matplotlib.pyplot as plt
import yfinance as yf
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from pytz import timezone

global turg_avatud
turg_avatud = False
global värskendusAeg
global värskendusSagedus
värskendusAeg = 0
värskendusSagedus = 30


def onClick(event):
    aktsia = event.widget.get()
    if len(aktsia) < 1:
        print("klikkasid tühja")
    elif aktsia != frame1.cget("text"):
        print("klikkasid", aktsia)
        vaadeldavAktsia = aktsia
        vahetaGraafik(vaadeldavAktsia)


def kasAvatud():
    tp = datetime.today().weekday()
    if tp < 6:
        return True
    else:
        return False


def caps(event):
    entryStringVars[entries.index(event.widget)].set(event.widget.get().upper())


def ajavahetus(aeg):
    print("Vahetasid ajavahemiku")
    print("Hetkel vaatan:", frame1.cget("text"))
    variable.set(aeg)
    vahetaGraafik(frame1.cget("text"))


def salvesta(event):
    vaadeldavAktsia = event.widget.get()
    f = open("nimekiri.txt", "w")

    for u in range(0, len(entryStringVars)):
        f.write(entryStringVars[u].get() + "\n")
    f.close()

    if len(vaadeldavAktsia) < 1:
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

    an.config(text=aktsia.get_info()["shortName"])

    amcv = aktsia.get_info()["marketCap"]
    if amcv < 1000000000:
        amcv = str(round(amcv / 1000000, 2)) + " M"
    elif amcv < 1000000000000:
        amcv = str(round(amcv / 1000000000, 2)) + "B"
    elif amcv < 1000000000000000:
        amcv = str(round(amcv / 1000000000000, 2)) + "T"

    #for mm in aktsia.get_info():
    #    print(mm)

    amc1.config(text=amcv)

    if "trailingPE" in aktsia.get_info():
        ape1.config(text=round(float(aktsia.get_info()["trailingPE"]), 1))
    else:
        try:
            ape1.config(text=round(float(aktsia.get_info()["forwardPE"]), 1))
        except:
            ape1.config(text="-")
    if aktsia.get_info()["dividendYield"] != None:
        adiv = str(round(float(aktsia.get_info()["dividendYield"]) * 100, 2)) + "%"
        adiv1.config(text=adiv)
    else:
        adiv1.config(text="-")

    a200d.config(text=round(float(aktsia.get_info()["twoHundredDayAverage"]), 2))
    a50d.config(text=round(float(aktsia.get_info()["fiftyDayAverage"]), 2))

    täna = datetime.today()
    period = ""
    interval = ""
    if variable.get() == "1P":
        period = "1d"
        interval = "2m"
    elif variable.get() == "5P":
        period = "5d"
        interval = "5m"
    elif variable.get() == "1K":
        period = "1mo"
        interval = "30m"
    elif variable.get() == "6K":
        period = "6mo"
        interval = "1d"
    elif variable.get() == "1A":
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

    if variable.get() == "1P":  # X telje väärtuste loomine
        for el in päevad:
            kohandatud_päevad.append((el.split(" ")[1]).split("-")[0][:-3])
        hind = hinnad[-1]
        openHind = aktsia.get_info()["previousClose"]

    elif variable.get() == "5P":
        tp = datetime.today().weekday()
        th = datetime.today().day
        tt = int(päevad[-1].split(" ")[0][-2:])
        nädalapäevad = ["Esmaspäev", "Teisipäev", "Kolmapäev", "Neljapäev", "Reede"]
        for i in range(tp + 1 - (th - tt)):
            nädalapäevad.append(nädalapäevad.pop(0))
        for el in päevad:
            if el.split(" ")[1] == "09:30:00-05:00":
                el = nädalapäevad.pop(0)
            kohandatud_päevad.append(el)
        hind = hinnad[-1]
        openHind = hinnad[0]
    elif variable.get() == "1K":
        for el in päevad:
            if el.split(" ")[1] == "09:30:00-05:00":
                el = el.split(" ")[0][5:]
                kohandatud_päevad.append(el)
            else:
                kohandatud_päevad.append(el)

        hind = hinnad[-1]
        openHind = hinnad[0]
    elif variable.get() == "6K":
        tp = datetime.today().month
        kuud = ["Jaan.", "Veebr.", "Märts", "Aprill", "Mai", "Juuni",
                "Juuli", "August", "Sept.", "Okt.", "Nov.", "Dets."]

        for i in range(tp):
            kuud.append(kuud.pop(0))
        kuud = kuud[-6:]
        praegune_kuu = ""
        for el in päevad:
            if praegune_kuu != el[5:7]:
                praegune_kuu = el[5:7]
                if el[-2:] == "01" or el[-2:] == "02" or el[-2:] == "03":
                    el = kuud.pop(0)
            kohandatud_päevad.append(el)
        hind = hinnad[-1]
        openHind = hinnad[0]
    elif variable.get() == "1A":
        tp = datetime.today().month

        kuud = ["Jaan.", "Veebr.", "Märts", "Aprill", "Mai", "Juuni",
                "Juuli", "August", "Sept.", "Okt.", "Nov.", "Dets."]
        for i in range(tp - 1):
            kuud.append(kuud.pop(0))

        praegune_kuu = ""
        for el in päevad:
            if praegune_kuu != el[5:7]:
                #print("uus kuu", el[5:7])
                praegune_kuu = el[5:7]
                if el[-2:] == "01" or el[-2:] == "02" or el[-2:] == "03":
                    el = kuud.pop(0)
                else:
                    kuud.append(kuud.pop(0))
            kohandatud_päevad.append(el)
        hind = hinnad[-1]
        openHind = hinnad[0]

    ah.config(text=round(hind, 2))
    ah1v = round(hind - openHind, 2)
    ah2v = round(100 * (hind - openHind) / openHind, 2)

    if ah1v < 0:
        ah1.config(text=round(hind - openHind, 2), fg="red")
        ah2.config(text="(" + str(ah2v) + "%)", fg="red")
    else:
        ah1.config(text=round(hind - openHind, 2), fg="green")
        ah2.config(text="(" + str(ah2v) + "%)", fg="green")

    fig = plt.figure(figsize=(20, 4))
    fig.patch.set_facecolor('#F0F0F0')
    plt.margins(x=0)

    ax = plt.subplot()

    # Tee x telg
    xteljed = []
    xväärtused = []

    if variable.get() == "1P":
        for i in range(9, 16, 1):
            for j in range(0, 59):
                if j < 10:
                    j = str(0) + str(j)
                if i == 9 and int(j) >= 30:
                    xteljed.append("0" + str(i) + ":" + str(j))
                elif i != 9:
                    xteljed.append(str(i) + ":" + str(j))
        for i in range(len(xteljed)):
            xväärtused.append(aktsia.get_info()["previousClose"])
        ax.plot(xteljed, xväärtused)
    else:
        for i in range(len(kohandatud_päevad)):
            xväärtused.append(hinnad[0])
        ax.plot(kohandatud_päevad, xväärtused)
        # print("xteljed: ", kohandatud_päevad)
        # print("xväärtused: ", xväärtused)

    ax.plot(kohandatud_päevad, hinnad, color="g")

    madalad_hinnad = []
    for v in hinnad:
        if v < openHind:
            madalad_hinnad.append(v)
        else:
            madalad_hinnad.append("")

    plt.grid()
    if variable.get() == "1P":
        ax.set_xticks(["10:00", "12:00", "14:00"])
    elif variable.get() == "5P":
        ax.set_xticks(["Esmaspäev", "Teisipäev", "Kolmapäev", "Neljapäev", "Reede"])

    elif variable.get() == "1K":
        valitud_päevad = []
        for i in range(len(kohandatud_päevad)):
            if (len(kohandatud_päevad[i]) < 11) and i % 5 == 0:
                valitud_päevad.append(kohandatud_päevad[i])

        ax.set_xticks(valitud_päevad)


    elif variable.get() == "6K":
        tp = datetime.today().month
        kuud = ["Jaan.", "Veebr.", "Märts", "Aprill", "Mai", "Juuni",
                "Juuli", "August", "Sept.", "Okt.", "Nov.", "Dets."]
        for i in range(tp):
            kuud.append(kuud.pop(0))
        kuud = kuud[-6:]
        ax.set_xticks(kuud)

    elif variable.get() == "1A":
        ax.set_xticks(["Jaan.", "Veebr.", "Märts", "Aprill", "Mai", "Juuni",
                       "Juuli", "August", "Sept.", "Okt.", "Nov.", "Dets."])

    for widget in frame1.winfo_children():
        widget.destroy()

    graafik = FigureCanvasTkAgg(fig, frame1)

    graafik.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)


raam = tk.Tk()

raam.geometry("1350x550")
raam.title("Aktsia projekt")
raam.pack_propagate(0)
raam.resizable(0, 0)

frames = []

# Graafiku aken
frame1 = tk.LabelFrame(raam, text="AAPL data")
frame1.place(x=300, y=40, height=450, width=850)

frames.append(frame1)

# Lisainfo akna sisu
frame2 = tk.LabelFrame(raam, text="Lisainfo")
frame2.place(height=1300, width=300)
frames.append(frame2)

an = tk.Label(frame2, text="", font=tkFont.Font(size=15))
ah = tk.Label(frame2, text=0.0, font=tkFont.Font(size=18))
ah1 = tk.Label(frame2, text="(" + str(0.0) + "%)", font=tkFont.Font(size=18))
ah2 = tk.Label(frame2, text="(" + str(0.0) + "%)", font=tkFont.Font(size=18))

amc = tk.Label(frame2, text="Turukapital", font=tkFont.Font(size=15))
amc1 = tk.Label(frame2, text=0.0, font=tkFont.Font(size=15))

ape = tk.Label(frame2, text="P/E suhe", font=tkFont.Font(size=15))
ape1 = tk.Label(frame2, text=0.0, font=tkFont.Font(size=15))

adiv = tk.Label(frame2, text="Div. määr", font=tkFont.Font(size=15))
adiv1 = tk.Label(frame2, text="-", font=tkFont.Font(size=15))

a200 = tk.Label(frame2, text="200 päev kesk.", font=tkFont.Font(size=15))
a200d = tk.Label(frame2, text="-", font=tkFont.Font(size=15))

a50 = tk.Label(frame2, text="50 päev kesk.", font=tkFont.Font(size=15))
a50d = tk.Label(frame2, text="-", font=tkFont.Font(size=15))

an.grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)
ah.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
ah1.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
ah2.grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)

amc.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
amc1.grid(row=2, column=2, columnspan=1, sticky=tk.W, padx=5, pady=5)

ape.grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
ape1.grid(row=3, column=2, columnspan=1, sticky=tk.W, padx=5, pady=5)

adiv.grid(row=4, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
adiv1.grid(row=4, column=2, columnspan=1, sticky=tk.W, padx=5, pady=5)

a200.grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
a200d.grid(row=5, column=2, columnspan=1, sticky=tk.W, padx=5, pady=5)

a50.grid(row=6, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
a50d.grid(row=6, column=2, columnspan=1, sticky=tk.W, padx=5, pady=5)

###

frame3 = tk.LabelFrame(raam, text="Aktsiad")
frame3.place(x=1150, y=0, height=1300, width=200)
frames.append(frame3)

variable = tk.StringVar(raam)
variable.set("1P")

frame4 = tk.Frame(raam)
frame4.place(x=300, y=490, height=100, width=850)
frames.append(frame4)

#

# w = tk.OptionMenu(raam, variable, "Päev", "Nädal", "Kuu", "Aasta", command=ajavahetus)
# w.place(x=350, y=455)

b1 = tk.Button(frame4, width=15, text="1 päev", command=lambda: ajavahetus("1P"))
b2 = tk.Button(frame4, width=15, text="5 päeva", command=lambda: ajavahetus("5P"))
b3 = tk.Button(frame4, width=15, text="1 kuu", command=lambda: ajavahetus("1K"))
b4 = tk.Button(frame4, width=15, text="6 kuud", command=lambda: ajavahetus("6K"))
b5 = tk.Button(frame4, width=15, text="1 aasta", command=lambda: ajavahetus("1A"))

b1.grid(row=0, column=0, padx=5, pady=5)
b2.grid(row=0, column=1, padx=5, pady=5)
b3.grid(row=0, column=2, padx=5, pady=5)
b4.grid(row=0, column=3, padx=5, pady=5)
b5.grid(row=0, column=4, padx=5, pady=5)

entries = []
entryStringVars = []

# for frame in frames:
#    frame.config(bg = "black")

# Nimekirja laadimine ja esimese aktsia kuvamine
f = open("nimekiri.txt")
vaadeldavAktsia = ""
for i in range(14):
    var = tk.StringVar()
    l = tk.Entry(frame3, textvariable=var)
    l.bind("<Button-1>", onClick)
    l.bind("<Return>", salvesta)
    l.bind("<KeyRelease>", caps)
    entries.append(l)
    entryStringVars.append(var)
    var.set(f.readline().strip())
    if len(vaadeldavAktsia) == 0:
        vaadeldavAktsia = var.get()
    l.grid(row=i, column=0, pady=5)

if (len(vaadeldavAktsia)) != 0:
    vahetaGraafik(vaadeldavAktsia)
f.close()


def time():
    nyse = timezone('America/New_York')
    nyse_time = datetime.now(nyse)
    string = nyse_time.strftime('%H:%M:%S')
    global turg_avatud
    global värskendusAeg
    global värskendusSagedus
    värskendusAeg += 1

    if turg_avatud and värskendusAeg >= värskendusSagedus:
        värskendusAeg = 0
        vahetaGraafik(frame1.cget("text"))

    if nyse_time.hour >= 16 or nyse_time.hour <= 8 or nyse_time.hour <= 9 and nyse_time.minute <= 30:
        turg_avatud = False
        kasAvatudLbl.config(text="Suletud", fg="red")
    else:
        turg_avatud = True
        kasAvatudLbl.config(text="Avatud", fg="green")

    lbl.config(text=string)
    lbl.after(1000, time)


frame5 = tk.Frame(raam)
frame5.place(x=300, y=0, height=40, width=850)
frame5.columnconfigure(0, weight=1)
frames.append(frame5)

lbl = tk.Label(frame5, font=('calibri', 20, 'bold'))
kasAvatudLbl = tk.Label(frame5, text="Avatud", font=('calibri', 15, 'bold'))

kasAvatudLbl.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
lbl.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)

time()
raam.mainloop()
