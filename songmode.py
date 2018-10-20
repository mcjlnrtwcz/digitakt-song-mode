#!/usr/bin/env python3

import os
import json
from tkinter import Tk, Label, Button, StringVar, OptionMenu, Button, filedialog

import rtmidi

from sequencer import Sequencer


class SongModeGUI:

    def __init__(self, root, sequencer):
        self.root = root
        self.sequencer = sequencer

        # Main window

        self.root.geometry('320x240+0+0')
        self.root.title('Digitakt song mode')
        root.after(0, self.update_counter)

        # Widgets

        self.counter_label = Label(self.root, text='Counter: -1')
        self.counter_label.pack()

        self.midi_out_name = StringVar(self.root)  # TODO: as property?
        self.midi_out_choices = self.sequencer.get_midi_outs()
        self.midi_out_selector = OptionMenu(
            self.root,
            self.midi_out_name,
            *self.midi_out_choices
        )
        self.midi_out_selector.pack()

        self.load_btn = Button(self.root, text='Load', command=self.load_file)
        self.load_btn.pack()

        self.toggle_seq_btn = Button(
            self.root,
            text='Start/stop',
            command=self.toggle_seq
        )
        self.toggle_seq_btn.pack()

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

"""
TODO:
 - block midi out option menu when running
 - block bpm when running
 - quantized stop - finish on measure (or configurable in the future)
 - processing instead of threading
 - midi wrapper
 - comparison between counters (counterdelta?)
 - previous/current/next pattern label
 - tempo from JSON
 - create event class, PatternSequence is an Event, and there's Stop event
"""