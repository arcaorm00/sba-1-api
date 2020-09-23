from titanic.entity import Entity
import sys
sys.path.insert(0, '/Users/saltQ/sbaProject')
import pandas as pd
import numpy as np

'''
** PassengerId  고객ID, ==> 머신러닝 모델에게 주어질 문제
** Survived 생존여부,  ==> 머신러닝 모델이 맞혀야 할 답
Pclass 승선권 1 = 1등석, 2 = 2등석, 3 = 3등석,
Name,
Sex,
Age,
SibSp 동반한 형제, 자매, 배우자,
Parch 동반한 부모, 자식,
-- Ticket 티켓번호,
Fare 요금,
-- Cabin 객실번호,
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
        # 교과서 p.149 내용처럼 훈련 세트와 테스트 세트로 나눈다.
        this.train = this.train.drop([feature], axis = 1)
        this.test = this.test.drop([feature], axis = 1) 
        return this

    @staticmethod
    def pclass_ordinal(this) -> object:
        return this

    @staticmethod
    def name_nominal(this) -> object:
        return this

    @staticmethod
    def sex_nominal(this) -> object:
        combine = [this.train, this.test] # train과 test가 묶인다.
        sex_mapping = {'male': 0, 'female': 1}
        for dataset in combine:
            dataset['Sex'] = dataset['Sex'].map(sex_mapping)

        this.train = this.train
        this.test = this.test
        return this

    @staticmethod
    def age_ordinal(this) -> object:
        train = this.train
        test = this.test
        train['Age'] = train['Age'].fillna(-0.5)
        test['Age'] = test['Age'].fillna(-0.5)
        # age를 평균으로 넣기도 애매하고 다수로 넣기도 근거가 없다.
        # 특히 age는 생존률 판단에서 가중치(weight)가 상당하므로 디테일한 접근이 필요하다.
        # 따라서 나이를 모르는 승객은 모르는 상태로 처리해야 값의 왜곡을 줄일 수 있기에
        # -0.5 라는 경계값으로 처리했다.
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf]
        labels = ['Unknown', 'Baby', 'Child', 'Teenager', 'Student', 'YoungAdult', 'Adult', 'Senior']
        train['AgeGroup'] = pd.cut(train['Age'], bins, labels=labels)
        test['AgeGroup'] = pd.cut(test['Age'], bins, labels=labels)
        age_title_mapping = {
            0: 'Unknown',
            1: 'Baby', 
            2: 'Child',
            3: 'Teenager',
            4: 'Student',
            5: 'YoungAdult',
            6: 'Adult',
            7: 'Senior'
        } # labels를 값으로 처리
        return this

    @staticmethod
    def sibsp_numeric(this) -> object:
        return this

    @staticmethod
    def parch_numeric(this) -> object:
        return this

    @staticmethod
    def fare_ordinal(this) -> object:
        # []은 변수명, {}은 변수값
        this.train['FareBand'] = pd.qcut(this['Fare'], 4, labels={1, 2, 3, 4}) # 4등분
        this.test['FareBand'] = pd.qcut(this['Fare'], 4, labels={1, 2, 3, 4}) 
        return this
    @staticmethod
    def fareBand_nominal(this) -> object: # 요금이 다양하니 클러스터링(그룹화)을 하기 위한 준비
        this.train = this.train.fillna({'FareBand': 1}) # FareBand는 없는 칼럼이지만 추가했다.
        this.test = this.test.fillna({'FareBand': 1})
        return this
    
    @staticmethod
    def embarked_nominal(this) -> object:
        this.train = this.train.fillna({'Embarked': 'S'}) # s가 가장 많아서 빈곳에 채운다.
        this.test = this.test.fillna({'Embarked': 'S'}) # 교과서 144p
        # 많은 머신러닝 라이브러리는 클래스 레이블이 *정수*로 인코딩되었을 것이라고 기대한다.
        # 교과서 146p를 보면 문자 blue = 0, green = 1, red = 2로 치환한다. ==> mapping한다.
        this.train['Embarked'] = this.train['Enbarked'].map({'S': 1, 'C': 2, 'Q': 3})
        this.test['Embarked'] = this.test['Enbarked'].map({'S': 1, 'C': 2, 'Q': 3})
        return this