import json

from diquencer import Sequencer


class SongModeController:
    def __init__(self):
        self._sequencer = Sequencer()

    @property
    def position(self):
        return self._sequencer.position or "N/A"

    @property
    def output_ports(self):
        return self._sequencer.output_ports

    @property
    def current_pattern(self):
        return self._sequencer.current_pattern or "N/A"

    @property
    def patterns(self):
        if self._sequencer.patterns:
            return [pattern.name for pattern in self._sequencer.patterns]
        return ["N/A"]

    @property
    def next_pattern(self):
        return self._sequencer.next_pattern or "N/A"

    def load(self, sequence_path):
        with open(sequence_path) as sequence_file:
            self._sequencer.load_sequence(json.load(sequence_file))

    def set_output_channel(self, channel):
        self._sequencer.set_midi_channel(channel)

    def set_output_port(self, output_port):
        self._sequencer.set_output_port(output_port)

    def set_start_pattern(self, start_pattern_idx):
        self._sequencer.set_start_pattern(start_pattern_idx)

    def toggle_seq(self):
        if self._sequencer.is_playing:
            self._sequencer.stop()
        else:
            self._sequencer.start()
