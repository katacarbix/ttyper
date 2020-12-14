#!/usr/bin/env python3
# -*- coding: utf-8 -*-

SPACE = ' '
ESCAPE = '\x1b['
RESET = ESCAPE + '0m'

class Drawing:
    def __init__(self, w=0, h=0):
        if w <= 0 or h <= 0:
            raise ValueError('Width and height must be greater than zero.')
        self.w = w
        self.h = h
        self.data = []
        for y in range(h):
            self.data.append([Char() for x in range(w)])
    
    def put(self, x=None, y=None, val=None):
        if x is None or y is None:
            raise ValueError('You must specify an x and y value.')
        if type(x) not in (int,float):
            raise TypeError(f'Unexpected x of type {type(x)}.')
        if type(y) not in (int,float):
            raise TypeError(f'Unexpected y of type {type(y)}.')
        
        if type(x) is float and x>=-1 and x<=1:
            x = round(x*(self.w-1))
        if type(y) is float and y>=-1 and y<=1:
            y = round(y*(self.h-1))
        
        if val is None:
            val = Char()
        
        self.data[y][x] = val
    
    def overlay_string(self, input='', x=0,y=0, fg=None, bg=None):
        ix = x
        iy = y
        for line in input.split('\n'):
            for c in line:
                if c != SPACE: self.put(ix+x, iy+y, Char(c, fg, bg))
                ix += 1
                if ix >= self.w: break
            ix = 0
            iy += 1
            if iy >= self.h: break
    
    def put_color(self, x=None, y=None, fg=None, bg=None):
        if x is None or y is None:
            raise ValueError('You must specify an x and y value.')
        if type(x) not in (int,float):
            raise TypeError(f'Unexpected x of type {type(x)}.')
        if type(y) not in (int,float):
            raise TypeError(f'Unexpected y of type {type(y)}.')
        
        if type(x) is float and x>=-1 and x<=1:
            x = round(x*(self.w-1))
        if type(y) is float and y>=-1 and y<=1:
            y = round(y*(self.h-1))
            
        if fg is not None:
            self.data[y][x].set_fg(fg)
        if bg is not None:
            self.data[y][x].set_bg(bg)
    
    def __str__(self):
        output = ''
        for y in range(self.h):
            for x in range(self.w):
                output += str(self.data[y][x])
            if y < self.h:
                output += '\n'
        return output


class Char:
    def __init__(self, val=SPACE, fg=None, bg=None, reset=True):
        if type(val) is not str:
            raise TypeError('Value must be a string of length 1.')
        if len(val) != 1:
            raise ValueError('Value must be a string of length 1.')
        if val is None:
            val = SPACE
        self.val = val
        
        if type(fg) is tuple and len(fg) == 3:
            self.fg = Color(*fg)
        elif type(fg) is Color or fg is None:
            self.fg = fg
        else:
            raise TypeError('Unrecognized foreground color.')
        
        if type(bg) is tuple and len(bg) == 3:
            self.bg = Color(*bg)
        elif type(bg) is Color or bg is None:
            self.bg = bg
        else:
            raise TypeError('Unrecognized background color.')
            
        if fg is None and bg is None:
            reset = False
        self.reset = reset
    
    def set_fg(c=None):
        if type(c) is tuple and len(c) == 3:
            self.fg = Color(*c)
        elif type(c) is Color or c is None:
            self.fg = c
        else:
            raise TypeError('Unrecognized foreground color.')
    
    def set_bg(c=None):
        if type(c) is tuple and len(c) == 3:
            self.bg = Color(*c)
        elif type(c) is Color or c is None:
            self.bg = c
        else:
            raise TypeError('Unrecognized background color.')
    
    def __str__(self):
        return f"{self.fg.make_code('fg') if type(self.fg) is Color and self.val != SPACE else ''}{self.bg.make_code('bg') if type(self.bg) is Color else ''}{self.val}{RESET if self.reset else ''}"
        

class Color:
    def __init__(self, r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b
    
    def make_code(self, mode='fg'):
        joined = ';'.join(map(str, (self.r,self.g,self.b)))
        if mode == 'fg':
        	return ESCAPE+'38;2;'+joined+'m'
        if mode == 'bg':
        	return ESCAPE+'48;2;'+joined+'m'
        
