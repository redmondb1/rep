"""unittest and doc for RepStore, dictionary like Rep storage class"""

from unittest import TestCase

from . import Rep, RepStore

class RepStoreTest(TestCase):
    """The RepStore class provides a dictionary like interface RepStorage.
    This implementation uses a dictionary for storage for testing, but should
    be extended to support persistent storage. This class adds a CRUD interface
    and keys are generated using an internal algorithm.
    """
    def setUp(self):
        self.rep_store = RepStore()

    def test_setitem_getitem(self):
        """Rep can be set and read using standard dictionary bracket
        notation.
        """
        new_key = self.rep_store.get_new_key()
        self.rep_store[new_key] = Rep(title="get item test")
        self.assertEquals(self.rep_store[new_key].title, "get item test")

    def test_delitem(self):
        """The del function removes the key like a dictionary."""
        key = self.rep_store.create(Rep(title="delitem test"))
        del self.rep_store[key]
        with self.assertRaises(KeyError):
            self.rep_store[key]

    def test_iter(self):
        """The RepStore can be iterated the same as a dictionary."""
        titles = {}
        for title in range(2):
            titles[self.rep_store.create(Rep(title=title))] = str(title)
        for key, value in self.rep_store.iteritems():
            self.assertEquals(value.title, titles[key])

    def test_len(self):
        """The builtin len function works with RepStores."""
        for _ in range(10):
            self.rep_store.create(Rep(title="item"))
        self.assertEquals(len(self.rep_store), 10)

    def test_create(self):
        """The create method assigns a new internally generated key and stores
        the Rep using the new key.  The return value is the new key.
        """
        key = self.rep_store.create(Rep(title="create test"))
        self.assertEquals(self.rep_store[key].title, "create test")

    def test_read(self):
        """The read method works the same as dictionary bracket notation."""
        key = self.rep_store.create(Rep(title="read test"))
        self.assertEquals(self.rep_store.read(key).title, "read test")

    def test_update(self):
        """The update method works the same as the dictionary method."""
        key = self.rep_store.create(Rep(title="initial update test"))
        self.rep_store.update({key: Rep(title="updated update test")})
        self.assertEquals(self.rep_store.read(key).title, "updated update test")

    def test_delete(self):
        """The delete method removes the key like a dictionary."""
        key = self.rep_store.create(Rep(title="initial update test"))
        self.rep_store.delete(key)
        with self.assertRaises(KeyError):
            self.rep_store.read(key)

    def test_as_dict(self):
        """The as_dict method returns the store as a dictionary."""
        key = self.rep_store.create(Rep(title="as_dict test"))
        self.assertEquals(self.rep_store.as_dict()[key]['title'], "as_dict test")
