import json
from unittest import TestCase

import rest_app

class RepRestAppTest(TestCase):
    REP_URL = '/rep/api/v1.0/reps'

    def test_root(self):
        """ The current root url response is a placeholder.
        """
        response = self.app.get('/')
        self.assertEquals(response.data, 'Hello, World!')

    def get_rep(self, key):
        """ Helper function to get a specific Rep.
        """
        return self.app.get('%s/%s' % (self.REP_URL, key))

    def post_rep(self, rep):
        """ Helper function to post a new Rep to the RepStore.
        """
        return self.app.post(self.REP_URL, data=json.dumps(rep),
                             content_type='application/json', follow_redirects=True)

    def delete_rep(self, key):
        """ Helper function to delete a Rep from the RepStore.
        """
        return self.app.delete('%s/%s' % (self.REP_URL, key))

    def put_rep(self, key, rep):
        """ Helper function to update a Rep.
        """
        return self.app.put('%s/%s' % (self.REP_URL, key), data=json.dumps(rep),
                            content_type='application/json')

    def setUp(self):
        """ Start each test with a new test Rep.
        """
        rest_app.app.config['TESTING'] = True
        self.app = rest_app.app.test_client()
        response = self.post_rep({'title' : 'Titus Redmond'})
        self.test_key = response.location.rsplit('/', 1)[-1]
        self.test_rep = json.loads(self.get_rep(self.test_key).data)

    def tearDown(self):
        """ Delete the test Rep at the end of each test.
        """
        self.delete_rep(self.test_key)
        self.test_key = None
        self.test_rep = None

    def test_get(self):
        """ When a Rep is added to a RepStore, a local key is created.  This
        key can be used to reference and retrieve the Rep using a get request.
        """
        rep = json.loads(self.get_rep(self.test_key).data)
        self.assertEquals(cmp(self.test_rep, rep), 0)

    def test_post_title(self):
        """ post requests are used to add a new Rep to the RepStore.
        """
        self.assertEquals(self.test_rep['title'], 'Titus Redmond')

    def test_delete(self):
        """ HTTP delete requests are used to delete a Rep referenced by local
        key.
        """
        self.delete_rep(self.test_key)
        self.assertEquals(self.get_rep(self.test_key).status_code, 404)

    def test_put_title(self):
        """ Reps are updated with HTTP put requests by referencing local key.
        """
        self.put_rep(self.test_key, {'title': 'Brian Redmond'})
        updated_title = json.loads(self.get_rep(self.test_key).data)['title']
        self.assertEquals(updated_title, 'Brian Redmond')
