import json
from unittest import TestCase

import rest_app

class PinRestAppTest(TestCase):
    PIN_URL = '/rep/api/v1.0/pins'

    def get_pin(self, key):
        """ Helper function to get a specific Pin.
        """
        return self.app.get('%s/%s' % (self.PIN_URL, key))

    def post_pin(self, pin):
        """ Helper function to post a new Pin to the PinStore.
        """
        return self.app.post(self.PIN_URL, data=json.dumps(pin),
                             content_type='application/json', follow_redirects=True)

    def delete_pin(self, key):
        """ Helper function to delete a Pin from the PinStore.
        """
        return self.app.delete('%s/%s' % (self.PIN_URL, key))

    def put_pin(self, key, pin):
        """ Helper function to update a Pin.
        """
        return self.app.put('%s/%s' % (self.PIN_URL, key), data=json.dumps(pin),
                            content_type='application/json')

    def setUp(self):
        """ Start each test with a new test Pin.
        """
        rest_app.app.config['TESTING'] = True
        self.app = rest_app.app.test_client()
        response = self.post_pin({'parent' : 1, 'child' : 2})
        self.test_key = response.location.rsplit('/', 1)[-1]
        self.test_pin = json.loads(self.get_pin(self.test_key).data)

    def tearDown(self):
        """ Delete the test Pin at the end of each test.
        """
        self.delete_pin(self.test_key)
        self.test_key = None
        self.test_pin = None

    def test_get(self):
        """ When a Pin is added to a PinStore, a local key is created.  This
        key can be used to reference and retrieve the Pin using a get request.
        """
        pin = json.loads(self.get_pin(self.test_key).data)
        self.assertEquals(cmp(self.test_pin, pin), 0)

    def test_post(self):
        """ post requests are used to add a new Pin to the Pin.
        """
        self.assertEquals(self.test_pin['parent'], 1)
        self.assertEquals(self.test_pin['child'], 2)

    def test_delete(self):
        """ HTTP delete requests are used to delete a Pin referenced by local
        key.
        """
        self.delete_pin(self.test_key)
        self.assertEquals(self.get_pin(self.test_key).status_code, 404)

    def test_put_parent(self):
        """ Pins are updated with HTTP put requests by referencing local key.
        """
        self.put_pin(self.test_key, {'parent': 3})
        updated = json.loads(self.get_pin(self.test_key).data)
        self.assertEquals(updated['parent'], 3)
        self.assertEquals(updated['child'], 2)

    def test_put_child(self):
        """ Pins are updated with HTTP put requests by referencing local key.
        """
        self.put_pin(self.test_key, {'child': 4})
        updated = json.loads(self.get_pin(self.test_key).data)
        self.assertEquals(updated['parent'], 1)
        self.assertEquals(updated['child'], 4)
