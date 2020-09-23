from titanic.entity import Entity
import sys
sys.path.insert(0, '/Users/saltQ/sbaProject')
import pandas as pd
import numpy as np
'''
PassengerId  고객ID,
Survived 생존여부,  ==> 머신러닝 모델이 맞혀야 할 답
Pclass 승선권 1 = 1등석, 2 = 2등석, 3 = 3등석,
Name,
Sex,
Age,
SibSp 동반한 형제, 자매, 배우자,
Parch 동반한 부모, 자식,
Ticket 티켓번호,
Fare 요금,
Cabin 객실번호,
Embarked 승선한 항구명 C = 쉐브루, Q = 퀸즈타운, S = 사우스햄튼
'''

class Service:
    def __init__(self):
        self.entity = Entity() # @Autowired

    def new_model(self, payload) -> object:
        this = self.entity
        this.fname = payload
        return pd.read_csv(this.context + this.fname) # p.139  df = tensor
    
    @staticmethod
    def create_train(this):
        return this.train.drop('Survived', axis=1) # train은 답이 제거된 데이터셋이다.

    # self 없이 create_lable 기능을 만든다. (지도학습)
    @staticmethod
    def create_label(this):
        return this.train['Survived'] # label은 곧 답이 된다.

    # self 없이 차원 축소를 위한 drop_feature 기능을 만든다.
    @staticmethod
    def drop_feature(this, feature) -> object:
        # p.149 내용처럼 훈련 세트와 테스트 세트로 나눈다.
        this.train = this.train.drop([feature], axis = 1)
        this.test = this.test.drop([feature], axis = 1) 
        return this