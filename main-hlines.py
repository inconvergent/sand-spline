#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

from numpy import pi
from numpy import array

from numpy import linspace
from numpy import arange
from numpy import zeros
from numpy import column_stack

TWOPI = 2.0*pi

BACK = [1,1,1,1]
FRONT = [0,0,0,0.05]
LIGHT = [0,0,0,0.05]

SIZE = 5000
PIX = 1.0/SIZE

GRID_Y = 40
GNUM = 5

EDGE = 0.08
RAD = 0.5-EDGE
LEAP_Y = (1.0-2*EDGE)/(GRID_Y-1)*0.5*0.75

STEPS = 300
INUM = 5000

STP = 0.000001


def f(x, y):
  while True:
    yield array([[x,y]])

def spline_iterator():
  from modules.sandSpline import SandSpline

  splines = []
  for i, y in enumerate(linspace(EDGE, 1.0-EDGE, GRID_Y)):
    pnum = 4+i
    guide = f(0.5,y)

    ## hlines
    x = linspace(-1,1.0, pnum)*(1.0-2*EDGE)*0.5
    y = zeros(pnum,'float')
    path = column_stack([x,y])

    scale = arange(pnum).astype('float')*STP

    s = SandSpline(
        guide,
        path,
        INUM,
        scale
        )
    splines.append(s)

  itt = 0
  while True:
    for s in splines:
      xy = s.next()
      itt += 1
      yield itt, xy


def main():

  import sys, traceback
  from render.render import Animate
  from modules.helpers import draw
  from fn import Fn


  fn = Fn(prefix='./res/', postfix='.png')
  si = spline_iterator()

  def wrap(render):
    try:
      itt, xy = si.next()
      draw(render, xy)
      if not itt%GRID_Y:
        print(itt)
        render.write_to_png(fn.name())
      return True
    except StopIteration:
      render.write_to_png(fn.name())
      return False
    except Exception:
      render.write_to_png(fn.name())
      traceback.print_exc(file=sys.stdout)
      return False

  render = Animate(SIZE, BACK, FRONT, wrap)
  render.set_line_width(PIX)
  render.transparent_pix()
  render.set_front(FRONT)
  render.start()


if __name__ == '__main__':
  main()

