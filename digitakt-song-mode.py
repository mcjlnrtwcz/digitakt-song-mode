#!/usr/bin/env python3

import json
import logging
import os
import tkinter as tk
from tkinter import filedialog

from diquencer import Sequencer


class SongModeGUI:

    def __init__(self, root, sequencer):
        self.root = root
        self.sequencer = sequencer

        # Main window
        self.root.geometry('320x240+0+0')
        self.root.title('digitakt-song-mode')
        root.after(0, self.refresh_position)

        # Widgets
        self.position_label = tk.Label(
            self.root,
            text='Position: N/A',
            font=('Menlo', '14')
        )
        self.position_label.grid(row=0, column=0, sticky=tk.W, padx=8)

        self.toggle_seq_btn = tk.Button(
            self.root,
            text='Start/stop',
            command=self.toggle_seq
        )
        self.toggle_seq_btn.grid(row=0, column=1, sticky=tk.E, padx=8)

        # MIDI output selector
        self.midi_out_name = tk.StringVar(self.root)

        self.midi_out_frame = tk.Frame(self.root)
        self.midi_out_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=tk.W+tk.E,
            padx=8
        )
        self.midi_out_frame.columnconfigure(0, weight=1)

        self.midi_out_label = tk.Label(self.midi_out_frame, text='MIDI output')
        self.midi_out_label.grid(row=0, column=0, sticky=tk.W)

        self.midi_out_choices = self.sequencer.get_output_ports()
        if self.midi_out_choices:
            self.midi_out_name.set(self.midi_out_choices[0])
        self.midi_out_selector = tk.OptionMenu(
            self.midi_out_frame,
            self.midi_out_name,
            *self.midi_out_choices
        )
        self.midi_out_selector.grid(row=1, column=0, sticky=tk.W+tk.E)

        # MIDI channel selector
        self.midi_channel = tk.IntVar(self.root)

        self.midi_channel_frame = tk.Frame(self.root)
        self.midi_channel_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky=tk.W+tk.E,
            padx=8
        )
        self.midi_channel_frame.columnconfigure(0, weight=1)

        self.midi_channel_label = tk.Label(
            self.midi_channel_frame,
            text='MIDI channel'
        )
        self.midi_channel_label.grid(row=0, column=0, sticky=tk.W)

        self.midi_channel_choices = list(range(1, 17))
        self.midi_channel.set(1)
        self.midi_channel_selector = tk.OptionMenu(
            self.midi_channel_frame,
            self.midi_channel,
            *self.midi_channel_choices
        )
        self.midi_channel_selector.grid(row=1, column=0, sticky=tk.W+tk.E)

        # Open sequence
        self.load_btn = tk.Button(
            self.root,
            text='Open sequence',
            command=self.load_file
        )
        self.load_btn.grid(row=3, column=1, sticky=tk.E, padx=8)

        # Configure grid
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.columnconfigure(0, weight=2)
        self.root.columnconfigure(1, weight=2)

    def refresh_position(self):
        position = self.sequencer.get_position()
        if self.sequencer.is_playing and position:
            self.position_label.config(text=f'Position: {position}')
        else:
            self.position_label.config(text='Position: N/A')
        self.root.after(42, self.refresh_position)

    def load_file(self):
            path = filedialog.askopenfilename(
                initialdir=os.path.dirname(os.path.abspath(__file__)),
                title='Select sequence to load',
                filetypes=(('JSON files', '*.json'), )
            )
            with open(path) as sequence_file:
                self.sequencer.load_sequence(json.load(sequence_file))

    def toggle_seq(self):
        if self.sequencer.is_playing:
            self.sequencer.stop()
        else:
            self.sequencer.set_midi_channel(self.midi_channel.get())
            self.sequencer.set_output_port(self.midi_out_name.get())
            self.sequencer.start()


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s][%(levelname)s] %(message)s',
        level=logging.INFO
    )
    sequencer = Sequencer()
    root = tk.Tk()
    gui = SongModeGUI(root, sequencer)
    root.mainloop()
