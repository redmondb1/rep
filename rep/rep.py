import re

class Rep(object):
    """Rep is the basic core class in rep. It's a simple, generic
    representation. Unlike a traditional file system, the fields of this
    class do not track details about the system such as access time or size
    in bytes. That kind of information is kept separately.
    """
    fields = ['title']

    """Each field can have a regular expression to describe legal values
    for fields.  These are checked when setting the fields and a
    ValueError is raised if the expression doesn't match.
    """
    format = {
        'title': re.compile(r"^\S(.{0,248}\S)?$"),
    }

    def __init__(self, from_dict=None, **kwargs):
        if from_dict is not None:
            self.from_dict(from_dict)
        else:
            self.from_dict(kwargs)

    def as_dict(self):
        """Return the fields required to recreate this rep. Can be fed back to
        from_dict method.
        """
        return {field: getattr(self, field) for field in self.fields}

    def from_dict(self, data):
        """Set fields based on dictionary.
        """
        for field in data:
            if field in self.fields:
                setattr(self, field, data[field])
            else:
                raise AttributeError("%s is not a valid field" % field)
        return self

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        if title is None or self.format['title'].match(str(title)) is None:
            raise ValueError("%s is not a valid title" % title)
        else:
            self.__title = str(title)
