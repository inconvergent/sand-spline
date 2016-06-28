# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division


from numpy import pi
from numpy import column_stack
from numpy import sin
from numpy import cos
from numpy import arange
from numpy import reshape
from numpy import zeros
from numpy.random import random

from helpers import _interpolate


TWOPI = pi*2
HPI = pi*0.5

class GuidedSandSpline(object):
  def __init__(
      self,
      guide,
      path,
      inum,
      steps,
      stp
      ):
    self.steps = steps
    self.inum = inum
    self.path = path
    self.stp = stp

    self.pnum =len(path)
    self.interpolated_path = _interpolate(path, inum)
    self.guide = _interpolate(guide, steps)
    self.noise = zeros(self.pnum,'float')
    self.i = 0

  def __iter__(self):
      return self

  def next(self):
    if self.i>=self.steps:
      raise StopIteration

    pnum = self.pnum

    r = (1.0-2.0*random(pnum))
    scale = arange(pnum).astype('float')
    # print(self.noise, scale)
    self.noise[:] += r*scale*self.stp

    a = random(pnum)*TWOPI
    rnd = column_stack((cos(a), sin(a)))

    self.path += rnd * reshape(self.noise, (self.pnum,1))
    self.interpolated_path = _interpolate(self.path, self.inum)

    self.i+=1
    return self.guide[self.i-1, :] + self.interpolated_path

