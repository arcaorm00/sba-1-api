
class Entity:
    def __init__(self, context, fname, train, test, id, label):
        self._context = context # _ 는 default 접근 # __는 private 접근
        self._fname = fname
        self._train = train
        self._test = test
        self._id = id
        self._label = label

    @property
    def context(self) -> str: # -> str 리턴 타입이 str이다.
        return self._context

    @context.setter
    def context(self, context):
        self._context = context

    @property
    def fname(self) -> str:
        return self.fname
    
    @fname.setter
    def fname(self, fname):
        self.fname = fname
        
    @property
    def train(self) -> object:
        return self.train
    
    @fname.setter
    def train(self, train):
        self.train = train

    @property
    def test(self) -> object:
        return self.test
    
    @fname.setter
    def test(self, test):
        self.test = test
