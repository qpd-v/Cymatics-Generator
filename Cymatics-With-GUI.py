import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import multiprocessing

def generate_wave(size, freq, phase_shift, time, x, y):
    dist = np.sqrt((x - size / 2) ** 2 + (y - size / 2) ** 2)
    return np.sin(2 * np.pi * freq * (dist - time % (1 / freq)) + phase_shift)

def generate_waves(n_waves, size, freqs, phase_shifts, time):
    waves = np.zeros((size, size))
    for i in range(n_waves):
        wave = np.zeros((size, size))
        for x in range(size):
            for y in range(size):
                wave[x][y] = generate_wave(size, freqs[i], phase_shifts[i], time, x, y)
        waves += wave
    return waves

def save_frame(frame, n_waves, size, freqs, phase_shifts, path):
    time = frame / 60
    fig, ax = plt.subplots()
    ax.imshow(generate_waves(n_waves, size, freqs, phase_shifts, time), cmap='gray')
    ax.axis('off')
    fig.savefig(os.path.join(path, 'frame_{0:03d}.png'.format(frame)))
    plt.close(fig)

class WaveGenerator(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Cymatics Generator")

        self.n_waves_var = tk.IntVar()
        self.n_waves_var.set(10)
        self.size_var = tk.IntVar()
        self.size_var.set(512)
        self.freqs_var = []
        self.phase_shifts_var = []
        self.path_var = tk.StringVar()

        n_waves_label = tk.Label(self, text="Number of Waves:")
        n_waves_entry = tk.Entry(self, textvariable=self.n_waves_var)
        size_label = tk.Label(self, text="Size:")
        size_entry = tk.Entry(self, textvariable=self.size_var)
        self.freq_labels = []
        self.freq_entries = []
        self.phase_shift_labels = []
        self.phase_shift_entries = []
        path_label = tk.Label(self, text="Path:")
        path_entry = tk.Entry(self, textvariable=self.path_var)
        path_button = tk.Button(self, text="Browse", command=self.browse_path)
        generate_button = tk.Button(self, text="Generate", command=self.generate)
        stop_button = tk.Button(self, text="Stop", command=self.stop)
        self.progress = ttk.Progressbar(self, orient='horizontal', length=200, mode='determinate')
        self.stop_flag = multiprocessing.Value('i', 0)

        n_waves_label.grid(row=0, column=0, sticky='W')
        n_waves_entry.grid(row=0, column=1)
        size_label.grid(row=1, column=0, sticky='W')
        size_entry.grid(row=1, column=1)

        for i in range(self.n_waves_var.get()):
            self.freqs_var.append(tk.DoubleVar())
            self.phase_shifts_var.append(tk.DoubleVar())
            freq_label = tk.Label(self, text="Frequency {}:".format(i + 1))
            freq_entry = tk.Entry(self, textvariable=self.freqs_var[i])
            phase_shift_label = tk.Label(self, text="Phase Shift {}:".format(i + 1))
            phase_shift_entry = tk.Entry(self, textvariable=self.phase_shifts_var[i])
            freq_label.grid(row=2 + i * 2, column=0, sticky='W')
            freq_entry.grid(row=2 + i * 2, column=1)
            phase_shift_label.grid(row=3 + i * 2, column=0, sticky='W')
            phase_shift_entry.grid(row=3 + i * 2, column=1)
            self.freq_labels.append(freq_label)
            self.freq_entries.append(freq_entry)
            self.phase_shift_labels.append(phase_shift_label)
            self.phase_shift_entries.append(phase_shift_entry)

        path_label.grid(row=3 + self.n_waves_var.get() * 2, column=0, sticky='W')
        path_entry.grid(row=3 + self.n_waves_var.get() * 2, column=1)
        path_button.grid(row=3 + self.n_waves_var.get() * 2, column=2)
        self.progress.grid(row=4 + self.n_waves_var.get() * 2, column=0, columnspan=3, pady=10)
        generate_button.grid(row=5 + self.n_waves_var.get() * 2, column=0, pady=10)
        stop_button.grid(row=5 + self.n_waves_var.get() * 2, column=2, pady=10)

    def browse_path(self):
        path = filedialog.askdirectory()
        self.path_var.set(path)

    def stop(self):
        self.stop_flag.value = 1

    def generate(self):
        self.stop_flag.value = 0
        n_waves = self.n_waves_var.get()
        size = self.size_var.get()
        freqs = [var.get() for var in self.freqs_var]
        phase_shifts = [var.get() for var in self.phase_shifts_var]
        path = self.path_var.get()

        if not os.path.exists(path):
            os.makedirs(path)

        self.progress.config(maximum=3600)
        for frame in range(3600):
            if self.stop_flag.value:
                break
            save_frame(frame, n_waves, size, freqs, phase_shifts, path)
            self.progress.step()

    def update_wave_fields(self, *args):
        for i in range(len(self.freq_labels)):
            self.freq_labels[i].grid_forget()
            self.freq_entries[i].grid_forget()
            self.phase_shift_labels[i].grid_forget()
            self.phase_shift_entries[i].grid_forget()
        self.freq_labels.clear()
        self.freq_entries.clear()
        self.phase_shift_labels.clear()
        self.phase_shift_entries.clear()
        self.freqs_var.clear()
        self.phase_shifts_var.clear()
        for i in range(self.n_waves_var.get()):
            self.freqs_var.append(tk.DoubleVar())
            self.phase_shifts_var.append(tk.DoubleVar())
            freq_label = tk.Label(self, text="Frequency {}:".format(i + 1))
            freq_entry = tk.Entry(self, textvariable=self.freqs_var[i])
            phase_shift_label = tk.Label(self, text="Phase Shift {}:".format(i + 1))
            phase_shift_entry = tk.Entry(self, textvariable=self.phase_shifts_var[i])
            freq_label.grid(row=2 + i * 2, column=0, sticky='W')
            freq_entry.grid(row=2 + i * 2, column=1)
            phase_shift_label.grid(row=3 + i * 2, column=0, sticky='W')
            phase_shift_entry.grid(row=3 + i * 2, column=1)
            self.freq_labels.append(freq_label)
            self.freq_entries.append(freq_entry)
            self.phase_shift_labels.append(phase_shift_label)
            self.phase_shift_entries.append(phase_shift_entry)
        self.progress.grid(row=4 + self.n_waves_var.get() * 2, column=0, columnspan=3, pady=10)
        generate_button.grid(row=5 + self.n_waves_var.get() * 2, column=0, pady=10)
        stop_button.grid(row=5 + self.n_waves_var.get() * 2, column=2, pady=10)

def generate_waves(n_waves, size, freqs, phase_shifts, time):
    waves = np.zeros((size, size))
    for i in range(n_waves):
        wave = np.zeros((size, size))
        for x in range(size):
            for y in range(size):
                dist = np.sqrt((x - size / 2) ** 2 + (y - size / 2) ** 2)
                wave[x][y] = np.sin(2 * np.pi * freqs[i] * (dist - time % (1 / freqs[i])) + phase_shifts[i])
        waves += wave
    return waves

def save_frame(frame, n_waves, size, freqs, phase_shifts, path):
    fig, ax = plt.subplots()
    ax.imshow(generate_waves(n_waves, size, freqs, phase_shifts, frame / 60), cmap='gray')
    ax.axis('off')
    fig.savefig(os.path.join(path, 'frame_{0:03d}.png'.format(frame)))
    plt.close(fig)

if __name__ == '__main__':
    app = WaveGenerator()
    app.mainloop()

