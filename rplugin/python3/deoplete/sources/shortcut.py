from urllib.parse import urlparse
import http.client
import json
import os

from .base import Base

class Source(Base):
    def __init__(self, vim):
        Base.__init__(self, vim)

        self.rank = 100
        self.name = 'shortcut'
        self.description = 'Shortcut ticket numbers'
        self.mark = '[sc]'
        self.filetypes = ['gitcommit']
        self._token = None
        self._query = None

    def on_init(self, context):
        self._query = context['vars'].get('deoplete#sources#shortcut#query', 'is:story')
        token_file = context['vars'].get('deoplete#sources#shortcut#apitokenfile', '{}/.shortcut'.format(os.getenv('HOME')))
        if os.path.isfile(token_file):
            with open(token_file, 'r') as fh:
                self._token = fh.read()

    def gather_candidates(self, context):
        if self._token is None:
            return []

        payload = {
            'page_size': 10,
            'query': self._query
        }

        c = http.client.HTTPSConnection('api.app.shortcut.com')
        c.request('GET', '/api/v3/search/stories', body=json.dumps(payload), headers={'Content-Type': 'application/json', 'Shortcut-Token': self._token})

        # try:
        response = c.getresponse()
        if response.status != 200:
            return []

        result = json.loads(response.read().decode('utf-8'))

        words = [{'word': 'sc-{}'.format(ticket['id']),
                  'menu': ticket['name']} for ticket in result['data']]
        return words