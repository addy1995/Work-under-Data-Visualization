import numpy
import csv
import matplotlib
matplotlib.use("TkAgg")
try:
    from mpl_toolkits.basemap import Basemap  #
except:
    print("Need to download Basemap module")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from tkinter import *

csvfile = open("Data.csv",encoding="utf-8")
csvfile.readline()
csv = csv.reader(csvfile,delimiter=',')
read_data = []


def read_all_data():
    for row in csv:
        read_data.append(row)


def data_processing_technique1():
    global technique1_data
    technique1_data = {}
    for row in read_data:
        try:
            if row[5].rfind(',') != -1:
                str = row[5][row[5].rfind(',') + 2:].strip()
            elif row[5] != '':
                str = row[5].strip()
            else:
                continue
            if row[2] != '':
                disease = row[2]
            else:
                continue
            technique1_data[str]
            try:
                technique1_data[str][disease]
                if (row[3], row[4]) not in technique1_data[str][disease]:
                    technique1_data[str][disease].append((row[3], row[4]))
            except:
                technique1_data[str][disease] = [(row[3], row[4])]
        except:
            technique1_data[str] = {}
            technique1_data[str][disease] = [(row[3], row[4])]


def data_processing_technique2():
    global technique2_data
    technique2_data = {}
    for row in read_data:
        if row[2] != '':
            try:
                if row[5].rfind(',') != -1:
                    str = row[5][row[5].rfind(',')+2:].strip()
                elif row[5] != '':
                    str = row[5]
                else:
                    continue

                if str not in technique2_data[row[2]]:
                    technique2_data[row[2]].append(str)
            except:
                technique2_data[row[2]] = [str]


def data_processing_technique3():
    global technique3_data
    technique3_data = {}
    for row in read_data:

        if row[2] != '' and row[6] != '':
            try:
                technique3_data[row[2]][0] += int(row[6])
                if row[7] != '':
                    technique3_data[row[2]][1] += int(row[7])
                else:
                    technique3_data[row[2]][1] += 0
            except:
                if row[7] != '':
                    technique3_data[row[2]] = [int(row[6]), int(row[7])]
                else:
                    technique3_data[row[2]] = [int(row[6]), 0]


def data_processing_technique4():
    global technique4_data
    technique4_data = {}
    for row in read_data:
        if row[2] != '':
            try:
                technique4_data[row[2]].append((float(row[3]), float(row[4])))
            except:
                technique4_data[row[2]] = [(float(row[3]), float(row[4]))]


def data_processing_technique5():
    global  technique5_data
    technique5_data = {}
    for row in read_data:
        if row[2] != '':
            try:
                if row[5].rfind(',') != -1:
                    str = row[5][row[5].rfind(',') + 2:].strip()
                elif row[5] != '':
                    str = row[5]
                else:
                    continue
                technique5_data[int(row[8])]
                if row[2] not in technique5_data[int(row[8])][0]:
                    technique5_data[int(row[8])][0].append(row[2])
                if str not in technique5_data[int(row[8])][1]:
                    technique5_data[int(row[8])][1].append(str)
            except:
                technique5_data[int(row[8])] = [[row[2]], [str]]
        pass


class Work(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.container = Frame(self)
        self.container.pack(fill=BOTH,expand=True)
        self.first = FirstTech(self.container,self)
        self.second = SecondTech(self.container,self)
        self.third = ThirdTech(self.container, self)
        self.fourth = FourthTech(self.container, self)
        self.fifth = FifthTech(self.container, self)
        self.title("Data Visualization")
        self.first.pack(fill=BOTH, expand=True)
        self.resizable(False, False)


class FirstTech(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.f = Figure(figsize=(6, 6), dpi=100)
        self.f.subplots_adjust(bottom=0.3, left=0.2)
        self.controller = controller
        self.canvas = FigureCanvasTkAgg(self.f,self)
        self.canvas.get_tk_widget().grid(row=0,column=0,sticky='nswe')
        toolbar_frame = Frame(self)
        toolbar = NavigationToolbar2TkAgg(self.canvas,toolbar_frame)
        toolbar.update()
        toolbar_frame.grid(row=1, column=0, sticky='we')
        next_button = Button(self, text="Next", command=self.next)
        next_button.grid(row=1, column=1, sticky='e')

        self.f.suptitle('Pie Chart of a specific Country where each Sector represents a Disease\n '
                        'and its proportion represents relative no of affected cities')
        scrollbar = Scrollbar(self)
        scrollbar.grid(row=0, column=2, sticky='ns')
        self.select_countries = Listbox(self)
        scrollbar.config(command=self.select_countries.yview)
        self.select_countries.config(yscrollcommand=scrollbar.set)
        self.select_countries.bind("<1>", lambda e: self.process_data(e))
        for row in sorted(technique1_data.keys()):
            self.select_countries.insert(END,row)
        self.select_countries.grid(row=0,column=1,sticky='ns')

        start = self.select_countries.get(0)
        self.subplot = self.f.add_subplot(111)
        data = technique1_data[start]
        values = []
        arr = []
        keys = list(data.keys())
        for key in keys:
            values.append(len(data[key]))
        tup=None
        for a in range(len(keys)-1):
            tup = (1, *tup)

        self.subplot.axis("equal")
        self.subplot.pie(values, labels=keys, startangle=90, shadow=True, autopct="%1.1f%%", explode=tup)
        self.canvas.show()

    def process_data(self,event):
        index = self.select_countries.nearest(event.y)
        _, yoffset, _, height = self.select_countries.bbox(index)
        if event.y > height + yoffset + 5:  # XXX 5 is a niceness factor
            return
        self.subplot.clear()
        selected = self.select_countries.get(index)
        data = technique1_data[selected]
        values = []
        arr = []
        keys = list(data.keys())
        for key in keys:
            arr.append((len(data[key]), key))
        keys = []
        arr.sort(reverse=True)
        num = 10

        for index in range(len(arr)):
            if index >= num:
                if 'Others' not in keys:
                    keys.append('Others')
                    values.append(arr[index][0])
                else:
                    values[-1] += arr[index][0]
                pass
            else:
                keys.append(arr[index][1])
                values.append(arr[index][0])
        tup=()
        for a in range(len(keys)):
            if int(len(keys)/2) == a:
                tup = (0.1, *tup)
            else:
                tup = (0, *tup)

        self.subplot.axis("equal")
        self.subplot.pie(values, labels=keys, shadow=True, autopct="%1.1f%%", explode=tup)
        self.canvas.draw()

    def next(self):
        self.controller.second.pack(fill=BOTH, expand=True)
        self.pack_forget()
        pass


class SecondTech(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.f = Figure(figsize=(6, 6), dpi=100)
        self.f.subplots_adjust(bottom=0.3)
        self.f.suptitle('Bar Chart representing Top 20 most spread Diseases')
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.get_tk_widget().grid(row=0, column=0,columnspan=2, sticky='nswe')
        toolbar_frame = Frame(self)
        toolbar = NavigationToolbar2TkAgg(self.canvas, toolbar_frame)
        toolbar.update()
        toolbar_frame.grid(row=1, column=0, sticky='we')
        next_button = Button(self, text="Next", command=self.next)
        prev_button = Button(self, text="Prev", command=self.prev)

        prev_button.grid(row=1, column=1,sticky='w')
        next_button.grid(row=1, column=1, sticky='e')

        self.subplot = self.f.add_subplot(111)
        arr = []
        for key in technique2_data:
            arr.append((len(technique2_data[key]),key))
        arr.sort(reverse=True)
        keys = []
        values = []
        num = 20
        for a in range(num):
            keys.append(arr[a][1])
            values.append(arr[a][0])

        ind = numpy.arange(num)
        self.subplot.bar(ind, values, label='Red')
        self.subplot.set_xlabel("Diseases")
        self.subplot.set_ylabel("No of Countries")
        self.subplot.set_xticks(ind, minor=False)
        self.subplot.set_xticklabels(keys, fontdict=None, minor=False, rotation='vertical')

    def next(self):
        self.controller.third.pack(fill=BOTH, expand=True)
        self.pack_forget()
        pass

    def prev(self):
        self.controller.first.pack(fill=BOTH, expand=True)
        self.pack_forget()
        pass


class ThirdTech(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.f = Figure(figsize=(12, 6), dpi=100)
        self.f.subplots_adjust(bottom=0.3)
        self.f.suptitle('Stacked Column Chart representing Diseases and its \nCases and Deaths')
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, sticky='nswe')
        toolbar_frame = Frame(self)
        toolbar = NavigationToolbar2TkAgg(self.canvas, toolbar_frame)
        toolbar.update()
        toolbar_frame.grid(row=1, column=0, sticky='we')
        prev_button = Button(self, text="Prev", command=self.prev)
        next_button = Button(self, text="Next", command=self.next)
        next_button.grid(row=1, column=1,sticky='e')
        prev_button.grid(row=1, column=1)

        self.subplot = self.f.add_subplot(111)
        self.subplot.set_xlabel("Diseases")
        self.subplot.set_ylabel("Cases/Deaths")
        self.subplot.legend()
        ind = numpy.arange(len(list(technique3_data.keys())))
        keys = []
        cases = []
        deaths = []

        for key in technique3_data.keys():
            keys.append(key)
            cases.append(technique3_data[key][0])
            deaths.append(technique3_data[key][1])

        self.subplot.bar(ind, cases, 0.35, label='Cases')
        self.subplot.bar(ind, deaths, 0.35, bottom=cases, label='Death')
        self.subplot.legend()
        self.subplot.set_xticks(ind, minor=False)
        self.subplot.set_xticklabels(keys, fontdict=None, minor=False, rotation='vertical')

    def next(self):
        self.controller.fourth.pack(fill=BOTH, expand=True)
        self.pack_forget()
        pass

    def prev(self):
        self.controller.second.pack(fill=BOTH, expand=True)
        self.pack_forget()
        pass


class FourthTech(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.controller = controller
        self.f = Figure(figsize=(6, 6), dpi=100)
        self.f.subplots_adjust(left=None, bottom=None, right=None, top=None,
                    wspace=None, hspace=None)
        self.f.suptitle('World Map showing the spread of the Disease')
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nswe')
        toolbar_frame = Frame(self)
        toolbar = NavigationToolbar2TkAgg(self.canvas, toolbar_frame)
        toolbar.update()
        toolbar_frame.grid(row=1, column=0, sticky='we')
        next_button = Button(self, text="Next", command=self.next)
        prev_button = Button(self, text="Prev", command=self.prev)
        next_button.grid(row=1, column=1, columnspan=2, sticky='e')
        prev_button.grid(row=1, column=1, columnspan=2)

        scrollbar = Scrollbar(self)
        scrollbar.grid(row=0,column=2,sticky='ns')
        self.select_disease = Listbox(self)
        scrollbar.config(command=self.select_disease.yview)
        self.select_disease.config(yscrollcommand=scrollbar.set)
        self.select_disease.bind("<1>", lambda e: self.process_data(e))
        for row in sorted(technique4_data.keys()):
            self.select_disease.insert(END, row)
        self.select_disease.grid(row=0, column=1, sticky='ns')

        start = self.select_disease.get(0)
        self.subplot = self.f.add_subplot(111)
        data = technique4_data[start]

        self.map = Basemap(projection='mill', ax=self.subplot)
        self.map.drawcoastlines()
        self.map.drawcountries(linewidth=1)
        self.map.drawstates()
        self.points = []
        for lat,long in data:
            xpt, ypt = self.map(long,lat)
            self.points.append(self.map.plot(xpt, ypt, 'co', markersize=4)[0])

    def process_data(self, event):
        index = self.select_disease.nearest(event.y)
        _, yoffset, _, height = self.select_disease.bbox(index)
        if event.y > height + yoffset + 5:  # XXX 5 is a niceness factor :)
            return

        selected = self.select_disease.get(index)
        data = technique4_data[selected]
        for point in self.points:
            point.set_ydata(None)
            point.set_xdata(None)
        self.points.clear()
        for lat,long in data:
            xpt, ypt = self.map(long,lat)
            self.points.append(self.map.plot(xpt, ypt, 'co')[0])
        self.canvas.draw()


    def next(self):
        self.controller.fifth.pack(fill=BOTH, expand=True)
        self.pack_forget()
        pass

    def prev(self):
        self.controller.third.pack(fill=BOTH, expand=True)
        self.pack_forget()
        pass


class FifthTech(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.controller = controller
        self.f = Figure(figsize=(6, 6), dpi=100)
        self.f.subplots_adjust(left=None, bottom=None, right=None, top=None,
                    wspace=None, hspace=None)
        self.f.suptitle('Bubble Chart showing variation of Rating,\n no of Diseases and no of Countries')
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.get_tk_widget().grid(row=0, column=0,columnspan=2, sticky='nswe')

        toolbar_frame = Frame(self)
        toolbar = NavigationToolbar2TkAgg(self.canvas, toolbar_frame)
        toolbar.update()
        toolbar_frame.grid(row=1, column=0, sticky='we')
        prev_button = Button(self, text="Prev", command=self.prev)
        prev_button.grid(row=1, column=1, sticky='e')

        data = technique5_data
        diseases = []
        countries = []
        for key in range(5):
            diseases.append(len(data[key+1][0]))
            countries.append(len(data[key+1][1]))

        self.subplot = self.f.add_subplot(111)
        self.subplot.set_xlabel("Rating")
        self.subplot.set_ylabel("No of Diseaes")
        self.subplot.scatter([1, 2, 3, 4, 5], diseases, s=countries, label="No of Countries")
        self.subplot.legend()

    def prev(self):
        self.controller.fourth.pack(fill=BOTH, expand=True)
        self.pack_forget()
        pass

read_all_data()
data_processing_technique1()
data_processing_technique2()
data_processing_technique3()
data_processing_technique4()
data_processing_technique5()
app = Work()
app.mainloop()
