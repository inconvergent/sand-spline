# -*- coding: utf-8 -*-


from scipy.interpolate import splprep
from scipy.interpolate import splev
from numpy.random import random
from numpy import linspace
from numpy import column_stack
from numpy import sort

def _interpolate(xy, num_points):
  tck,u = splprep([
    xy[:,0],
    xy[:,1]],
    s=0
  )
  unew = linspace(0, 1, num_points)
  out = splev(unew, tck)
  return column_stack(out)

def _rnd_interpolate(xy, num_points, ordered=False):
  tck,u = splprep([
    xy[:,0],
    xy[:,1]],
    s=0
  )
  unew = random(num_points)
  if sort:
    unew = sort(unew)
  out = splev(unew, tck)
  return column_stack(out)

def get_colors(f):
  try:
    import Image
  except Exception:
    from PIL import Image
  from numpy.random import shuffle

  scale = 1./255.
  im = Image.open(f)
  w,h = im.size
  rgbim = im.convert('RGB')
  res = []
  for i in range(w):
    for j in range(h):
      r,g,b = rgbim.getpixel((i,j))
      res.append([r*scale,g*scale,b*scale])

  shuffle(res)
  return res

def get_img_size(f):
  from PIL import Image
  im = Image.open(f)
  w,h = im.size
  return w,h

