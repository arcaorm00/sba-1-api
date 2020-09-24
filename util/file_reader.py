from dataclasses import dataclass
'''
context path: /Users/saltQ/sbaProject/
module path: /titanic/data/
'''
@dataclass
class Entity:
    context: str = ''
    fname:str = ''
    train:object = None
    test:object = None
    id:str = ''
    label:str = ''