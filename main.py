import math
from tkinter import *

import matplotlib.pyplot
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)


class Data:
    def __init__(self, sampling_time, sampling_freq, mass, spring_constant, x0, b):
        self.b = float(b)
        self.x0 = float(x0)
        self.k = float(spring_constant)
        self.m = float(mass)
        self.dt = float(sampling_freq)
        self.sampling_time = float(sampling_time)

        self.a = None
        self.t = 0
        self.x = self.x0
        self.v = 0

        self.C1 = self.x0 / 2
        self.C = self.x0 / 2
        self.B = self.b / (2 * self.m)
        self.w0 = math.sqrt(self.k / self.m)
        self.w1 = math.sqrt(self.w0 ** 2 - self.B ** 2)

        self.arguments = [self.a, self.t, self.dt, self.m, self.b, self.k, self.x0, self.x, self.v,
                          self.C1, self.C, self.B, self.w0, self.w1]

        self.list_a = []
        self.list_v = []
        self.list_x = []
        self.list_t = []

        self.main_loop()

    def main_loop(self):
        print(f"main_loop")
        while self.t < self.sampling_time:
            self.a = (-self.k * self.x - self.b * self.v) / self.m
            self.list_a.append(round(self.a, 3))

            self.v = self.v + self.a * self.dt
            self.list_v.append(round(self.v, 3))

            self.x = self.x + self.v * self.dt
            self.list_x.append(round(self.x, 3))

            self.t = self.t + self.dt
            self.list_t.append(round(self.t, 1))


    def get_acceleration_plot_data(self):
        return self.list_a, self.list_t

    def get_velocity_plot_data(self):
        return self.list_v, self.list_t

    def get_position_plot_data(self):
        return self.list_x, self.list_t

    @staticmethod
    def make_plots(x, y):
        plt.plot(x, y)
        plt.show()


class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1420x720")

        self.frame_entry = LabelFrame(self.root, text="Parametryzacja")
        self.frame_plots = LabelFrame(self.root, text="Wykresy")

        # czas prókowania
        self.entry_sampling_time = Entry(self.frame_entry, width=5, font=('Lucid', 12))
        # częśtotliwość prókowania
        self.entry_sampling_freq = Entry(self.frame_entry, width=5, font=('Lucid', 12))
        # masa
        self.entry_mass = Entry(self.frame_entry, width=5, font=('Lucid', 12))
        # stała sprężystości
        self.entry_spring_constant = Entry(self.frame_entry, width=5, font=('Lucid', 12))
        # wychylenie początkowe
        self.entry_x0 = Entry(self.frame_entry, width=5, font=('Lucid', 12))
        # Beta
        self.entry_b = Entry(self.frame_entry, width=5, font=('Lucid', 12))

        self.button_make_plot = Button(self.frame_entry, text="Make plot", width=10, command=self.make_plot)

        self.label_sampling_time = Label(self.frame_entry, width=25, text="Czas próbkowania:")
        self.label_sampling_freq = Label(self.frame_entry, width=25, text="Częstotliwość próbkowania:")
        self.label_mass = Label(self.frame_entry, width=25, text="Masa:")
        self.label_spring_constant = Label(self.frame_entry, width=25, text="Stała sprężystości:")
        self.label_x0 = Label(self.frame_entry, width=25, text="Wychylenie początkowe:")
        self.label_b = Label(self.frame_entry, width=25, text="Współczynnik Beta:")

        """
        Acceleration canvas
        """
        self.fig_acceleration = Figure(figsize=(7, 7), dpi=50)
        self.canvas_acceleration = FigureCanvasTkAgg(self.fig_acceleration, master=self.frame_plots)
        self.canvas_acceleration.draw()
        """
        Velocity canvas
        """
        self.fig_velocity = Figure(figsize=(7, 7), dpi=50)
        self.canvas_velocity = FigureCanvasTkAgg(self.fig_velocity, master=self.frame_plots)
        self.canvas_velocity.draw()
        """
        Position canvas
        """
        self.fig_position = Figure(figsize=(7, 7), dpi=50)
        self.canvas_position = FigureCanvasTkAgg(self.fig_position, master=self.frame_plots)
        self.canvas_position.draw()


        self.entry_sampling_time.insert(0, '3')
        self.entry_sampling_freq.insert(0, '0.001')
        self.entry_mass.insert(0, '0.05')
        self.entry_spring_constant.insert(0, '5')
        self.entry_x0.insert(0, '0.1')
        self.entry_b.insert(0, '0.1')

        self.publish()

    def make_plot(self):
        sampling_time = self.entry_sampling_time.get()
        sampling_freq = self.entry_sampling_freq.get()
        mass = self.entry_mass.get()
        sprint_constant = self.entry_spring_constant.get()
        x0 = self.entry_x0.get()
        b = self.entry_b.get()

        Main_Data = Data(sampling_time, sampling_freq, mass, sprint_constant, x0, b)
        a, y = Main_Data.get_acceleration_plot_data()
        v, y = Main_Data.get_velocity_plot_data()
        x, y = Main_Data.get_position_plot_data()

        """
        Acceleration canvas
        """
        self.fig_acceleration = Figure(figsize=(7, 7), dpi=50)
        plot_a = self.fig_acceleration.add_subplot(111)
        plot_a.plot(a)
        plot_a.set_xlabel('t [s]')
        plot_a.set_ylabel('a [m/s^2]')
        plot_a.grid()
        self.canvas_acceleration = FigureCanvasTkAgg(self.fig_acceleration, master=self.frame_plots)
        self.canvas_acceleration.draw()
        self.canvas_acceleration.get_tk_widget().grid(column=1, row=1, columnspan=3, padx=10, pady=10)

        """
        Velocity canvas
        """
        self.fig_velocity = Figure(figsize=(7, 7), dpi=50)
        plot_v = self.fig_velocity.add_subplot(111)
        plot_v.plot(v)
        plot_v.set_xlabel('t [s]')
        plot_v.set_ylabel('v [m/s]')
        plot_v.grid()
        self.canvas_acceleration = FigureCanvasTkAgg(self.fig_velocity, master=self.frame_plots)
        self.canvas_acceleration.draw()
        self.canvas_acceleration.get_tk_widget().grid(column=4, row=1, columnspan=3, padx=10, pady=10)

        """
        Position canvas
        """
        self.fig_position = Figure(figsize=(7, 7), dpi=50)
        plot_x = self.fig_position.add_subplot(111)
        plot_x.plot(x)
        plot_x.set_xlabel('t [s]')
        plot_x.set_ylabel('x [m]')
        plot_x.grid()
        self.canvas_acceleration = FigureCanvasTkAgg(self.fig_position, master=self.frame_plots)
        self.canvas_acceleration.draw()
        self.canvas_acceleration.get_tk_widget().grid(column=7, row=1, columnspan=3, padx=10, pady=10)

    def publish(self):
        self.frame_entry.grid(column=1, row=1, padx=5, pady=5)
        self.frame_plots.grid(column=1, row=2, padx=5, pady=5)

        self.label_sampling_time.grid(column=1, row=1, padx=5, pady=5)
        self.label_sampling_freq.grid(column=1, row=2, padx=5, pady=5)
        self.label_mass.grid(column=1, row=3, padx=10, pady=5)
        self.label_spring_constant.grid(column=1, row=4, padx=5, pady=5)
        self.label_x0.grid(column=1, row=5, padx=5, pady=5)
        self.label_b.grid(column=1, row=6, padx=5, pady=5)

        self.entry_sampling_time.grid(column=2, row=1, padx=5, pady=5)
        self.entry_sampling_freq.grid(column=2, row=2, padx=5, pady=5)
        self.entry_mass.grid(column=2, row=3, padx=5, pady=5)
        self.entry_spring_constant.grid(column=2, row=4, padx=5, pady=5)
        self.entry_x0.grid(column=2, row=5, padx=5, pady=5)
        self.entry_b.grid(column=2, row=6, padx=5, pady=5)

        self.button_make_plot.grid(column=3, row=1, rowspan=6, padx=10, pady=5)

        self.canvas_acceleration.get_tk_widget().grid(column=1, row=1, columnspan=3, padx=10, pady=10)
        self.canvas_velocity.get_tk_widget().grid(column=4, row=1, columnspan=3, padx=10, pady=10)
        self.canvas_position.get_tk_widget().grid(column=7, row=1, columnspan=3, padx=10, pady=10)

if __name__ == "__main__":
    Main_GUI = GUI()
    Main_GUI.root.mainloop()