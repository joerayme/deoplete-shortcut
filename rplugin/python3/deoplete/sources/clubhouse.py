from urllib.parse import urlparse
import http.client
import json
import os

from .base import Base

class Source(Base):
    def __init__(self, vim):
        Base.__init__(self, vim)

        self.rank = 100
        self.name = 'clubhouse'
        self.description = 'Clubhouse ticket numbers'
        self.mark = '[ch]'
        self.filetypes = ['gitcommit']
        self.input_pattern = r'\[ch'
        self._token = None
        self._query = None

    def on_init(self, context):
        self._query = context['vars'].get('deoplete#sources#clubhouse#query', 'is:story')
        token_file = context['vars'].get('deoplete#sources#clubhouse#apitokenfile', '{}/.clubhouse'.format(os.getenv('HOME')))
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

        print(payload)

        c = http.client.HTTPSConnection('api.clubhouse.io')
        c.request('GET', '/api/v3/search/stories?token={}'.format(self._token), body=json.dumps(payload), headers={'Accept': 'application/json'})

        # try:
        response = c.getresponse()
        if response.status != 200:
            print(dir(response))
            return
        result = json.loads(response.read().decode('utf-8'))
        print(result)

        return [{'word': '[ch{}]'.format(ticket['id']),
                 'menu': ticket['name']} for ticket in result['data']]