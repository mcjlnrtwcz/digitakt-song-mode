import tkinter as tk

from .midi import MIDIFrame
from .pattern import PatternFrame
from .transport import TransportFrame


class SongModeView(tk.Tk):
    def __init__(self, controller, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.controller = controller

        # Main window settings
        self.config(padx=8, pady=4)
        self.title("digitakt-song-mode")
        self.resizable(False, False)

        # Transport
        self.transport_frame = TransportFrame(controller, self)
        self.transport_frame.grid(row=0, sticky=tk.W + tk.E)
        self.transport_frame.columnconfigure(0, weight=1)
        self.after(0, self.transport_frame.refresh)

        # Pattern
        self.pattern_frame = PatternFrame(controller, self)
        self.pattern_frame.grid(row=1, sticky=tk.W + tk.E)
        self.pattern_frame.columnconfigure(0, weight=1)
        self.after(0, self.pattern_frame.refresh)

        # MIDI
        self.midi_frame = MIDIFrame(controller, self)
        self.midi_frame.grid(row=2, sticky=tk.W + tk.E)
        self.midi_frame.columnconfigure(0, weight=1)

        # Configure grid
        _, row_count = self.grid_size()
        for row_idx in range(row_count):
            self.rowconfigure(row_idx, pad=12)
