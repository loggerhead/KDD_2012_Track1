#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random


class Reader(object):
    def __init__(self, filepath, get_fields=None, skip_header=False):
        self.__dict__.update(locals())
        self.get_fields = get_fields or self._get_fields
        self.skiped_header = False

        path, suffix = self.filepath.rsplit('.', 1)
        self.filter_path = path + '.filter.' + suffix

        self.fp = open(filepath, 'rb')
        self.filesize = os.path.getsize(filepath)

    def _get_fields(self, line):
        return map(int, line.strip().split(','))

    def reset(self):
        self.fp.seek(0)
        self.skiped_header = False
        return self

    def get_all(self):
        return self.reset()

    def __iter__(self):
        return self

    def next_line(self):
        return self.fp.next()

    def next(self):
        if self.skip_header and not self.skiped_header:
            self.next_line()
            self.skiped_header = True
        return self.get_fields(self.fp.next())

    def random(self):
        fp_position = self.fp.tell()
        self.fp.seek(random.randrange(self.filesize))
        # skip current line
        self.fp.readline()

        line = self.fp.readline()
        # last line?
        if len(line) == 0:
            self.fp.seek(0)
            if self.skip_header:
                self.fp.readline()
            line = self.fp.readline()

        # recover
        self.fp.seek(fp_position)
        return self.get_fields(line)

    def sample(self, number):
        cnt = 0
        while cnt < number:
            yield self.random()
            cnt += 1