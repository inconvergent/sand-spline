#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import print_function

BACK = [1,1,1,1]
FRONT = [0,0,0,0.05]
LIGHT = [0,0,0,0.05]

SIZE = 2000

EDGE = 0.15
RAD = 0.5-EDGE

INUM = 400
SNUM = 20

NOISE_STP = 0.005


def main():

  from modules.sand import Sand
  from render.render import Animate
  from fn import Fn

  from numpy.random import randint


  fn = Fn(prefix='./res/', postfix='.png')

  sand = Sand(
      SIZE,
      INUM,
      NOISE_STP,
      fn
      )
  sand.init(sorted(randint(20,70,20)), RAD)

  render = Animate(SIZE, BACK, FRONT, sand.wrap)
  render.set_line_width(sand.one)
  render.transparent_pix()
  render.set_front(FRONT)

  render.start()


if __name__ == '__main__':
  main()

