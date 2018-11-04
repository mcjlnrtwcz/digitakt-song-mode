from copy import deepcopy
from threading import Thread, Event
from time import perf_counter, sleep

import logging


class Position:

    def __init__(self, pulses):
        self.pulses = pulses % 24
        self.beats = int(pulses / 24) % 4
        self.measures = int(pulses / (24 * 4))

    def __str__(self):
        # This assumes that songs won't be longer than 999 measures
        return f'{str(self.measures).zfill(3)}.{self.beats}.{str(self.pulses).zfill(2)}'


class Pattern:

    def __init__(self, pattern_id, bank_id, length):
        self.pattern_id = pattern_id
        self.bank_id = bank_id
        self.length = length

    def __str__(self):
        return f'{self.bank_id}{self.pattern_id}'


class PatternSequence:

    def __init__(self, pattern, pulsestamp):
        self.pattern = pattern
        self.pulsestamp = pulsestamp

    def __str__(self):
        return f'{self.pattern.bank_id}{self.pattern.pattern_id} @ {Position(self.pulsestamp)}'


class Sequence:
    # TODO: next() returns a Pattern (use repetitions from PatternSequence)

    def __init__(self, tempo, sequence):
        self.tempo = tempo
        self._patterns_blueprint = []
        self._patterns = []

        last_event_pulses = 0

        for index, pattern_sequence in enumerate(sequence):
            pattern = Pattern(
                pattern_sequence['pattern'],
                pattern_sequence['bank'],
                pattern_sequence['length']
            )
            if index != 0:
                last_event_pulses += pattern_sequence['length'] * pattern_sequence['repetitions'] * 24 * 4
            pattern_seq = PatternSequence(pattern, last_event_pulses)
            self._patterns_blueprint.append(pattern_seq)

        self._patterns = deepcopy(self._patterns_blueprint)  # For reset

        self._stop_event = last_event_pulses
        self._stop_event += sequence[-1]['length'] * sequence[-1]['repetitions'] * 24 * 4

    def get_event(self, pulsestamp, force=False):
        # This is a bit stupid and off by one pattern
        # What is the first pattern and how to send it?
        if len(self._patterns) > 0:
            if force:
                return self._patterns.pop(0).pattern
            next_pattern_sequence = self._patterns[0]
            if next_pattern_sequence.pulsestamp - 24 == pulsestamp:  # TODO: Magic number
                return self._patterns.pop(0).pattern
        else:
            if pulsestamp == self._stop_event:
                return 'stop'

    def reset(self):
        self._patterns = deepcopy(self._patterns_blueprint)


class SequencerEngine(Thread):

    def __init__(self, sequence, midi_out):
        super().__init__()
        self._sequence = sequence
        self._midi_out = midi_out
        self._pulsestamp = 0  # In pulses
        self._stop_event = Event()
        self._pulse_duration = 60.0 / self._sequence.tempo / 24.0

    def _pulse(self):
        start = perf_counter()
        while perf_counter() < start + self._pulse_duration:
            sleep(0.0001)

    def run(self):
        logging.info(f'[{self.get_position()}] Sequencer started.')

        # Set first pattern
        event = self._sequence.get_event(self._pulsestamp, force=True)
        self._midi_out.send_message([0xC0, event.pattern_id - 1])  # MIDI messages count from 0, move to midi wrapper
        # TODO; Is sleep below useless since introduction of warm-up?
        sleep(0.25)  # Compensate for Digitakt's lag

        # Warm-up
        for pulse in range(24 * 4):
            self._midi_out.send_message([0xF8])  # Clock
            self._pulse()

        self._midi_out.send_message([0xFA])  # Start
        while not self._stop_event.is_set():
            self._midi_out.send_message([0xF8])  # Clock

            event = self._sequence.get_event(self._pulsestamp)
            if event == 'stop':
                break
            if event:
                """"
                Channel Voice Messages [nnnn = 0-15 (MIDI Channel Number 1-16)]
                1100nnnn 0ppppppp Program Change. This message sent when the patch number changes. (ppppppp) is the new program number.
                """
                self._midi_out.send_message([0xC0, event.pattern_id - 1])
                logging.info(f'[{self.get_position()}] Changing pattern to {event}.')

            self._pulse()
            self._pulsestamp += 1

        self._midi_out.send_message([0xFC])  # Stop
        logging.info(f'[{self.get_position()}] Sequencer stopped.')

        self._sequence.reset()

    def stop(self):
        self._stop_event.set()

    def get_position(self):
        return Position(self._pulsestamp)


class Sequencer:

    def __init__(self, midi_out, sequence=None):
        self._midi_out = midi_out
        self._sequence = sequence
        self._engine = None

    def start(self):
        # TODO: Is port open?
        if self._sequence:
            self._engine = SequencerEngine(self._sequence, self._midi_out)
            self._engine.start()
        else:
            logging.warning('Cannot start sequencer. Sequence is not set.')

    def stop(self):
        if self._engine.is_alive():
            self._engine.stop()
            self._engine.join()
        else:
            logging.warning('Sequencer has already been stopped')

    def get_position(self):
        if self._engine and self._engine.is_alive():
            return str(self._engine.get_position())

    def get_midi_outs(self):
        return self._midi_out.get_ports()

    def set_midi_out(self, midi_out_id):
        if not self._midi_out.is_port_open():
            self._midi_out.open_port(midi_out_id)
        else:
            logging.debug('Selected MIDI port is already opened.')

    def load_sequence(self, sequence_data):
        self._sequence = Sequence(**sequence_data)

    @property
    def is_playing(self):
        if self._engine:
            return self._engine.is_alive()
        return False