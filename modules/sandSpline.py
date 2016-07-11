# -*- coding: utf-8 -*-

from numpy import pi
from numpy import column_stack
from numpy import sin
from numpy import cos
from numpy import reshape
from numpy import zeros
from numpy.random import random

from .helpers import _rnd_interpolate

ORDERED = True


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
    self.interpolated_path = _rnd_interpolate(path, inum, ordered=ORDERED)
    self.guide = guide
    self.noise = zeros(self.pnum,'float')
    self.i = 0

  def __iter__(self):
      return self

  def __next__(self):
    try:
      g = next(self.guide)
    except Exception:
      raise StopIteration

    pnum = self.pnum

    r = 1.0-2.0*random(pnum)
    self.noise[:] += r*self.scale

    a = random(pnum)*TWOPI
    rnd = column_stack((cos(a), sin(a)))

    self.path += rnd * reshape(self.noise, (self.pnum,1))
    self.interpolated_path = _rnd_interpolate(self.path, self.inum, ordered=ORDERED)

    self.i+=1
    return g + self.interpolated_path

