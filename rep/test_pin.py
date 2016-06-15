"""unittest and doc for Pin, relational class in the rep system"""
from unittest import TestCase

from . import Pin

class PinTest(TestCase):
    """A Pin expresses a parent-child relationship between two Reps.
    """
    def setUp(self):
        self.pin = Pin('key1', 'key2')

    def test_pin_parent(self):
        """A Pin stores two Rep keys.
        """
        self.assertEquals(self.pin.parent, 'key1')

    def test_pin_child(self):
        """A Pin stores two Rep keys.
        """
        self.assertEquals(self.pin.child, 'key2')
