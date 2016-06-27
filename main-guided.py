#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

from numpy import pi
# from numpy.random import randint
from numpy.random import random
from numpy import linspace
from numpy import column_stack
from numpy import sin
from numpy import cos
from numpy import ones

TWOPI = 2.0*pi

BACK = [1,1,1,1]
FRONT = [0,0,0,0.05]
LIGHT = [0,0,0,0.05]

SIZE = 2000

EDGE = 0.15
RAD = 0.5-EDGE

INUM = 2000
NOISE_STP = 0.005


def main():

  from modules.guidedSandSpline import GuidedSandSpline
  from render.render import Animate
  from fn import Fn


  fn = Fn(prefix='./res/', postfix='.png')

  sand = GuidedSandSpline(
      SIZE,
      INUM,
      NOISE_STP,
      fn
      )


  ## sphere
  snum = 60
  a = linspace(0,TWOPI, snum)
  xy = 0.5+column_stack((cos(a), sin(a)))*RAD
  sand.init(xy)

  render = Animate(SIZE, BACK, FRONT, sand.wrap)
  render.set_line_width(sand.one)
  render.transparent_pix()
  render.set_front(FRONT)

  render.start()


if __name__ == '__main__':
  main()

