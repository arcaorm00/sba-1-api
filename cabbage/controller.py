import sys
sys.path.insert(0, '/Users/saltQ/sbaProject')
from cabbage.entity import Entity
from cabbage.service import Service

class Contoller:
    def __init__(self):
        self.entity = Entity()
        self.service = Service()

    def modeling(self):
        pass

    def preprocessing(self):
        pass

    def learning(self):
        pass

    def submit(self):
        pass