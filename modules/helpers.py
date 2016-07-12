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

def get_colors(f, do_shuffle=True):
  from numpy import array
  try:
    import Image
  except Exception:
    from PIL import Image

  im = Image.open(f)
  data = array(list(im.convert('RGB').getdata()),'float')/255.0

  res = []
  for rgb in data:
    res.append(list(rgb))

  if do_shuffle:
    from numpy.random import shuffle
    shuffle(res)
  return res

def get_img_as_rgb_array(f):
  from PIL import Image
  from numpy import array
  from numpy import reshape
  im = Image.open(f)
  w,h = im.size
  data = array(list(im.convert('RGB').getdata()), 'float')/255.0
  return reshape(data,(w,h,3))

