#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import thread
from util import *
from data_reader import Reader
from latent_factor_model import LFM

def predict(train_path, test_path, outpath):
    test = Reader(test_path, skip_header=False)
    model = LFM(train_path).do_train()

    print "predict and write result...",; t()
    with open(outpath, 'wb') as fp:
        for user, item, _, timestamp in test:
            r = model.predict(user, item)
            line = ','.join(map(str, [user, item, r, timestamp])) + '\n'
            fp.write(line)
    t()

def to_submission_format(predicted_path, outpath):
    def get_fields(line):
        return [float(field) if '.' in field else int(field) for field in line.split(',')]

    data = Reader(predicted_path, get_fields)

    print "convert predict result to dict...",; t()
    public = {}
    private = {}
    for user, item, r, timestamp in data:
        if timestamp < 1321891200:
            tmp = public
        else:
            tmp = private
        tmp.setdefault(user, []).append((r, item))
    t()

    def remove_duplicate(l):
        has = set()
        return [x for x in l if not (x in has or has.add(x))]

    print "convert to submission format...",; t()
    with open(outpath, 'wb') as fp:
        def write_to_file(d):
            for user in sorted(d.keys()):
                items = remove_duplicate([item for _, item in sorted(d[user], reverse=True)])[:3]
                fp.write("%s,%s\n" % (user, " ".join(map(str, items))))

        write_to_file(public)
        write_to_file(private)
    t()