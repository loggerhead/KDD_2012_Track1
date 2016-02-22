#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import rank_data
from data_reader import Reader

def mean_average_precision(submission_path, solution_path):
    submission_data = Reader(submission_path, lambda line: line.strip().split(','))
    solution_data = Reader(solution_path, lambda line: line.strip().split(','))

    map3s = {}
    ap_sum = 0
    user_cnt = 0
    type = None

    try:
        while True:
            _, items1 = submission_data.next()
            _, items2, ptype = solution_data.next()
            if ptype != type:
                if type is not None:
                    map3s[type] = {
                        'ap_sum': ap_sum,
                        'user_cnt': user_cnt,
                        'mAP@3': ap_sum / user_cnt,
                    }
                ap_sum = 0
                user_cnt = 0
                type = ptype
            user_cnt += 1

            items2 = items2.split()
            if len(items2) == 0:
                continue
            items1 = items1.split()
            if len(items1) == 0:
                continue
            ap = 0.0
            cnt = 0.0

            for i in xrange(min(3, len(items1))):
                if items1[i] in items2 and items1[i] not in items1[:i]:
                    cnt += 1
                    ap += cnt / (i+1)

            n = min(3, len(items2))
            ap_sum += ap / n
    except StopIteration:
        pass

    map3s[type] = {
        'ap_sum': ap_sum,
        'user_cnt': user_cnt,
        'mAP@3': ap_sum / user_cnt,
    }
    return map3s

def get_submission_path(path):
    prefix, suffix = path.rsplit('.', 1)
    if 'sub' not in prefix:
        path = prefix + '_sub.csv'
    return path

def get_rank(val, type):
    ranks = rank_data.__dict__[type.lower()]
    rank = 1
    for map3 in ranks:
        if val < map3:
            rank += 1
        else:
            break
    return rank

def compute_mAP_and_rank(submission_path, solution_path):
    map3s = mean_average_precision(submission_path, solution_path)
    for type in map3s:
        mAP = map3s[type]['mAP@3']
        # 0.03 is a bug of leaderboard rank
        print "%7s rank: %3d  \tmAP@3: %.5f" % (type, get_rank(mAP - 0.03, type), mAP)