# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division


from numpy import pi
from numpy import linspace
from numpy import column_stack
from numpy import sin
from numpy import cos
from numpy import arange
from numpy import reshape
from numpy import ones
from numpy.random import random
from scipy.interpolate import splprep
from scipy.interpolate import splev


TWOPI = pi*2
HPI = pi*0.5

EDGE = 0.3
RAD = 0.5-EDGE


class Sand(object):

  def __init__(
      self,
      size,
      fn,
      inum = 100
    ):

    self.itt = 0

    self.size = size
    self.one = 1.0/size
    self.inum = inum

    self.fn = fn

    self.grains = 5

  def init(self, n=10, rad=RAD):
    # a = sorted(random(n)*TWOPI)
    # a = random(n)*TWOPI
    a = linspace(0, TWOPI, n)
    self.xy = 0.5+column_stack((cos(a), sin(a)))*rad

    self.noise = ones((n,1), 'float')
    self.interpolated_xy = self._interpolate(self.xy, self.inum)

  def _interpolate(self, xy, num_points):
    tck,u = splprep([
      xy[:,0],
      xy[:,1]],
      s=0
    )
    unew = linspace(0, 1, num_points)
    out = splev(unew, tck)
    return column_stack(out)

  def draw(self, render):
    xy = self.interpolated_xy
    points = column_stack((xy[1:,:], xy[:-1,:]))
    render.sandstroke(points,self.grains)

  def step(self):
    self.itt+=1


    self.noise[:] += (1.0-2.0*random((len(self.noise),1)))*0.01

    a = random(len(self.xy))*TWOPI
    rnd = column_stack((cos(a), sin(a)))

    scale = reshape(arange(len(rnd)).astype('float'), (len(rnd),1))

    scale *= self.one/3.0
    scale *= self.noise
    self.xy[:,:] += rnd*scale
    self.interpolated_xy = self._interpolate(self.xy,self.inum)

    return True

  def wrap(self, render):
    res = self.step()
    self.draw(render)

    if not self.itt%100:
      name = self.fn.name()
      print(self.itt, name)
      render.write_to_png(name)

    return res

