from unittest import TestCase

from sequencer import Position


class TestCounter(TestCase):

    def test_pulses_below(self):
        position = Position(47)
        self.assertEqual(position.pulses, 23)
        self.assertEqual(position.beats, 1)
        self.assertEqual(position.measures, 0)

    def test_pulses_zero(self):
        position = Position(48)
        self.assertEqual(position.pulses, 0)
        self.assertEqual(position.beats, 2)
        self.assertEqual(position.measures, 0)

    def test_pulses_above(self):
        position = Position(49)
        self.assertEqual(position.pulses, 1)
        self.assertEqual(position.beats, 2)
        self.assertEqual(position.measures, 0)

    def test_measures(self):
        position = Position(96)
        self.assertEqual(position.pulses, 0)
        self.assertEqual(position.beats, 0)
        self.assertEqual(position.measures, 1)
