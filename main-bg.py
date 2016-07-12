#!/usr/bin/python3
# -*- coding: utf-8 -*-

from numpy import pi
from numpy import array

from numpy import linspace
from numpy.random import random
from numpy.random import randint
from numpy import zeros
from numpy import arange
from numpy import column_stack
from numpy import cos
from numpy import sin
from modules.helpers import get_img_as_rgb_array

BG = [1,1,1,1]
BACK = [1,1,1,1]
FRONT = [0,0,0,0.5]

TWOPI = 2.0*pi


IMGNAME = './img/check-bw.png'
img = get_img_as_rgb_array(IMGNAME)
SIZE = img.shape[0]

PIX = 1.0/SIZE

CNUM = 50

INUM = 4000

STP = 0.000001

GRID_X = SIZE*20


# def f():
#   x = random()
#   y = random()
#   while True:
#     yield array([[x,y]])

# def spline_iterator():
#   from modules.sandSpline import SandSpline
#
#   splines = []
#   for _ in range(CNUM):
#     guide = f()
#
#     pnum = randint(10, 100)
#     crad = 0.01 + 0.1*random()
#
#     a = random()*TWOPI + linspace(0, TWOPI, pnum)
#     path = column_stack((cos(a), sin(a))) * crad
#
#     scale = arange(pnum).astype('float')*STP
#
#     s = SandSpline(
#         guide,
#         path,
#         INUM,
#         scale
#         )
#     splines.append(s)
#
#   itt = 0
#   while True:
#     for s in splines:
#       xy = next(s)
#       itt += 1
#       yield itt, xy

def f():
  for x in linspace(0, 1.0, GRID_X):
    yield array([[x,0]])

def spline_iterator():
  from modules.sandSpline import SandSpline

  splines = []
  pnum = 10
  guide = f()

  y = linspace(0,1.0, pnum)
  x = zeros(pnum,'float')
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
      xy = next(s)
      itt += 1
      yield itt, xy


def main():
  import sys, traceback
  from fn import Fn
  from sand import Sand

  sand = Sand(SIZE)
  sand.set_bg_from_rgb_array(img)
  sand.set_rgba(FRONT)

  fn = Fn(prefix='./res/', postfix='.png')
  si = spline_iterator()

  while True:
    try:
      itt, xy = next(si)
      # sand.distort_dots_swap(xy)
      sand.distort_dots_wind(xy)

      if not itt%5000:
        print(itt)
        sand.write_to_png(fn.name())
    except Exception:
      sand.write_to_png(fn.name())
      traceback.print_exc(file=sys.stdout)
      return


if __name__ == '__main__':
  main()

