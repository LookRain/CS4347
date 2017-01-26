import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

class mclass:
    def __init__(self,  window):
        self.window = window
        self.box = Entry(window)
        self.in_button = Button(window, text="import data", command=self.plot)
        self.out_button = Button(window, text="export data", command=self.plot)
        self.button = Button (window, text="plot", command=self.plot)
        self.box.pack ()
        self.button.pack()
        self.in_button.pack()
        self.out_button.pack()

        # self.button = Button(self, text="Browse", command=self.load_file, width=10)
        # self.button.grid(row=1, column=0, sticky=W)




    def plot (self):
        # x=np.array ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        # v= np.array ([16,16.31925,17.6394,16.003,17.2861,17.3131,19.1259,18.9694,22.0003,22.81226])
        # p= np.array ([16.23697,     17.31653,     17.22094,     17.68631,     17.73641 ,    18.6368,
        #     19.32125,     19.31756 ,    21.20247  ,   22.41444   ,  22.11718  ,   22.12453])


        x = np.random.choice(50, 20, replace=True)
        y = np.random.choice(30, 20, replace=True)

        fig = Figure()
        a = fig.add_subplot(111)
        # a.scatter(v,x,color='red')
        fit = np.polyfit(x, y, 1)
        fit_fn = np.poly1d(fit)
        a.plot(x,y, 'bo', x, fit_fn(x), '-r')
        a.invert_yaxis()

        a.set_title ("Estimation Grid", fontsize=16)
        a.set_ylabel("Y", fontsize=14)
        a.set_xlabel("X", fontsize=14)

        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.get_tk_widget().pack()
        canvas.draw()

window= Tk()
start= mclass (window)
window.mainloop()