import threading
from time import sleep
import math

import tkinter as tk
from tkinter import ttk

from control import Control

class GUI:

    def __init__(self):

        self.control = Control()
        self.max_yaw_deg = 359
        self.max_pitch_deg = 70

        self.distances = [[0] * (self.max_pitch_deg + 1)] * (self.max_yaw_deg + 1)

        # GUI STUFF
        self.root = tk.Tk()

        self.title = tk.Label(self.root, text="3D Scanner")
        self.title.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        self.file_path_lbl = tk.Label(self.root, text="File Path:")
        self.file_path_lbl.grid(row=1, column=0, sticky=tk.E, pady=10, padx=10)

        self.file_path_entry = tk.Entry(self.root)
        self.file_path_entry.insert(0, "output.obj")
        self.file_path_entry.grid(row=1, column=1, sticky=tk.W, pady=10, padx=10)

        self.animation_running = False
        self.progress = tk.IntVar()
        self.progressbar = ttk.Progressbar(self.root, variable=self.progress, length=300)
        self.progressbar.grid(row=2, column=0, columnspan=2, pady=10, padx=10)
        
        self.start_btn = tk.Button(self.root, text="Start", command=lambda: self.start_animation())
        self.start_btn.grid(row=3, column=0, sticky=tk.W, pady=10, padx=10)

        self.cancel_btn = tk.Button(self.root, text="Cancel", command=lambda: self.stop_animation())
        self.cancel_btn["state"] = "disabled"
        self.cancel_btn.grid(row=3, column=1, sticky=tk.E, pady=10, padx=10)


        self.feedback_lbl = tk.Label(self.root, text="")
        self.feedback_lbl.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

        self.root.mainloop()


    def animation(self, file_name):

        self.start_btn["state"] = "disabled"
        self.cancel_btn["state"] = "normal"

        self.control.ready_gpio()

        # scan into self.distances
        for yaw_deg in range(0, self.max_yaw_deg + 1):
            self.control.set_yaw(yaw_deg)
            self.progress.set((yaw_deg / self.max_yaw_deg) * 100)

            for pitch_deg in range(0, (self.max_pitch_deg + 1)):
                self.control.set_pitch(pitch_deg)
                self.distances[yaw_deg][pitch_deg] = self.control.get_distance()

            if (self.animation_running == False):
                self.feedback_lbl["text"] = "Canceled scan."
                break

        # if here as a result of finishing the loops, not cancel condition
        if (self.animation_running == True):
            self.output_as_obj(file_name)
            self.feedback_lbl["text"] = "Successfully output results to "+file_name+"."


        self.animation_running = False
        self.start_btn["state"] = "normal"
        self.cancel_btn["state"] = "disabled"
        self.file_path_entry["state"] = "normal"
        self.progress.set(0)


    def start_animation(self):
        if (self.file_path_entry.get() == ""):
            self.feedback_lbl["text"] = "Please enter a file path to output to."
            return

        self.animation_running = True
        self.file_path_entry["state"] = "disabled"
        thread = threading.Thread(target=self.animation, args=[self.file_path_entry.get()])
        thread.start()

    def stop_animation(self):
        self.animation_running = False

    def output_as_obj(self, path):
        fd = open(path, "wt")

        # write vertices
        for yaw_deg in range(0, self.max_yaw_deg + 1):
            for pitch_deg in range(0, (self.max_pitch_deg + 1)):
                x_coord = self.distances[yaw_deg][pitch_deg] * math.cos(yaw_deg * math.pi / 180) * math.cos(pitch_deg * math.pi / 180)
                z_coord = self.distances[yaw_deg][pitch_deg] * math.sin(yaw_deg * math.pi / 180) * math.cos(pitch_deg * math.pi / 180)
                y_coord = self.distances[yaw_deg][pitch_deg] * math.sin(pitch_deg * math.pi / 180)
                fd.write("v "+str(x_coord)+" "+str(y_coord)+" "+str(z_coord)+"\n")

        # write faces
        for yaw_deg in range(0, self.max_yaw_deg):
            for pitch_deg in range(0, self.max_pitch_deg):
                #    v1             v2
                #
                #
                #    v4             v3

                v1 = 1 + (yaw_deg * (self.max_pitch_deg + 1) + pitch_deg)
                v2 = 1 + ((yaw_deg + 1) * (self.max_pitch_deg + 1) + pitch_deg)
                v3 = 1 + ((yaw_deg + 1) * (self.max_pitch_deg + 1) + (pitch_deg + 1))
                v4 = 1 + (yaw_deg * (self.max_pitch_deg + 1) + (pitch_deg + 1))
                fd.write("f "+str(v1)+" "+str(v2)+" "+str(v3)+"\n")
                fd.write("f "+str(v1)+" "+str(v3)+" "+str(v4)+"\n")

        # connecting max yaw to yaw 0
        for pitch_deg in range(0, self.max_pitch_deg):
            v1 = 1 + (self.max_yaw_deg * (self.max_pitch_deg + 1) + pitch_deg)
            v2 = 1 + (pitch_deg)
            v3 = 1 + ((pitch_deg + 1))
            v4 = 1 + (self.max_yaw_deg * (self.max_pitch_deg + 1) + (pitch_deg + 1))
            fd.write("f "+str(v1)+" "+str(v2)+" "+str(v3)+"\n")
            fd.write("f "+str(v1)+" "+str(v3)+" "+str(v4)+"\n")

        fd.close()
