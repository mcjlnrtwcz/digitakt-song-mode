import os

import tkinter as tk
from tkinter import filedialog


class TransportControl(tk.Frame):

    def __init__(self, controller, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller
        self.position_label = tk.Label(
            self,
            text='Position: N/A',
            font=(None, '16')
        )
        self.position_label.grid(row=0, sticky=tk.W)
        self.toggle_seq_btn = tk.Button(
            self,
            text='Start/stop',
            command=self.controller.toggle_seq
        )
        self.toggle_seq_btn.grid(row=0, column=1, sticky=tk.E)
        self.columnconfigure(0, minsize=256)

    def refresh_position(self):
        self.position_label.config(
            text=f'Position: {self.controller.position}'
        )
        self.after(42, self.refresh_position)


class OutputSelector(tk.Frame):

    def __init__(self, controller, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller

        self._output = tk.StringVar(self)
        choices = self.controller.output_ports
        if choices:
            self._output.set(choices[0])
            self.set_output_port(self._output.get())

        self.title = tk.Label(self, text='MIDI output')
        self.title.grid(row=0, sticky=tk.W)
        self.selector = tk.OptionMenu(
            self,
            self._output,
            *choices,
            command=self.set_output_port
        )
        self.selector.grid(row=1, sticky=tk.W+tk.E)

    def set_output_port(self, port):
        self.controller.set_output_port(port)


class ChannelSelector(tk.Frame):

    def __init__(self, controller, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller

        self._channel = tk.IntVar(self)
        self._channel.set(1)
        self.controller.set_output_channel(self._channel.get())

        self.title = tk.Label(self, text='MIDI channel')
        self.title.grid(row=0, sticky=tk.W)
        self.selector = tk.OptionMenu(
            self,
            self._channel,
            *list(range(1, 17)),
            command=self.set_output_channel
        )
        self.selector.grid(row=1, sticky=tk.W+tk.E)

    def set_output_channel(self, channel):
        self.controller.set_output_channel(channel)


class SongModeView(tk.Tk):

    def __init__(self, controller, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.controller = controller

        # Main window settings
        self.config(padx=8, pady=4)
        self.title('digitakt-song-mode')

        # Transport control
        self.transport_control = TransportControl(controller, self)
        self.transport_control.grid(row=0, sticky=tk.W+tk.E)
        self.transport_control.columnconfigure(0, weight=1)
        self.after(0, self.transport_control.refresh_position)

        # MIDI output selector
        self.output_selector = OutputSelector(
            self.controller,
            self
        )
        self.output_selector.grid(row=1, sticky=tk.W+tk.E)
        self.output_selector.columnconfigure(0, weight=1)

        # MIDI channel selector
        self.channel_selector = ChannelSelector(controller, self)
        self.channel_selector.grid(row=2, sticky=tk.W+tk.E)
        self.channel_selector.columnconfigure(0, weight=1)

        # Open sequence
        self.load_btn = tk.Button(
            self,
            text='Open sequence',
            command=self.open_sequence
        )
        self.load_btn.grid(row=3, sticky=tk.E)

        # Configure grid
        _, row_count = self.grid_size()
        for row_idx in range(row_count):
            self.rowconfigure(row_idx, pad=12)

    def open_sequence(self):
        path = filedialog.askopenfilename(
            initialdir=os.path.dirname(os.path.abspath(__file__)),
            title='Select sequence to open',
            filetypes=(('JSON files', '*.json'), )
        )
        if path:
            self.controller.load(path)
