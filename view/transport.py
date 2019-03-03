import tkinter as tk


class TransportFrame(tk.Frame):
    def __init__(self, controller, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller

        self.position_label = tk.Label(self, text="Position: N/A", font=(None, "16"))
        self.position_label.grid(row=0, sticky=tk.W)
        self.toggle_seq_btn = tk.Button(
            self, text="Start/stop", command=self.controller.toggle_seq
        )
        self.toggle_seq_btn.grid(row=0, column=1, sticky=tk.E)
        self.columnconfigure(0, minsize=256)

    def refresh(self):
        self.position_label.config(text=f"Position: {self.controller.position}")
        self.after(42, self.refresh)
