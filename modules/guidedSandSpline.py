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


class GuidedSandSpline(object):
  def __init__(
      self,
      size,
      inum,
      noise_stp,
      fn
      ):

    self.itt = 0

    self.size = size
    self.one = 1.0/size
    self.inum = inum
    self.noise_stp = noise_stp

    self.fn = fn

    self.grains = 1

    self.xy = []
    self.interpolated_xy = []
    self.noise = []
    self.snums = []

  def init(self, xy):
    snum = len(xy)
    self.snums.append(snum)
    interp = self._interpolate(xy, self.inum)
    noise = zeros((snum,1), 'float')
    self.noise.append(noise)
    self.xy.append(xy)
    self.interpolated_xy.append(interp)

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
    for xy in self.interpolated_xy:
      points = column_stack((xy[1:,:], xy[:-1,:]))
      render.sandstroke(points,self.grains)

  def step(self):
    self.itt+=1

    inum = self.inum
    one = self.one
    noise_stp = self.noise_stp

    new_interpolated = []

    for snum,xy,noise in zip(self.snums, self.xy, self.noise):
      r = (1.0-2.0*random((snum,1)))
      scale = reshape(arange(snum).astype('float'), (snum,1))
      noise[:] += r*scale*noise_stp

      a = random(snum)*TWOPI
      rnd = column_stack((cos(a), sin(a)))
      xy[:,:] += rnd * one*noise
      new_interpolated.append(self._interpolate(xy,inum))

    self.interpolated_xy = new_interpolated

    return True

  def wrap(self, render):
    res = self.step()
    self.draw(render)

    if not self.itt%50:
      name = self.fn.name()
      print(self.itt, name)
      render.write_to_png(name)

    return res

