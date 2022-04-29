import numpy as np


class EmbedsReader(object):
    def __init__(self):
        self.mapping = {}

    def load(self, path):
        data = np.load(path, allow_pickle=True)[()]
        assert data['tag'] not in self.mapping
        self.mapping[data['tag']] = data

    @property
    def tags(self):
        return tuple(self.mapping.keys())

    def __getitem__(self, item):
        return self.mapping[item]

    def get_words(self, tag):
        return tuple(self.mapping[tag]['extractions'].keys())

    def read_embeddings(self, tag, word):
        extractions = self.mapping[tag]['extractions']
        return extractions[word]['embeddings']
