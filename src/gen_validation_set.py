#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from data_reader import Reader

def gen_validation_set(inpath, train_path, validation_path, skip_header=False):
    reader = Reader(inpath, skip_header=skip_header)
    data_dir = os.path.dirname(inpath)

    train_set = open(os.path.join(data_dir, train_path), 'wb')
    validation_set = open(os.path.join(data_dir, validation_path), 'wb')

    for record in reader:
        time = record[-1]
        line = ','.join(map(str, record)) + '\n'
        # last 7 days used as validation set
        if time < 1320336000:
            train_set.write(line)
        else:
            validation_set.write(line)

    train_set.close()
    validation_set.close()