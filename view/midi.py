import logging
import tkinter as tk

from diquencer.exceptions import MIDIOutputError

from .utils import display_alert


class MIDIFrame(tk.Frame):
    def __init__(self, controller, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Output selector
        self.output_selector = OutputSelector(controller, self)
        self.output_selector.grid(row=0, sticky=tk.W + tk.E)
        self.output_selector.columnconfigure(0, weight=1)

        # Channel selector
        self.channel_selector = ChannelSelector(controller, self)
        self.channel_selector.grid(row=1, sticky=tk.W + tk.E)
        self.channel_selector.columnconfigure(0, weight=1)


class Selector(tk.Frame):
    def __init__(self, title, choices, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.choice_var = tk.StringVar(self)
        if choices:
            self.choice_var.set(choices[0])
            self.option_command(self.choice_var.get())

        self.title = tk.Label(self, text=title)
        self.title.grid(row=0, sticky=tk.W)

        self.selector = tk.OptionMenu(
            self, self.choice_var, *choices, command=self.option_command
        )
        self.selector.grid(row=1, sticky=tk.W + tk.E)

    def option_command(self, new_value):
        raise NotImplementedError


class OutputSelector(Selector):
    def __init__(self, controller, parent, *args, **kwargs):
        self.controller = controller
        super().__init__(
            "MIDI output:", controller.output_ports, parent, *args, **kwargs
        )

    def option_command(self, new_value):
        try:
            self.controller.set_output_port(new_value)
        except MIDIOutputError as error:
            logging.debug(error)
            display_alert("Cannot open MIDI output port.")


class ChannelSelector(Selector):
    def __init__(self, controller, parent, *args, **kwargs):
        self.controller = controller
        super().__init__("MIDI channel:", list(range(1, 17)), parent, *args, **kwargs)

    def option_command(self, new_value):
        self.controller.set_output_channel(int(new_value))
