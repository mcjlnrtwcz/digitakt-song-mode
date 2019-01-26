import json

from diquencer import Sequencer


class SongModeController:

    def __init__(self):
        self.sequencer = Sequencer()

    @property
    def position(self):
        return self.sequencer.get_position() or 'N/A'

    @property
    def output_ports(self):
        return self.sequencer.get_output_ports()

    def load(self, sequence_path):
        with open(sequence_path) as sequence_file:
                self.sequencer.load_sequence(json.load(sequence_file))

    def set_output_channel(self, channel):
        self.sequencer.set_midi_channel(channel)

    def set_output_port(self, output_port):
        self.sequencer.set_output_port(output_port)

    def toggle_seq(self):
        if self.sequencer.is_playing:
            self.sequencer.stop()
        else:
            self.sequencer.start()
