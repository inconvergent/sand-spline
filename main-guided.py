#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

from numpy import pi
from numpy.random import random
from numpy import linspace
from numpy import zeros
from numpy import ones
from numpy import column_stack

TWOPI = 2.0*pi

BACK = [1,1,1,1]
FRONT = [0,0,0,0.05]
LIGHT = [0,0,0,0.05]

SIZE = 2000
PIX = 1.0/SIZE

EDGE = 0.08
RAD = 0.5-EDGE

NOISE_STP = 0.005

GRAINS = 1

GRID_SIZE = 6

GNUM = 5
PNUM = 5

INUM = 500
STEPS = 500
N = 10

GUIDE_NOISE = 0.05
STP = 0.00005

def draw(render, xy):
  points = column_stack((xy[1:,:], xy[:-1,:]))
  render.sandstroke(points,GRAINS)


def spline_iterator():
  from modules.guidedSandSpline import GuidedSandSpline

  i = 0
  leap = (1.0-2*EDGE)/(GRID_SIZE-1)*0.5*0.5
  print('leap', leap)

  for i, a in enumerate(linspace(EDGE, 1.0-EDGE, GRID_SIZE)):
    for j, b in enumerate(linspace(EDGE, 1.0-EDGE, GRID_SIZE)):
      i += 1
      gx = linspace(a-leap,a+leap,GNUM,'float')
      gy = b*ones(GNUM,'float')
      # gy = linspace(b-leap,b+leap,PNUM,'float')
      # gy = b+sorted((1.0-2.0*random(size=GNUM))*GUIDE_NOISE)
      guide = column_stack((gx, gy))

      px = zeros(PNUM,'float')
      py = linspace(-1,1,PNUM,'float')*leap
      path = column_stack((px, py))

      s = GuidedSandSpline(
          guide,
          path,
          inum=INUM,
          steps=STEPS,
          stp=STP
          )
      yield i, s


def main():

  from render.render import Animate
  from fn import Fn

  import sys, traceback


  fn = Fn(prefix='./res/', postfix='.png')

  si = spline_iterator()

  def wrap(render):
    try:
      i, spline = si.next()
      print(i)
      for xy in spline:
        # print(xy)
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

