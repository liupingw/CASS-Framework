# coding: utf-8

from __future__ import print_function

import os
import tensorflow as tf
import tensorflow.contrib.keras as kr
from Naked.commands.classifier import Classifier

from Classifer.cnn_model import TCNNConfig, TextCNN
from Classifer.data.cnews_loader import read_category, read_vocab

try:
    bool(type(unicode))
except NameError:
    unicode = str

base_dir = '../Classifer/data/cnews'
vocab_dir = os.path.join(base_dir, 'data.vocab.txt')

save_dir = '../Classifer/checkpoints/textcnn'
save_path = os.path.join(save_dir, 'best_validation')



class CnnModel:
    def __init__(self):
        self.config = TCNNConfig()
        self.categories, self.cat_to_id = read_category()
        self.words, self.word_to_id = read_vocab(vocab_dir)
        self.config.vocab_size = len(self.words)
        self.model = TextCNN(self.config)

        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess=self.session, save_path=save_path)

    def predict(self, message):
        content = unicode(message)
        data = [self.word_to_id[x] for x in content if x in self.word_to_id]

        feed_dict = {
            self.model.input_x: kr.preprocessing.sequence.pad_sequences([data], self.config.seq_length),
            self.model.keep_prob: 1.0
        }

        y_pred_cls = self.session.run(self.model.y_pred_cls, feed_dict=feed_dict)
        return self.categories[y_pred_cls[0]]


if __name__ == '__main__':


    cnn_model = CnnModel()

    writeFile = open("data/predict.txt", 'w', encoding='utf-8')

    readFile = open("data/cnews/data.predict.txt",encoding='utf-8')
    all_lines = readFile.readlines()
    for line in all_lines:
        cat = cnn_model.predict(line)
        print(cat)
        writeFile.write(cat +"\t" + line)

    readFile.close()
    writeFile.close()
