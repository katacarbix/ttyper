#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math
import PIL.Image

from .entities import *

class Image:
	def __init__(self, path=''):
		self.img = PIL.Image.open(path).convert(mode='RGBA')
		self.size = self.w,self.h = self.img.size
	
	def draw(self, w=0, h=0, alpha_thresh=127):
		if (w,h) in [(0,0), self.size, (self.w,0), (0,self.h)]:
			w,h = self.size
			b = self.img.tobytes()
		else:
			if w > 0 and h == 0:
				h = round(w/self.w*self.h)
			elif h > 0 and w == 0:
				w = round(h/self.h*self.w)
			b = self.img.resize((w,h), resample=PIL.Image.LANCZOS).tobytes()
			
		upper_block = '\u2580'
		lower_block = '\u2584'
		def make_pair(t=(0,0,0,0), b=(0,0,0,0)):
			if t[3] <= alpha_thresh and b[3] <= alpha_thresh:
				return Char()
			if t[3] <= alpha_thresh:
				return Char(lower_block, fg=b[:3])
			elif b[3] <= alpha_thresh:
				return Char(upper_block, fg=t[:3])
			else:
				return Char(upper_block, fg=t[:3], bg=b[:3])
		
		drawing = Drawing(w, math.ceil(h/2.0))
		x = y = 0
		it = 0
		ib = w*4
		while True:
			rt = int(b[it])
			gt = int(b[it+1])
			bt = int(b[it+2])
			at = int(b[it+3])
			if ib >= len(b):
				rb = gb = bb = ab = 0
			else:
				rb = int(b[ib])
				gb = int(b[ib+1])
				bb = int(b[ib+2])
				ab = int(b[ib+3])
			
			drawing.put(x,y, make_pair((rt,gt,bt,at),(rb,gb,bb,ab)))
			
			x += 1
			it += 4
			ib += 4
			if it % (w*4) == 0:
				it += w*4
				ib += w*4
				x = 0
				y += 1
			if it >= len(b): return drawing
