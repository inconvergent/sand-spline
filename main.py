#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import print_function

BACK = [1,1,1,1]
FRONT = [0,0,0,0.05]
LIGHT = [0,0,0,0.05]



def main():

  from modules.sand import Sand
  from render.render import Animate
  from fn import Fn

  size = 2000

  fn = Fn(prefix='./res/', postfix='.png')

  sand = Sand(size, fn)
  sand.init()

  render = Animate(size, BACK, FRONT, sand.wrap)
  render.set_line_width(sand.one)
  render.transparent_pix()
  render.set_front(FRONT)

  render.start()


if __name__ == '__main__':
  main()

