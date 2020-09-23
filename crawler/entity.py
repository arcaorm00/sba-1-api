# 프로퍼티는 url, parser, path, api, apikey ==> 전부 str
from dataclasses import dataclass

@dataclass
class Entity:
    url: str = ''
    parser: str = 'html.parser'
    path: str = ''
    api: str = ''
    apikey: str = ''