# from data import expand_words
import sys


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Keywords(metaclass=Singleton):
    def __init__(self):
        self.keywords = dict()
        self.selector = self._english
        self.selector()

    def _english(self):
        # verifications = ('check', 'verify', 'observe', 'recheck')
        # verifications = expand_words(verifications, k=5)
        verifications = ('verify', 'validate', 'observing', 'observe', 'checking', 'check', 'recheck', 'rechecked')
        self.keywords['verifications'] = verifications
        self.keywords['adverbs_of_manner_termination'] = 'ly'

