# -*- coding: utf-8 -*-

"""
DOA for ReSpeaker 4 Mic Linear Array
"""

import collections

import numpy as np

from voice_engine.element import Element
from voice_engine.gcc_phat import gcc_phat

SOUND_SPEED = 340.0

MIC_DISTANCE = 0.1496
MAX_TDOA = MIC_DISTANCE / float(SOUND_SPEED)


class DOA(Element):
    def __init__(self, rate=16000, chunks=50):
        super(DOA, self).__init__()

        self.queue = collections.deque(maxlen=chunks)
        self.sample_rate = rate

    def put(self, data):
        self.queue.append(data)

        super(DOA, self).put(data)

    def get_direction(self):
        buf = b''.join(self.queue)
        buf = np.fromstring(buf, dtype='int16')
        tau, _ = gcc_phat(buf[0::8], buf[3::8], fs=self.sample_rate, max_tau=MAX_TDOA, interp=4)
        theta = np.arcsin(tau / MAX_TDOA) * 180 / np.pi

        return theta
