#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config

locals().update(config.__dict__)

this_dir = os.path.dirname(os.path.realpath(config.__file__))
for k in paths:
    # if not abspath
    if not paths[k].startswith('/'):
        paths[k] = os.path.join(this_dir, paths[k])