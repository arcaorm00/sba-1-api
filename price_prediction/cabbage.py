import sys
sys.path.insert(0, '/Users/saltQ/sbaProject')
from util.file_handler import FileReader
import pandas as pd
import numpy as np
import tensorflow as tf

class Model:    # entity + service

    def __init__(self):
        self.fileReader = FileReader()
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

if __name__ == '__main__':
    m = Model()
    dframe = m.new_model('price_data.csv')
    print(dframe.head())
    m.create_tf(dframe)
    