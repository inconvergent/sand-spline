# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division


from numpy import pi
from numpy import column_stack
from numpy import sin
from numpy import cos
from numpy import reshape
from numpy import zeros
from numpy.random import random

from helpers import _interpolate


TWOPI = pi*2
HPI = pi*0.5

class SandSpline(object):
  def __init__(
      self,
      guide,
      path,
      inum,
      scale
      ):
    self.inum = inum
    self.path = path
    self.scale = scale

    self.pnum = len(path)
    self.interpolated_path = _interpolate(path, inum)
    self.guide = guide
    self.noise = zeros(self.pnum,'float')
    self.i = 0

  def __iter__(self):
      return self

  def next(self):
    try:
      g = self.guide.next()
    except Exception:
      raise StopIteration

    pnum = self.pnum

    r = (1.0-2.0*random(pnum))
    self.noise[:] += r*self.scale

    a = random(pnum)*TWOPI
    rnd = column_stack((cos(a), sin(a)))

    self.path += rnd * reshape(self.noise, (self.pnum,1))
    self.interpolated_path = _interpolate(self.path, self.inum)

    self.i+=1
    return g + self.interpolated_path

