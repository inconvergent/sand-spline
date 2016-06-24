# -*- coding: utf-8 -*-

from __future__ import print_function

from render.render import Animate
from fn import Fn

from numpy import pi
from numpy import linspace
from numpy import column_stack
from numpy import array
from numpy import dstack
from numpy import concatenate
from numpy import transpose
from numpy import zeros
from numpy.random import random
from scipy.interpolate import splprep
from scipy.interpolate import splev


TWOPI = pi*2
HPI = pi*0.5

BACK = [1,1,1,1]
FRONT = [0,0,0,0.1]
LIGHT = [0,0,0,0.05]


class Sand(object):

  def __init__(
      self,
      size,
      prefix = './res/',
      back = BACK
    ):

    self.size = size
    self.one = 1.0/size

    self.fn = Fn(prefix=prefix, postfix='.png')
    self.render = Animate(size, back, FRONT, self.wrap)

    self.render.set_line_width(self.one)

    self.__init()

  def __init(self):
    self.xy = random(size=(10,2))
    self.interpolated_xy = self._interpolate(self.xy, 100)

  def _random_in_range(self, a, b):
    return a + random()*(b-a)

  def _interpolate(self, xy, num_points=100):
    tck,u = splprep([
      xy[:,0],
      xy[:,1]],
      s=0
    )

    unew = linspace(0, 1, num_points)
    out = splev(unew, tck)

    return column_stack(out)

  def draw(self, render):
    render.path(self.interpolated_xy)

  def wrap(self, render):
    self.step()
    self.draw(render)

    # self.render.write_to_png(self.fn.name())

    return False

