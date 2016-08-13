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
FRONT = [0,0,0,0.001]

SIZE = 13000

EDGE = 0.08

INUM = 20*SIZE

STP = 0.0000003*0.15

GAMMA = 1.5


def f():
  for x in linspace(EDGE, 1.0-EDGE, SIZE*10):
    yield array([[x, 0.0]])

def spline_iterator():
  from modules.sandSpline import SandSpline

  splines = []
  guide = f()

  pnum = randint(4,100)
  px = zeros(pnum,'float')
  py = linspace(EDGE, 1.0-EDGE, pnum)
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

  sand = Sand(SIZE)
  sand.set_bg(BG)
  sand.set_rgba(FRONT)

  fn = Fn(prefix='./res/', postfix='.png')
  si = spline_iterator()

  while True:
    try:
      itt, w, xy = next(si)
      sand.paint_dots(xy)
      if not itt%(SIZE):
        print(itt)
      #   sand.write_to_png(fn.name(), GAMMA)
    except Exception as e:
      print(e)
      sand.write_to_png(fn.name(), GAMMA)
      traceback.print_exc(file=sys.stdout)
      return


if __name__ == '__main__':
  main()

