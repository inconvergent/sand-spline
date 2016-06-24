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
from numpy import zeros
from numpy.random import random
from scipy.interpolate import splprep
from scipy.interpolate import splev


TWOPI = pi*2
HPI = pi*0.5

EDGE = 0.2
RAD = 0.5-EDGE

INUM = 1000
SNUM = 200

NOISE = 0.001


class Sand(object):

  def __init__(
      self,
      size,
      fn,
      inum = INUM
    ):

    self.itt = 0

    self.size = size
    self.one = 1.0/size
    self.inum = inum

    self.fn = fn

    self.grains = 1

  def init(self, n=SNUM, rad=RAD):
    a = sorted(random(n)*TWOPI)
    self.xy = 0.5+column_stack((cos(a), sin(a)))*rad

    self.noise = zeros((n,1), 'float')
    self.interpolated_xy = self._interpolate(self.xy, self.inum)
    self.interpolated_xy_old = self.interpolated_xy[:,:]

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
    # points = column_stack((self.interpolated_xy, self.interpolated_xy_old))
    # render.sandstroke(points,self.grains)

  def step(self):
    self.itt+=1

    n = len(self.xy)

    r = (1.0-2.0*random((len(self.noise),1)))
    scale = reshape(arange(n).astype('float'), (n,1))
    self.noise[:] += r*scale*NOISE

    a = random(len(self.xy))*TWOPI
    rnd = column_stack((cos(a), sin(a)))
    self.xy[:,:] += rnd * self.one*self.noise
    self.interpolated_xy_old[:,:] = self.interpolated_xy[:,:]
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

