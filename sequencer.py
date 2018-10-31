from copy import deepcopy
from threading import Thread, Event
from time import perf_counter, sleep


class Pattern:

    def __init__(self, pattern_id, bank_id, length):
        self.pattern_id = pattern_id
        self.bank_id = bank_id
        self.length = length


class PatternSequence:

    def __init__(self, pattern, timestamp):
        self.pattern = pattern
        self.timestamp = timestamp

    def __str__(self):
        return f'{self.pattern.bank_id}{self.pattern.pattern_id} on {self.timestamp}'


class Counter:

    def __init__(self):
        self.measures = 1  # TODO: readonly?
        self.beats = 1  # TODO: readonly?
        self.pulses = 1  # TODO: readonly?

    def __eq__(self, other):
        return (self.measures == other.measures
            and self.beats == other.beats
            and self.pulses == other.pulses)

    def __str__(self):
        return f'{self.measures}.{self.beats}.{self.pulses}'

    def increment(self):
        if self.pulses < 24:
            self.pulses += 1
        else:
            self.pulses = 1
            if self.beats < 4:
                self.beats += 1
            else:
                self.beats = 1
                self.measures +=1


class Sequence:
    # TODO: next() returns a Pattern (use repetitions from PatternSequence)

    def __init__(self, tempo, raw_sequence):
        self.tempo = tempo  # TODO: From file?
        self._patterns_blueprint = []
        self._patterns = []

        last_event = Counter()
        for index, element in enumerate(raw_sequence):
            pattern = Pattern(element['pattern'], element['bank'], element['length'])
            if index != 0:
                last_event.measures += element['length'] * element['repetitions']
            pattern_seq = PatternSequence(pattern, deepcopy(last_event))  # Or have Counter in PatternSequence created already and only update it?
            self._patterns_blueprint.append(pattern_seq)
        self._patterns = deepcopy(self._patterns_blueprint)
        self._stop_event = deepcopy(last_event)
        self._stop_event.measures += raw_sequence[-1]['length'] * raw_sequence[-1]['repetitions']

    def get_event(self, counter, force=False):
        # This is a bit stupid and off by one pattern
        # What is the first pattern and how to send it?
        if len(self._patterns) > 0:
            if force:
                return self._patterns.pop(0).pattern
            elem = self._patterns[0]
            temp_count = deepcopy(counter)
            for i in range(24):
                temp_count.increment()
            if elem.timestamp == temp_count:
                print(temp_count)
                return self._patterns.pop(0).pattern
        else:
            if counter == self._stop_event:
                return 'stop'

    def reset(self):
        self._patterns = deepcopy(self._patterns_blueprint)


class SequencerEngine(Thread):

    def __init__(self, sequence, midi_out):
        super().__init__()
        self._sequence = sequence
        self._midi_out = midi_out
        self.counter = Counter()
        self._stop_event = Event()
        self._pulse_duration = 60.0 / self._sequence.tempo / 24.0

    def _pulse(self):
        start = perf_counter()
        while perf_counter() < start + self._pulse_duration:
            sleep(0.0001)

    def run(self):
        # Set first pattern
        event = self._sequence.get_event(self.counter, force=True)
        self._midi_out.send_message([0xC0, event.pattern_id - 1])  # MIDI messages count from 0, move to midi wrapper
        sleep(0.25)  # Compensate for Digitakt's lag

        self._midi_out.send_message([0xFA])  # Start
        while not self._stop_event.is_set():
            self._midi_out.send_message([0xF8])  # Clock

            event = self._sequence.get_event(self.counter)
            if event == 'stop':
                print('fertig')
                break
            if event:
                # Change pattern or whatever
                # Channel 16 or 14
                # Channel Voice Messages [nnnn = 0-15 (MIDI Channel Number 1-16)] 
                # 1100nnnn	0ppppppp	Program Change. This message sent when the patch number changes. (ppppppp) is the new program number.
                self._midi_out.send_message([0xC0, event.pattern_id - 1])
                print(event.pattern_id)

            self._pulse()
            self.counter.increment()
        self._midi_out.send_message([0xFC])  # Stop

    def stop(self):
        self._stop_event.set()
        self._sequence.reset()


class Sequencer:

    def __init__(self, midi_out, sequence=None):
        self._midi_out = midi_out
        self._sequence = sequence
        self.is_playing = False  # TODO: read only
        self._engine = None

    def start(self):
        # TODO: Is port open?
        if self._sequence:
            self._engine = SequencerEngine(self._sequence, self._midi_out)
            self._engine.start()
            self.is_playing = True
        else:
            print('sequence is not set')

    def stop(self):
        if self._engine:
            self._engine.stop()
            self._engine.join()
        self._engine = None
        self._midi_out.close_port()
        self.is_playing = False

    def get_counter(self):
        if self._engine and self._engine.isAlive():
            return str(self._engine.counter)

    def get_midi_outs(self):
        return self._midi_out.get_ports()

    def set_midi_out(self, midi_out_id):
        # TODO: Does that out really exists? GUI should update the list
        # TODO: Check if port changed and then open it again???
        if not self._midi_out.is_port_open():
            self._midi_out.open_port(midi_out_id)
        else:
            print('port already opened')

    def load_sequence(self, sequence):
        self._sequence = Sequence(135, sequence)