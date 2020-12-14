#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyfiglet
from .entities import *

class Figlet:
    def __init__(self, text='', font='standard', direction='auto', justify='auto'):
        self.text = text
        self.font = font
        self.dir = direction
        self.just = justify
        
    def draw(self, w=60, h=6):
        fig = pyfiglet.Figlet(self.font, self.dir, self.just, w).renderText(self.text)
        drawing = Drawing(w,h)
        drawing.overlay_string(fig)
        return drawing
