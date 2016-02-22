#!/usr/bin/env python
# -*- coding: utf-8 -*-

import conf
import math
import random
from util import *
from data_reader import Reader

SAMPLES_NUMBER = conf.SAMPLES_NUMBER
TRAIN_REPEAT   = conf.TRAIN_REPEAT
DIMENSION      = conf.DIMENSION
LAMBDA         = conf.LAMBDA
ETA            = conf.ETA

SQRT_DIMENSION = math.sqrt(conf.DIMENSION)


class LFM(object):
    def __init__(self, datapath):
        self.data = Reader(datapath, skip_header=False)
        self.get_data = lambda: self.data.sample(SAMPLES_NUMBER)
        self.b_u = {}
        self.b_i = {}
        self.q_i = {}
        self.p_u = {}
        self.avg_bu = 0
        self.avg_bi = 0

    def do_train(self):
        eta = ETA

        print "init LFM...",; t()
        b_u, b_i, q_i, p_u = self.init_LFM()
        t()

        i = 1
        while i < 1 + TRAIN_REPEAT and not received_exit_signal():
            t()
            cnt = 0
            average_e = 0

            for record in self.get_data():
                user, item, result = record[:3]
                # map [-1, 1] to [0, 1]
                e = ((result + 1) >> 1) - self.predict(user, item)
                average_e += e * e
                cnt += 1

                b_u[user] += eta * (e - LAMBDA * b_u[user])
                b_i[item] += eta * (e - LAMBDA * b_i[item])
                for k in xrange(DIMENSION):
                    p = p_u[user][k]
                    q = q_i[item][k]
                    q_i[item][k] += eta * (e * p - LAMBDA * q)
                    p_u[user][k] += eta * (e * q - LAMBDA * p)

            average_e /= cnt
            reprint("%dth trainning used %.1fs\terror = %lf" % (i, t(False), average_e))
            i += 1

        print
        self.update_average_args()
        return self

    def init_LFM(self):
        self.u = 0.0
        self.total = 0

        for record in self.data.get_all():
            user, item, result = record[:3]
            self.u += result
            self.total += 1

            if user not in self.b_u:
                self.b_u[user] = 0
                self.p_u.setdefault(user, self.random_qp())
            if item not in self.b_i:
                self.b_i[item] = 0
                self.q_i.setdefault(item, self.random_qp())

        self.u /= self.total
        return [self.b_u, self.b_i, self.q_i, self.p_u]

    def random_qp(self):
        return [random.random() / SQRT_DIMENSION for _ in xrange(DIMENSION)]

    def predict(self, user, item):
        qp = self.compute_qp(user, item)
        predict_r = self.get_b_ui(user, item) + qp
        return predict_r

    def compute_qp(self, u, i):
        self.q_i.setdefault(i, self.random_qp())
        self.p_u.setdefault(u, self.random_qp())
        return sum(self.q_i[i][k]*self.p_u[u][k] for k in xrange(DIMENSION))

    def get_b_ui(self, u, i):
        b_i = self.b_i.get(i, self.avg_bi)
        b_u = self.b_u.get(u, self.avg_bu)
        return self.u + b_i + b_u

    def update_average_args(self):
        bi = self.b_i.values()
        bu = self.b_u.values()
        self.avg_bi = sum(bi) / float(len(bi))
        self.avg_bu = sum(bu) / float(len(bu))