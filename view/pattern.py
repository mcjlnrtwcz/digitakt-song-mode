import logging
import os
import tkinter as tk
from tkinter import filedialog

from diquencer.exceptions import SequencerTransportError

from .utils import display_alert


class PatternFrame(tk.Frame):
    def __init__(self, controller, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller

        self.current_pattern_fmt = "Current pattern: {}"
        self.next_pattern_fmt = "Next pattern: {}"

        self.load_btn = tk.Button(
            self, text="Open sequence", command=self.open_sequence
        )
        self.load_btn.grid(row=0, sticky=tk.W, pady=(0, 8))

        self.pattern_selector = PatternSelector(controller, self)
        self.pattern_selector.grid(row=1, sticky=tk.W + tk.E)
        self.pattern_selector.columnconfigure(0, weight=1)

        self.current_label = tk.Label(
            self, text=self.current_pattern_fmt.format("N/A"), pady=4
        )
        self.current_label.grid(row=2, sticky=tk.W)

        self.next_label = tk.Label(
            self, text=self.next_pattern_fmt.format("N/A"), pady=4
        )
        self.next_label.grid(row=3, sticky=tk.W)

    def open_sequence(self):
        path = filedialog.askopenfilename(
            initialdir=os.path.dirname(os.path.abspath(__file__)),
            title="Select sequence to open",
            filetypes=(("JSON files", "*.json"),),
        )
        if not path:
            return
        try:
            self.controller.load(path)
            self.reload_patterns()
        except SequencerTransportError as error:
            display_alert(error)

    def reload_patterns(self):
        self.pattern_selector.reload_patterns()

    def refresh(self):
        self.current_label.config(
            text=self.current_pattern_fmt.format(self.controller.current_pattern)
        )
        self.next_label.config(
            text=self.next_pattern_fmt.format(self.controller.next_pattern)
        )
        self.after(42, self.refresh)


class PatternSelector(tk.Frame):
    def __init__(self, controller, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller

        self.start_pattern = tk.StringVar(self)
        choices = self.controller.patterns
        self.start_pattern.set(choices[0])

        self.title = tk.Label(self, text="Start pattern:")
        self.title.grid(row=0, sticky=tk.W)

        self.selector = tk.OptionMenu(self, self.start_pattern, *choices)
        self.selector.grid(row=1, sticky=tk.W + tk.E)

    def set_start_pattern(self, start_pattern_idx, start_pattern_name):
        try:
            self.controller.set_start_pattern(start_pattern_idx)
        except SequencerTransportError as error:
            logging.debug(error)
            display_alert("Cannot change start pattern while sequencer is running.")
        else:
            self.start_pattern.set(start_pattern_name)

    def reload_patterns(self):
        menu = self.selector["menu"]
        menu.delete(0, "end")
        for pattern_idx, pattern in enumerate(self.controller.patterns):
            menu.add_command(
                label=pattern,
                command=lambda idx=pattern_idx, choice=pattern: self.set_start_pattern(
                    idx, choice
                ),
            )
        self.start_pattern.set(self.controller.patterns[0])
