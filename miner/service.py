import sys
sys.path.insert(0, '/Users/saltQ/sbaProject')
import re
from nltk.tokenize import word_tokenize
from konlpy.tag import Okt
import pandas as pd
from nltk import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt
class SamsungService:
    def __init__(self):
        self.texts = []
        self.tokens = []
        self.okt = Okt()
        self.stopwords = []
        self.freqtxt = []
    def extract_token(self, payload):
        print('>>> text 문서에서 token 추출')
        filename = payload.context + payload.fname
        with open(filename, 'r', encoding='utf-8') as f:
            self.texts = f.read()
        # print(f'{self.texts[:300]}')
    def extract_hanguel(self):
        print('>>> 한글만 추출')
        texts = self.texts.replace('\n', ' ')
        tokenizer = re.compile(r'[^ ㄱ-힣]')
        self.texts = tokenizer.sub('', texts)
        # print(f'{self.texts[:300]}')
    def conversion_token(self):
        print('>>> 토큰으로 변환')
        self.tokens = word_tokenize(self.texts)
        # print(f'{self.tokens[:300]}')
    def compound_noun(self):
        print('>>> 복합명사는 묶어서 fitering 으로 출력')
        print('>>> ex) 삼성전자의 스마트폰은 --> 삼성전자 스마트폰')
        noun_token = []
        for token in self.tokens:
            token_pos = self.okt.pos(token)
            temp = [txt_tag[0] for txt_tag in token_pos
                    if txt_tag[1] == 'Noun']
            if len("".join(temp)) > 1:
                noun_token.append("".join(temp))
        self.texts = " ".join(noun_token)
        # print(f'{self.texts[:300]}')
    def extract_stopword(self, payload):
        print('>>> text 문서에서 token 추출')
        filename = payload.context + payload.fname
        with open(filename, 'r', encoding='utf-8') as f:
            self.stopwords = f.read()
        self.stopwords = self.stopwords.split(' ')
        # print(f'{self.stopwords[:10]}')
    def filtering_text_with_stopword(self):
        print('>>> stopword 로 필터링 ')
        self.texts = word_tokenize(self.texts)
        self.texts = [text for text in self.texts
                      if text not in self.stopwords]
    def frequent_text(self):
        print('>>> 빈도수로 정렬 ')
        self.freqtxt = pd.Series(dict(FreqDist(self.texts)))\
            .sort_values(ascending=False)
        # print(f'{self.freqtxt[:10]}')
    def draw_wordcloud(self, payload):
        print('>>> 워드크라우드 작성 ')
        filename = payload.context + payload.fname
        wcloud = WordCloud(filename,
                           relative_scaling=0.2,
                           background_color='white').generate(" ".join(self.texts))
        plt.figure(figsize=(12,12))
        plt.imshow(wcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()