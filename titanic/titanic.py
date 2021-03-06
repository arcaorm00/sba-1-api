import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from util.file_handler import FileReader
# from titanic.service import Service
from config import basedir
from sklearn.ensemble import RandomForestClassifier # rforest
import pandas as pd
import numpy as np
# sklearn algorithm: classification, regression, clustring, reduction 
from sklearn.tree import DecisionTreeClassifier # dtree
from sklearn.ensemble import RandomForestClassifier # rforest
from sklearn.naive_bayes import GaussianNB # nb
from sklearn.neighbors import KNeighborsClassifier # knn
from sklearn.svm import SVC # svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold # k값은 count의 의미로 이해
from sklearn.model_selection import cross_val_score
# dtree, rforest, nb, knn, svm


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
        self.fileReader = FileReader() # @Autowired
        self.kaggle = os.path.join(basedir, 'titanic')
        self.data = os.path.join(self.kaggle, 'data')

    def new_model(self, payload) -> object:
        this = self.fileReader
        this.data = self.data
        this.fname = payload
        return pd.read_csv(os.path.join(self.data, this.fname)) # p.139  df = tensor
    
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
    def title_nominal(this) -> object: # 이름 앞의 경칭
        combine = [this.train, this.test]
        for dataset in combine:
            dataset['Title'] = dataset.Name.str.extract('([A-Za-z]+)\.', expand=False)
        for dataset in combine:
            dataset['Title'] = dataset['Title'].replace(['Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Jonkheer', 'Dona', 'Mme'], 'Rare')
            dataset['Title'] = dataset['Title'].replace(['Countess', 'Lady', 'Sir'], 'Royal')
            dataset['Title'] = dataset['Title'].replace('Ms', 'Miss')
            dataset['Title'] = dataset['Title'].replace('Mlle', 'Mr')
        title_mapping = {'Mr': 1, 'Miss': 2, 'Mrs': 3, 'Master': 4, 'Royal': 5, 'Rare': 6}
        for dataset in combine:
            dataset['Title'] = dataset['Title'].map(title_mapping)
            dataset['Title'] = dataset['Title'].fillna(0)
        
        this.train = this.train
        this.test = this.test
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
        # -0.5 라는 중간값으로 처리했다. (unknown으로 처리되도록)
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf] # 범위
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

        for x in range(len(train['AgeGroup'])):
            if train['AgeGroup'][x] == 'Unknown':
                train['AgeGroup'][x] = age_title_mapping[train['Title'][x]]
        for x in range(len(test['AgeGroup'])):
            if test['AgeGroup'][x] == 'Unknown':
                test['AgeGroup'][x] = age_title_mapping[test['Title'][x]]
        
        age_mapping = {
            'Unknown': 0,
            'Baby': 1, 
            'Child': 2,
            'Teenager': 3,
            'Student': 4,
            'YoungAdult': 5,
            'Adult': 6,
            'Senior': 7
        }
        train['AgeGroup'] = train['AgeGroup'].map(age_mapping)
        test['AgeGroup'] = test['AgeGroup'].map(age_mapping)
        this.train = train
        this.test = test
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
        this.train['FareBand'] = pd.qcut(this.train['Fare'], 4, labels={1, 2, 3, 4}) # 4등분
        this.test['FareBand'] = pd.qcut(this.test['Fare'], 4, labels={1, 2, 3, 4}) 
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
        this.train['Embarked'] = this.train['Embarked'].map({'S': 1, 'C': 2, 'Q': 3})
        this.test['Embarked'] = this.test['Embarked'].map({'S': 1, 'C': 2, 'Q': 3})
        return this

    # Learning Algorithm: dtree, rforest, nb, knn, svm 다섯가지 모듈을 대표로 사용한다.

    @staticmethod
    def create_k_fold():
        return KFold(n_splits=10, shuffle=True, random_state=0)
    
    def accuracy_by_dtree(self, this):
        dtree = DecisionTreeClassifier()
        score = cross_val_score(dtree, this.train, this.label, cv=Service.create_k_fold(), n_jobs=1, scoring='accuracy')
        return round(np.mean(score) * 100, 2)

    def accuracy_by_rforest(self, this):
        rforest = RandomForestClassifier()
        score = cross_val_score(rforest, this.train, this.label, cv=Service.create_k_fold(), n_jobs=1, scoring='accuracy')
        return round(np.mean(score) * 100, 2)

    def accuracy_by_nb(self, this):
        nb = GaussianNB()
        score = cross_val_score(nb, this.train, this.label, cv=Service.create_k_fold(), n_jobs=1, scoring='accuracy')
        return round(np.mean(score) * 100, 2)

    def accuracy_by_knn(self, this):
        knn = KNeighborsClassifier()
        score = cross_val_score(knn, this.train, this.label, cv=Service.create_k_fold(), n_jobs=1, scoring='accuracy')
        return round(np.mean(score) * 100, 2)

    def accuracy_bt_svm(self,this):
        svm = SVC()
        score = cross_val_score(svm, this.train, this.label, cv=Service.create_k_fold(), n_jobs=1, scoring='accuracy')
        return round(np.mean(score) * 100, 2)

class Controller:
    def __init__(self):
        self.fileReader = FileReader() # @Autowired
        self.kaggle = os.path.join(basedir, 'titanic')
        self.data = os.path.join(self.kaggle, 'data')
        self.service = Service()
  
    def modeling(self, train, test):
        service = self.service
        this = self.preprocessing(train, test)

        this.label = service.create_label(this)
        this.train = service.create_train(this)
        return this
        
    def preprocessing(self, train, test):
        service = self.service
        this = self.fileReader
        this.context = '/Users/saltQ/sbaProject/titanic/data/'
        this.train = service.new_model(train) # payload
        this.test = service.new_model(test) # payload
        this.id = this.test['PassengerId'] # 머신에게 문제가 된다.
        print(f'feature 드롭 전 변수: \n{this.train.columns}')
        this = service.drop_feature(this, 'Cabin')
        this = service.drop_feature(this, 'Ticket')
        print(f'feature 드롭 후 변수: \n{this.train.columns}')
        this = service.embarked_nominal(this)
        print(f'승선 항구 정제 결과: \n{this.train.head()}')
        this = service.title_nominal(this)
        print(f'타이틀 정제 결과: \n{this.train.head()}')
        # name 변수에서 title을 추출했으니 name은 필요가 없어졌고, str이니
        # 후에 머신러닝 라이브러리가 이를 인식하는 과정에서 에러를 발생시킬 것이다.
        # 고로 삭제해주어야 마땅하다.
        this = service.drop_feature(this, 'Name')
        this = service.drop_feature(this, 'PassengerId')
        this = service.age_ordinal(this)
        print(f'나이 정제 결과: \n{this.train.head()}')
        this = service.sex_nominal(this)
        print(f'성별 정제 결과: \n{this.train.head()}')
        this = service.fare_ordinal(this)
        this = service.fareBand_nominal(this)
        print(f'요금 정제 결과: \n{this.train.head()}')
        this = service.drop_feature(this, 'Fare')
        print(f'전체 정제 결과: \n{this.train.head()}')
        print(f'train na 체크: {this.train.isnull().sum()}')
        print(f'test na 결과: {this.test.isnull().sum()}')
        return this

    def learning(self, train, test):
        service = self.service
        this = self.modeling(train, test)
        print('############# Learning 결과 #############')
        print(f'결정트리 검증 결과: {service.accuracy_by_dtree(this)}')
        print(f'랜덤포레스트 검증 결과: {service.accuracy_by_rforest(this)}')
        print(f'나이브베이즈 검증 결과: {service.accuracy_by_nb(this)}')
        print(f'KNN 검증 결과: {service.accuracy_by_knn(this)}')
        print(f'SVM 검증 결과: {service.accuracy_bt_svm(this)}')

    def submit(self, train, test): 
        # 머신이 된다. submit은 캐글에게 내 머신을 보내서 평가받게 하는 단계이다.
        this = self.modeling(train, test)
        clf = RandomForestClassifier()
        clf.fit(this.train, this.label)
        prediction = clf.predict(this.test)
        pd.DataFrame(
            {'PassengerId': this.id, 'Survived': prediction}
        ).to_csv(os.path.join(self.data, 'submission.csv'), index=False)

if __name__ == '__main__':
    print(f'********** {basedir} **********')
    ctrl = Controller()
    ctrl.submit('train.csv', 'test.csv')
    