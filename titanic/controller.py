import sys
sys.path.insert(0, '/Users/saltQ/sbaProject')
from titanic.entity import Entity
from titanic.service import Service

class Controller:
    def __init__(self):
        self.entity = Entity()
        self.service = Service()
  
    def modeling(self, train, test):
        service = self.service
        this = self.preprocessing(train, test)

        this.label = service.create_label(this)
        this.train = service.create_train(this)
        return this
        
    def preprocessing(self, train, test):
        service = self.service
        this = self.entity
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

    def submit(self): 
        # 머신이 된다. submit은 캐글에게 내 머신을 보내서 평가받게 하는 단계이다.
        pass

if __name__ == '__main__':
    ctrl = Controller()
    ctrl.learning('train.csv', 'test.csv')
    