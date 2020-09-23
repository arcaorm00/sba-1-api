from dataclasses import dataclass

@dataclass
class Entity:

    context: str = '/Users/saltQ/sbaProject/titanic/data/'
    fname: str = ''
    train: object = None
    test: object = None
    id: str = ''
    label: str = ''
    # def __init__(self, context, fname, train, test, id, label):
    #     self._context = context # _ 는 default 접근 # __는 private 접근
    #     self._fname = fname
    #     self._train = train
    #     self._test = test
    #     self._id = id
    #     self._label = label
    
    