#!/usr/bin/env python
# -*- coding: utf-8 -*-

import conf
from data_reader import Reader

TAU0     = conf.TAU0
EPSILON  = conf.EPSILON
PI_MINUS = conf.PI_MINUS
PI_PLUS  = conf.PI_PLUS

# @return dict[user][time] = [(item, result)]
def dataset2dict(reader):
    records = {}
    for user, item, result, time in reader:
        if user not in records:
            records[user] = {}
        if time not in records[user]:
            records[user][time] = []

        records[user][time].append((item, result))
    return records

# @return [[(item, result)]]
def seperate_to_sessions(urecord, times):
    # formula (5)
    intervals = [(times[s], times[s+1]) for s in xrange(len(times)-1)]
    deltats = [ts[1]-ts[0] for ts in intervals if ts[1]-ts[0] < 3600]

    # formula (6)
    # τ(u)
    tauu = 0.5 * TAU0
    if len(deltats):
        tauu += 0.5 * sum(deltats)/len(deltats)

    # ψ(u)
    sessions = [[] for _ in xrange(len(intervals)+1)]
    # seperated to different sessions
    for i in xrange(len(intervals)):
        ts = intervals[i]
        dt = ts[1] - ts[0]

        sessions[i].extend(urecord[ts[0]])
        sessions[i + (dt > tauu)].extend(urecord[ts[1]])

    sessions = filter(lambda session: len(session) > 0, sessions)
    return sessions

def get_positive_sessions(sessions):
    # `pair` means 'item and result pair'
    sessions_plus = [filter(lambda pair: pair[1] == 1, s) for s in sessions]
    session_num = len([s for s in sessions_plus if len(s) > 0])
    return sessions_plus, session_num

def get_eligibles_from_session(session, session_plus):
    sessions_plus = set(session_plus)
    # σ-
    min_i = len(session)
    # σ+
    max_i = -1

    for i in xrange(len(session)):
        if session[i] in session_plus:
            if min_i > i:
                min_i = i
            max_i = i

    pairs = []
    for i in xrange(len(session)):
        # I think formula (7), (8) have some problems, and it should be below
        if min_i - PI_PLUS <= i <= max_i + PI_MINUS:
            pairs.append(session[i])

    return pairs

def write_records_to_file(records, outpath):
    with open(outpath, 'wb') as fp:
        for user in records:
            for item, result in records[user]:
                line = "%d,%d,%d\n" % (user, item, result)
                fp.write(line)

# session analysis for data filtering
def filter_by_session(filepath, outpath, skip_header=False):
    reader = Reader(filepath, skip_header=skip_header)
    # read dataset into `dict`
    # @type records[user][time] = [(item, result)]
    records = dataset2dict(reader)

    for user in records:
        # @type urecord[time] = [(item, result)]
        urecord = records[user]
        times = urecord.keys()
        records[user] = []

        # @type [[(item, result)]]
        sessions = seperate_to_sessions(urecord, times)
        if len(sessions) == 0:
            continue

        # ψ+(u)
        sessions_plus, session_num = get_positive_sessions(sessions)
        # formula (9)
        if not (0 < session_num < EPSILON * len(sessions)):
            continue

        # @type records[user] = [(item, result)]
        for k in xrange(len(sessions)):
            session = sessions[k]
            session_plus = sessions_plus[k]
            # `pairs` means 'item and result pairs'
            pairs = get_eligibles_from_session(session, session_plus)
            records[user].extend(pairs)

    write_records_to_file(records, outpath)