import sys
sys.path.insert(0, '/Users/saltQ/sbaProject')
from util.file_handler import FileReader
import pandas as pd
import numpy as np
import tensorflow as tf

class Model:    # entity + service

    def __init__(self):
        self.fileReader = FileReader()

    def new_model(self, payload):
        this = self.fileReader
        this.context = '/Users/saltQ/sbaProject/price_prediction/data/'
        this.fname = payload
        return pd.read_csv(this.context + this.fname, sep=',')
    def create_tf(self, payload):
    	xy = np.array(payload, dtype=np.float32)
        x_data = xy[:, 1:-1] # feature
        y_data = xy[:, [-1]] # price
        x = tf.placeholder(tf.float32, shape=[None, 4])
        y = tf.placeholder(tf.float32, shape=[None, 2])
        w = tf.Variable(tf.random_normal([4, 1]), name='weight')
        b = tf.Variable(tf.random_normal([1]), name='bias')
        hyposthesis = tf.matmul(x, w) + b
        cost = tf.reduce_mean(tf.square(hyposthesis - y))
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.000005)
        train = optimizer.minimize(cost)
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())
        for step in range(100000):
            cost_, hypo_, _ = sess.run([cost, hyposthesis, train],
                                        feed_dint={x: x_data, y:y_data})
            if step % 500 == 0:
                print(f'# {step} 손실비용: {cost_}')
                print(f'- 배추가격: {hypo_[0]}')

        saver = tf.train.Saver()
        print('저장 완료')