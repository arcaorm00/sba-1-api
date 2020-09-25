import sys
sys.path.insert(0, '/Users/saltQ/sbaProject')
from util.file_handler import FileReader
import pandas as pd
import numpy as np
import tensorflow as tf
from dataclasses import dataclass

@dataclass
class Model:    # entity + service

    # year,avgTemp,minTemp,maxTemp,rainFall,avgPrice
    # 20100101,-4.9,-11,0.9,0,2123
    # 멤버변수
    year:int = 0
    avgTemp:float = 0.0
    minTemp:float = 0.0
    maxTemp:float = 0.0
    rainFall:float = 0.0
    avgPrice:int = 0

    # 클래스 내부에서 공유하는 객체, 상수값
    def __init__(self):
        self.fileReader = FileReader() # 기능은 상수
        self.context = '/Users/saltQ/sbaProject/price_prediction/data/'

    def new_model(self, payload):
        this = self.fileReader
        this.context = self.context
        this.fname = payload
        return pd.read_csv(this.context + this.fname, sep=',')

    def create_tf(self, payload):
        xy = np.array(payload, dtype=np.float32)
        x_data = xy[:, 1:-1] # feature
        y_data = xy[:, [-1]] # price
        x = tf.compat.v1.placeholder(tf.float32, shape=[None, 4])
        y = tf.compat.v1.placeholder(tf.float32, shape=[None, 1])
        w = tf.Variable(tf.random.normal([4, 1]), name='weight')
        b = tf.Variable(tf.random.normal([1]), name='bias')
        hyposthesis = tf.matmul(x, w) + b
        cost = tf.reduce_mean(tf.square(hyposthesis - y))
        optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=0.000005)
        train = optimizer.minimize(cost)
        sess = tf.compat.v1.Session()
        sess.run(tf.compat.v1.global_variables_initializer())
        for step in range(100000):
            cost_, hypo_, _ = sess.run([cost, hyposthesis, train],
                                        feed_dict={x: x_data, y: y_data})
            if step % 500 == 0:
                print(f'# {step} 손실비용: {cost_}')
                print(f'- 배추가격: {hypo_[0]}')

        saver = tf.compat.v1.train.Saver()
        saver.save(sess, self.context + 'saved_model.ckpt')
        print('저장 완료')

    def test(self):
        self.avgPrice = 100
        return self.avgPrice

    def service(self):
        X = tf.combat.v1.placeholder(tf.float32, shape=[None, 4])
        # year,avgTemp,minTemp,maxTemp,rainFall,avgPrice
        # 에서 avgTemp,minTemp,maxTemp,rainFall 입력 받겠다.
        # year는 모델에서 필요없는 값 -> 상관관계 없음
        # avgPrice는 얻고자 하는 답. 종속변수
        # avgTemp,minTemp,maxTemp,rainFall는 종속변수를 결정하는 독립변수이자
        # avgPrice를 결정하는 요소로 사용되는 파라미터 (중요!)
        # 이제 우리는 통계와 확률로 들어가야 하니 용어를 잘 정의하자.
        # y = wx + b 선형관계
        # X는 대문자를 사용하고 확률변수라고 한다.
        # 비교. 웹프로그래밍(Java, C)에서는 소문자로 x를 쓰는데 이것은 한 타인에 하나의 value
        # 그리고 그 값은 외부에서 주어지는 하나의 값이므로 그냥---변수
        # 지금은 X의 값이 제한적이지만 집합상태로 많은 값이 있는 상태
        # 이럴 때는 확률---변수. 
        W = tf.Variable(tf.random.normal([4, 1]), name='weight')
        b = tf.Variable(tf.random.normal([1]), name='bias')
        # tensorflow에서 변수는 웹프로그래밍에서의 변수와 다르다.
        # 이 변수를 결정하는 것은 외부에서 주어진 값이 아니라 tensor가 내부에서 사용하는 변수이다.
        # 기존 웹에서 사용하는 변수는 placeholder.
        saver = tf.combat.v1.train.Saver()
        with tf.Session() as sess:
            sess.run(tf.combat.v1.global_variables_initializer())
            saver.restore(sess, self.context + 'saved_model.ckpt')
            data = [[self.avgTemp, self.minTemp, self.maxTemp, self.rainFall], ]
            arr = np.array(data, dtype = np.float32)
            dict = sess.run(tf.matmul(X, W) + b, {X: arr[0:4]}) # matmul: 상호 곱 (매트릭스 구조이기 때문)
            # Y = WX + b를 코드로 표현하면 위와 같이 나타낼 수 있다.
            print(dict[0])
            return int(dict[0])
            

if __name__ == '__main__':
    m = Model()
    dframe = m.new_model('price_data.csv')
    print(dframe.head())
    m.create_tf(dframe)
    