#!/usr/bin/python3
# -*- coding: utf-8 -*-

from numpy.random import randint
from numpy import linspace
from numpy import arange
from numpy import zeros
from numpy import column_stack
from numpy import pi
from numpy import array

BG = [1,1,1,1]
FRONT = [0,0,0,0.05]


TWOPI = 2.0*pi

BACK = [1,1,1,1]
FRONT = [0,0,0,0.05]

SIZE = 1000
PIX = 1.0/SIZE

GRID_Y = 20
GRID_X = 20
GNUM = 5

EDGE = 0.08
RAD = 0.5-EDGE
LEAP_Y = (1.0-2*EDGE)/(GRID_Y-1)*0.5
LEAP_X = (1.0-2*EDGE)/(GRID_X-1)*0.5

GNUM = 600
INUM = 300

STP = 0.0000003


def f(x, y):
  for xx in x-linspace(-1, 1, GNUM)*LEAP_X:
    yield array([[xx,y]])

def spline_iterator():
  from modules.sandSpline import SandSpline

  splines = []
  for i, x in enumerate(linspace(EDGE, 1.0-EDGE, GRID_X)):
    for j, y in enumerate(linspace(EDGE, 1.0-EDGE, GRID_Y)):
      guide = f(x,y)

      pnum = randint(4,100)
      px = zeros(pnum,'float')
      py = linspace(-1,1.0, pnum)*LEAP_Y
      path = column_stack([px,py])

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
    for w, s in enumerate(splines):
      xy = next(s)
      itt += 1
      yield itt, w, xy


def main():
  import sys, traceback
  from fn import Fn
  from sand import Sand
  from modules.helpers import get_colors

  sand = Sand(SIZE)
  sand.set_bg(BG)
  sand.set_rgba(FRONT)

  colors = get_colors('../colors/shimmering.gif')
  nc = len(colors)

  fn = Fn(prefix='./res/', postfix='.png')
  si = spline_iterator()

  while True:
    try:
      itt, w, xy = next(si)
      rgba = colors[w%nc] + [0.005]
      sand.set_rgba(rgba)
      sand.paint_dots(xy)
      if not itt%(10*GRID_X*GRID_Y):
        print(itt)
        sand.write_to_png(fn.name())
    except Exception as e:
      print(e)
      sand.write_to_png(fn.name())
      traceback.print_exc(file=sys.stdout)
      return


if __name__ == '__main__':
  main()

