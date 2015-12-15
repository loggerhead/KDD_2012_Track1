#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from datetime import date, datetime
from data_reader import Reader

def timestamp2hour(t):
    return datetime.fromtimestamp(t).strftime('%H')

def get_summary_of_dataset(filepath, skip_header=False, has_timestamp=True):
    reader = Reader(filepath, skip_header=skip_header)

    users = set()
    items = set()
    positive = 0
    negative = 0
    begin_time = time.time()
    end_time = 0
    hours = {}

    for record in reader:
        users.add(record[0])
        items.add(record[1])

        result = record[2]
        if result > 0:
            positive += 1
        elif result < 0:
            negative += 1

        if not has_timestamp:
            continue

        timestamp = record[3]
        if begin_time > timestamp:
            begin_time = timestamp
        if end_time < timestamp:
            end_time = timestamp

        hour = timestamp2hour(timestamp)
        hours[hour] = hours.get(hour, 0) + 1

    return locals()

def summary_of_training_set(filepath, skip_header=False, has_timestamp=True):
    summary = get_summary_of_dataset(filepath,
                                     skip_header=skip_header,
                                     has_timestamp=has_timestamp)
    users = summary['users']
    items = summary['items']
    positive = summary['positive']
    negative = summary['negative']
    begin_time = summary['begin_time']
    end_time = summary['end_time']
    interval = float(end_time - begin_time)

    print (" Summary of '%s' " % os.path.basename(filepath)).center(80, "=")
    print "Users: %d\tItems: %d\tUsers/Items: %.2f" % (len(users), len(items), float(len(users)) / len(items))
    print "+1: %d\t-1: %d\t+1/-1: %.2f" % (positive, negative, float(positive) / negative)
    print "Begin time: %d\tEnd time:%d\tInterval: %ds = %.2f h = %.2f d" % (begin_time, end_time, interval, interval / 3600, interval / (3600 * 24))

    print (' Distribution of user active time (in hour) ').center(80, fillchar='=')
    print_histogram(summary['hours'])

def get_summary_of_user_profile(filepath, skip_header=False):
    def get_fields(line):
        record = line.split(",")

        try:
            age = 2012 - int(record[1])
        except:
            age = 0
        user = int(record[0])
        gender = int(record[2])
        num_of_tweet = int(record[3])
        tags = map(int, record[4].strip().split(";"))

        return [user, age, gender, num_of_tweet, tags]

    reader = Reader(filepath, skip_header=skip_header, get_fields=get_fields)

    ages = {}
    genders = {}
    ntweet = {}
    ntags = {}

    for user, age, gender, num_of_tweet, tags in reader:
        num_of_tags = len(tags)
        ages[age] = ages.get(age, 0) + 1
        genders[gender] = genders.get(gender, 0) + 1
        ntweet[num_of_tweet] = ntweet.get(num_of_tweet, 0) + 1
        ntags[num_of_tags] = ntags.get(num_of_tags, 0) + 1

    return {
        'age': ages,
        'gender': genders,
        'tweet': ntweet,
        'tags': ntags,
    }

def summary_of_user_profile(filepath, skip_header=False):
    summary = get_summary_of_user_profile(filepath, skip_header=skip_header)

    def show(key):
        fillchar = '='
        print (' Distribution of %s' % key + ' ').center(80, fillchar=fillchar)
        print_histogram(summary[key])

    show('age')
    show('gender')
    show('tweet')
    show('tags')

def print_histogram(d, symbol='|', threshold=0.05, bar_length=50, max_key_len=3):
    total = float(sum(d.values()))
    for k in sorted(d.keys()):
        l = round(d[k] / total * bar_length)
        if l > threshold:
            print '%*s: %s' % (max_key_len, k, symbol * int(l))

    return total