#!/usr/bin/env python3

import json
import logging
import os
import tkinter as tk
from tkinter import filedialog

from diquencer import Sequencer


class OutputSelector(tk.Frame):

    def __init__(self, choices, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self._output = tk.StringVar(self)
        self.title = tk.Label(self, text='MIDI output')
        self.title.grid(row=0, sticky=tk.W)
        if choices:
            self._output.set(choices[0])
        self.selector = tk.OptionMenu(self, self._output, *choices)
        self.selector.grid(row=1, sticky=tk.W+tk.E)

    @property
    def output(self):
        return self._output.get()


class ChannelSelector(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self._channel = tk.IntVar(self)
        self.title = tk.Label(self, text='MIDI channel')
        self.title.grid(row=0, sticky=tk.W)
        self._channel.set(1)
        self.selector = tk.OptionMenu(self, self._channel, *list(range(1, 17)))
        self.selector.grid(row=1, sticky=tk.W+tk.E)

    @property
    def channel(self):
        return self._channel.get()


class SongModeGUI(tk.Tk):

    def __init__(self, sequencer, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.sequencer = sequencer

        # Main window
        self.geometry('320x240+0+0')
        self.title('digitakt-song-mode')
        self.after(0, self.refresh_position)

        # Widgets
        self.position_label = tk.Label(
            self,
            text='Position: N/A',
            font=('Menlo', '14')
        )
        self.position_label.grid(row=0, sticky=tk.W, padx=8)

        self.toggle_seq_btn = tk.Button(
            self,
            text='Start/stop',
            command=self.toggle_seq
        )
        self.toggle_seq_btn.grid(row=0, column=1, sticky=tk.E, padx=8)

        # MIDI output selector
        self.output_selector = OutputSelector(
            self.sequencer.get_output_ports(),
            self
        )
        self.output_selector.grid(
            row=1,
            columnspan=2,
            sticky=tk.W+tk.E,
            padx=8
        )
        self.output_selector.columnconfigure(0, weight=1)

        # MIDI channel selector
        self.channel_selector = ChannelSelector(self)
        self.channel_selector.grid(
            row=2,
            columnspan=2,
            sticky=tk.W+tk.E,
            padx=8
        )
        self.channel_selector.columnconfigure(0, weight=1)

        # Open sequence
        self.load_btn = tk.Button(
            self,
            text='Open sequence',
            command=self.load_file
        )
        self.load_btn.grid(row=3, column=1, sticky=tk.E, padx=8)

        # Configure grid
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=2)

    def refresh_position(self):
        position = self.sequencer.get_position()
        if self.sequencer.is_playing and position:
            self.position_label.config(text=f'Position: {position}')
        else:
            self.position_label.config(text='Position: N/A')
        self.after(42, self.refresh_position)

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
            self.sequencer.set_midi_channel(self.channel_selector.channel)
            self.sequencer.set_output_port(self.output_selector.output)
            self.sequencer.start()


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s][%(levelname)s] %(message)s',
        level=logging.INFO
    )
    sequencer = Sequencer()
    gui = SongModeGUI(sequencer)
    gui.mainloop()
