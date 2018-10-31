#!/usr/bin/env python3

import os
import json
from tkinter import Tk, Label, Button, StringVar, OptionMenu, Button, filedialog
import tkinter as tk

import rtmidi

from sequencer import Sequencer


class SongModeGUI:

    def __init__(self, root, sequencer):
        self.root = root
        self.sequencer = sequencer

        # Main window

        self.root.geometry('320x160+0+0')
        self.root.title('Digisong')
        root.after(0, self.update_counter)

        # Widgets

        self.counter_label = Label(self.root, text='Counter: -1')
        self.counter_label.grid(row=0, column=0, sticky=tk.W, padx=8)

        self.toggle_seq_btn = Button(
            self.root,
            text='Start/stop',
            command=self.toggle_seq
        )
        self.toggle_seq_btn.grid(row=0, column=1, sticky=tk.E, padx=8)

        # MIDI output selector

        self.midi_out_name = StringVar(self.root)  # TODO: as property?

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

        self.midi_out_choices = self.sequencer.get_midi_outs()
        self.midi_out_selector = OptionMenu(
            self.midi_out_frame,
            self.midi_out_name,
            *self.midi_out_choices
        )
        self.midi_out_selector.grid(row=1, column=0, sticky=tk.W+tk.E)

        # Open sequence

        self.load_btn = Button(
            self.root,
            text='Open sequence',
            command=self.load_file
        )
        self.load_btn.grid(row=2, column=1, sticky=tk.E, padx=8)

        # Configure grid

        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=2)
        self.root.columnconfigure(1, weight=2)

    def update_counter(self):
        if self.sequencer.is_playing:
            self.counter_label.config(
                text=f'Counter: {self.sequencer.get_counter()}'
            )
        else:
            self.counter_label.config(text='Counter: 1.1.1')
        self.counter_label.update()  # TODO
        root.after(42, self.update_counter)

    def load_file(self):
            path = filedialog.askopenfilename(
                initialdir=os.path.dirname(os.path.abspath(__file__)),
                title='Select sequence to load',
                filetypes=(('JSON files', '*.json'), )
            )
            with open(path) as sequence_file:
                # TODO: validate file
                self.sequencer.load_sequence(
                    json.load(sequence_file)['sequence']
                )

    def toggle_seq(self):
        # TODO: Turn on/off update_counter?
        if self.sequencer.is_playing:
            self.sequencer.stop()
        else:
            try:
                port_id = self.midi_out_choices.index(self.midi_out_name.get())
                self.sequencer.set_midi_out(port_id)
                self.sequencer.start()
            except:
                print('midi out name not in midi choices list')


midi_out = rtmidi.MidiOut()
sequencer = Sequencer(midi_out)
root = Tk()
gui = SongModeGUI(root, sequencer)
root.mainloop()
