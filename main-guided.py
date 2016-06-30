#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

from numpy import pi
from numpy.random import randint
from numpy.random import random

from numpy import linspace
from numpy import arange
from numpy import zeros
from numpy import ones
from numpy import column_stack
from numpy import cos
from numpy import sin

from modules.helpers import _interpolate

TWOPI = 2.0*pi

BACK = [1,1,1,1]
FRONT = [0,0,0,0.05]
LIGHT = [0,0,0,0.05]

SIZE = 5000
PIX = 1.0/SIZE

GRID_X = 20
GRID_Y = 20
GNUM = 5

EDGE = 0.08
RAD = 0.5-EDGE
LEAP_X = (1.0-2*EDGE)/(GRID_X-1)*0.5*0.75
LEAP_Y = (1.0-2*EDGE)/(GRID_Y-1)*0.5*0.75

STEPS = 300
INUM = 2000


STP = 0.00001


GRAINS = 1


print('LEAP_Y', LEAP_Y)
print('LEAP_X', LEAP_X)
# print('STEPS', STEPS)
print('INUM', INUM)


def draw(render, xy):
  points = column_stack((xy[1:,:], xy[:-1,:]))
  render.sandstroke(points,GRAINS)

def spline_iterator():
  from modules.guidedSandSpline import GuidedSandSpline

  itt = 0
  for i, x in enumerate(linspace(EDGE, 1.0-EDGE, GRID_X)):
    for j, y in enumerate(linspace(EDGE, 1.0-EDGE, GRID_Y)):
      itt += 1

      ## horizontal line
      # gx = linspace(x-LEAP_X,x+LEAP_X,GNUM,'float')
      # gy = y*ones(GNUM,'float')
      # guide = _interpolate(column_stack((gx, gy)), STEPS)

      ## same position
      gx = x*ones((i+1)*10,'float')
      gy = y*ones((i+1)*10,'float')
      guide = column_stack((gx, gy))

      pnum = 10+j

      ## vertical line
      # px = zeros(pnum,'float')
      # py = linspace(-1,1,pnum,'float')*LEAP_Y
      # path = column_stack((px, py))

      ## circle
      a = random()*TWOPI + linspace(0, TWOPI, pnum)
      px = cos(a)
      py = sin(a)
      path = column_stack((px, py)) * LEAP_Y

      scale = arange(pnum).astype('float')*STP

      s = GuidedSandSpline(
          guide,
          path,
          INUM,
          scale
          )
      yield itt, s


def main():

  from render.render import Animate
  from fn import Fn


  fn = Fn(prefix='./res/', postfix='.png')
  si = spline_iterator()

  def wrap(render):
    import sys, traceback
    try:
      i, spline = si.next()
      if not i%5:
        print(i)
        render.write_to_png(fn.name())
      for xy in spline:
        draw(render, xy)
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

