import matplotlib

matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *

from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
import csv
import wave
import sys


class mclass:
    def __init__(self, window):
        self.list1 = []
        self.list2 = []
        self.window = window
        self.box = Entry(window)
        self.in_button = Button(window, text="Read data pt and plot", command=self.readFileAndPlot)
        self.out_button = Button(window, text="Save data pt", command=self.saveFile)
        self.button = Button(window, text="plot", command=self.plot)
        self.sound_button = Button(window, text="Read wav file and plot", command=self.readSoundandPlot)
        self.box.pack()
        self.button.pack()
        self.in_button.pack()
        self.out_button.pack()
        self.sound_button.pack()
        # self.button = Button(self, text="Browse", command=self.load_file, width=10)
        # self.button.grid(row=1, column=0, sticky=W)

    def readFileAndPlot(self):
        filename = askopenfilename()
        count = 0
        # file = open(filename)
        with open(filename, 'r') as file:
            lists = list(csv.reader(file, delimiter= ' '))
            trimmed_list1 = list(filter(None, lists[0]))
            trimmed_list2 = list(filter(None, lists[1]))
            list1 = list(map(int, trimmed_list1))

            list2 = list(map(int, trimmed_list2))

        self.list1 = list1
        self.list2 = list2
        self.plot()
    def readSoundandPlot(self):
        filename = askopenfilename()
        spf = wave.open(filename, 'r')
        signal = spf.readframes(-1)
        signal = np.fromstring(signal, 'Int16')
        if spf.getnchannels() == 2:
            print('Just mono files')
            sys.exit(0)
        fig = Figure()
        a = fig.add_subplot(111)
        a.plot(signal)
        canvas = FigureCanvasTkAgg(fig, master=self.window)

        canvas.get_tk_widget().pack()

        canvas.draw()

    def saveFile(self):
        pathName = askdirectory()
        fileName = pathName + "/dataPoints.csv"
        file = open(fileName, "w")
        for item in self.list1:
            file.write("%s " % item)

        file.write("\n")
        for item in self.list2:
            file.write("%s " % item)

    def plot(self):

        if len(self.list1)==0:
            x = np.random.choice(50, 20, replace=True)
            y = np.random.choice(30, 20, replace=True)
            self.list1 = x
            self.list2 = y
        else:
            x = self.list1
            y = self.list2

        print(x)
        fig = Figure()
        a = fig.add_subplot(111)
        fit = np.polyfit(x, y, 1)
        fit_fn = np.poly1d(fit)
        a.plot(x, y, 'bo', x, fit_fn(x), '-r')
        a.invert_yaxis()

        a.set_title("Estimation Grid", fontsize=16)
        a.set_ylabel("Y", fontsize=14)
        a.set_xlabel("X", fontsize=14)
        a.set_xlim([0,50])
        a.set_ylim([-10,40])

        canvas = FigureCanvasTkAgg(fig, master=self.window)

        canvas.get_tk_widget().pack()

        canvas.draw()


window = Tk()
start = mclass(window)
window.mainloop()
