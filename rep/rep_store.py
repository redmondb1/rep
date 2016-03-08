import collections

class RepStore(collections.MutableMapping):
    """A dictionary like interface for storing Rep objects"""

    def __init__(self, *args, **kwargs):
        self.__store = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self.__store[key]

    def __setitem__(self, key, value):
        self.__store[key] = value

    def __delitem__(self, key):
        del self.__store[key]

    def __iter__(self):
        return iter(self.__store)

    def __len__(self):
        return len(self.__store)

    def get_new_key(self):
        return max(self.__store.keys(), key=int) + 1 if len(self.__store) else 1

    def create(self, value):
        new_key = self.get_new_key()
        self.__setitem__(new_key, value)
        return new_key

    def read(self, key):
        return self.__getitem__(key)

    def update(self, *args, **kwargs):
        for key, value in dict(*args, **kwargs).iteritems():
            self.__store[key] = value

    def delete(self, key):
        self.__delitem__(key)

    def as_dict(self):
        return {key: value.as_dict() for key, value in self.__store.iteritems()}
