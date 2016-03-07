"""unittest and doc for Rep, core class in the rep system"""
from unittest import TestCase

from unittest_data_provider import data_provider

from . import Rep

class RepTest(TestCase):
    """The rep approach to organizing data is modeled on how humans organize
    data more than how computers do.
    """
    @data_provider(lambda: [[x] for x in ('a', 'bc', 'd'*250, 'e f', 'Ghi JK')])
    def test_valid_titles(self, title):
        """Every Rep has a descriptive title string of 250 characters or less."""
        self.assertEquals(Rep(title=title).title, title)

    @data_provider(lambda: [[x] for x in ('z'*251, 'way too long'*1000)])
    def test_title_too_long(self, title):
        """Titles cannot be longer than 250 characters."""
        with self.assertRaises(ValueError):
            Rep(title=title)

    @data_provider(lambda: [[x] for x in (None, "", " ", " "*100, " "*1000,
                                          "\n", "\t", "\t\n")])
    def test_blank_titles_not_allowed(self, title):
        """Blank titles are not allowed."""
        with self.assertRaises(ValueError):
            Rep(title=title)

    @data_provider(lambda: [[x] for x in (0, 0.0, 1, 999.9, '999', object)])
    def test_titles_are_always_strings(self, title):
        """Titles are always cast to strings."""
        self.assertEquals(Rep(title=title).title, str(title))

    def test_multiline_titles_are_not_allowed(self):
        """Multiline titles are not allowed."""
        with self.assertRaises(ValueError):
            Rep(title="Multiline titles\nare not allowed.")

    @data_provider(lambda: [[x] for x in (" begin", "end ", " both ", "\ttabstart", "tabend\t\t")])
    def test_titles_cannot_start_or_end_with_whitespace(self, title):
        """Titles cannot start or end with whitespace"""
        with self.assertRaises(ValueError):
            Rep(title=title)

    @data_provider(lambda: [[x] for x in ('titlez', 'buttonz')])
    def test_invalid_fields(self, field):
        """Only attributes listed in the self.fields list are valid."""
        with self.assertRaises(AttributeError):
            Rep(**{field: 'title'})

    def test_as_dict(self):
        """Reps can be converted to dicts using self.as_dict()."""
        rep_dict = Rep(title="as dict test").as_dict()
        for field in Rep().fields:
            self.assertIn(field, rep_dict)

    def test_from_dict_init(self):
        """Reps can be created from dicts using from_dict in the init."""
        self.assertEquals("from dict init test",
                          Rep(from_dict={'title': "from dict init test"}).title)

    def test_from_dict_method(self):
        """Reps can also be created from dicts using the from_dict method."""
        self.assertEquals("from dict method test",
                          Rep().from_dict({'title': "from dict method test"}).title)
