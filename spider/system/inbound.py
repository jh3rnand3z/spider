# -*- coding: utf-8 -*-
'''
    Spider inbound system.
'''

# This file is part of spider.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import logging

import motor
import uuid

from tornado import gen

from howler.messages import inbound


class Inbound(object):
    '''
        Inbound call resources
    '''
    pass