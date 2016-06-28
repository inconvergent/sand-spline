# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

from scipy.interpolate import splprep
from scipy.interpolate import splev
from numpy import linspace
from numpy import column_stack

def _interpolate(xy, num_points):
  tck,u = splprep([
    xy[:,0],
    xy[:,1]],
    s=0
  )
  unew = linspace(0, 1, num_points)
  out = splev(unew, tck)
  return column_stack(out)

