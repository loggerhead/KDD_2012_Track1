#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import time
import signal
import logging

_begin = None
_received_exit_signal = False

def handler_exit_signal(signal, frame):
    global _received_exit_signal
    if _received_exit_signal:
        print('\nI am gonna to exit anyway!')
        exit(1)
    else:
        print('\nExit program after finish current work!')
    _received_exit_signal = True

signal.signal(signal.SIGINT, handler_exit_signal)

def received_exit_signal():
    return _received_exit_signal

def reprint(*args):
    sys.stdout.write('\r%s' % ''.join(args))
    sys.stdout.flush()

def t(p=True):
    fmt = "\t\t%.3fs"
    current = time.time()

    global _begin
    if _begin is None:
        _begin = current
        return current
    else:
        used = current - _begin
        _begin = None
        if p:
            print fmt % used
        return used

if __name__ == '__main__':
    t()
    t(False)