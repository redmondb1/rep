class Pin(object):
    """Pin contains a parent-child relationship between two Reps.
    """

    def __init__(self, parent, child):
        self.parent = parent
        self.child = child

    def as_dict(self):
        """Return the fields required to recreate this pin. Can be fed back to
        from_dict method.
        """
        return {'parent': self.parent, 'child': self.child}

    def from_dict(self, data):
        """Set fields based on dictionary.
        """
        fields = ['parent', 'child']

        for field in data:
            if field in fields:
                setattr(self, field, data[field])
            else:
                raise AttributeError("%s is not a valid field" % field)
        return self

