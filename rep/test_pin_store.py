"""unittest and doc for PinStore, dictionary like Pin storage class"""

from unittest import TestCase

from . import (
    Pin,
    PinStore,
)

class PinStoreTest(TestCase):
    """The PinStorage class provides a dictionary like interface PinStorage.
    This implementation uses a dictionary for storage for testing, but should
    be extended to support persistent storage. This class adds a CRUD interface
    and keys are generated using an internal algorithm.
    """
    def setUp(self):
        self.pin_store = PinStore()

    def test_setitem_getitem(self):
        """Pin can be set and read using standard dictionary bracket
        notation.
        """
        new_key = self.pin_store.get_new_key()
        self.pin_store[new_key] = Pin('key1', 'key2')
        self.assertEquals(self.pin_store[new_key].parent, 'key1')
        self.assertEquals(self.pin_store[new_key].child, 'key2')

    def test_delitem(self):
        """The del function removes the key like a dictionary."""
        key = self.pin_store.create(Pin('key1', 'key2'))
        del self.pin_store[key]
        with self.assertRaises(KeyError):
            self.pin_store[key]

    def test_iter(self):
        """The PinStore can be iterated the same as a dictionary."""
        pins = {}
        for parent in range(2):
            pins[self.pin_store.create(Pin(parent, parent*2))] = parent
        for key, value in self.pin_store.iteritems():
            self.assertEquals(value.parent, pins[key])

    def test_len(self):
        """The builtin len function works with PinStores."""
        for _ in range(10):
            self.pin_store.create(Pin(1, 2))
        self.assertEquals(len(self.pin_store), 10)

    def test_create(self):
        """The create method assigns a new internally generated key and stores
        the Pin using the new key.  The return value is the new key.
        """
        key = self.pin_store.create(Pin('key1', 'key2'))
        self.assertEquals(self.pin_store[key].parent, 'key1')
        self.assertEquals(self.pin_store[key].child, 'key2')

    def test_read(self):
        """The read method works the same as dictionary bracket notation."""
        key = self.pin_store.create(Pin('key1', 'key2'))
        self.assertEquals(self.pin_store.read(key).parent, 'key1')
        self.assertEquals(self.pin_store.read(key).child, 'key2')

    def test_update(self):
        """The update method works the same as the dictionary method."""
        key = self.pin_store.create(Pin('key1', 'key2'))
        self.pin_store.update({key: Pin('key3', 'key4')})
        self.assertEquals(self.pin_store.read(key).parent, 'key3')
        self.assertEquals(self.pin_store.read(key).child, 'key4')

    def test_delete(self):
        """The delete method removes the key like a dictionary."""
        key = self.pin_store.create(Pin('key1', 'key2'))
        self.pin_store.delete(key)
        with self.assertRaises(KeyError):
            self.pin_store.read(key)

    def test_as_dict(self):
        """The as_dict method returns the store as a dictionary."""
        key = self.pin_store.create(Pin('key1', 'key2'))
        self.assertEquals(self.pin_store.as_dict()[key]['parent'], 'key1')
        self.assertEquals(self.pin_store.as_dict()[key]['child'], 'key2')

    def test_get_children_str(self):
        """The get_children method returns a list of pin keys where the parent
        matches the key argument."""
        key = self.pin_store.create(Pin('key1', 'key2'))
        self.assertEquals(self.pin_store.get_children('key1'),
                          [self.pin_store[key].child])

    def test_get_children_int(self):
        """The get_children method returns a list of pin keys where the parent
        matches the key argument."""
        key = self.pin_store.create(Pin(1, 2))
        self.assertEquals(self.pin_store.get_children(1),
                          [self.pin_store[key].child])

