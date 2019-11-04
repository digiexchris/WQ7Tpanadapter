# FreqShow main application and configuration.
# Author: Tony DiCola (tony@tonydicola.com)
#
# The MIT License (MIT)
#
# Copyright (c) 2014 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# Enhancements over the original Freqshow by Dan Stixrud, WQ7T
import os
import time

import pygame

import controller
import model
import ui
import yaml

# Application configuration.

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

for i in cfg:
    print(i, cfg[i])

#SDR_SAMPLE_SIZE = 512  # Number of samples per frequency bin to grab from the radio. See config.yml.example Should be
#SDR_SAMPLE_SIZE = 1024	 # larger than the maximum display width.
#SDR_SAMPLE_SIZE = 2048
#SDR_SAMPLE_SIZE = 4096
#SDR_SAMPLE_SIZE = 8192  # This ithe default value to allow zooming the display to a 10kHz span in 320 pixels with a sample rate of 0.230 MHz.
#SDR_SAMPLE_SIZE = 16384				

SDR_SAMPLE_SIZE = cfg['SDR_SAMPLE_SIZE']

#Number of seconds to wait between touch events to keep it from flapping
# set to a few hunded milliseconds to prevent accidental
# double clicks from hard screen presses.
CLICK_DEBOUNCE  = 0.04

# Font size configuration.
MAIN_FONT = cfg['MAIN_FONT']
NUM_FONT  = cfg['NUM_FONT']

# Color configuration (RGB tuples, 0 to 255).
MAIN_BG        = ( 5,   45,  45) # Dark Brown
INPUT_BG       = MAIN_BG
INPUT_FG       = ( 60, 255, 255) # Cyan-ish
CANCEL_BG      = MAIN_BG
ACCEPT_BG      = MAIN_BG
BUTTON_BG      = MAIN_BG
BUTTON_FG      = INPUT_FG 
BUTTON_BORDER  = MAIN_BG
SYMBOL_FG      =  ( 255, 255,  0) # Bright Yellow
INSTANT_LINE   = ( 150, 255, 255) # Bright yellow green.
GRID_LINE      = (  119, 119, 130) # Light Grey
GRID_BG        = (  10,  10,  30) # Dark Blue
CENTER_LINE    = ( 125, 0,   0) # Red
BLACK	       = (   0, 0,   0) # Black
LINE_SHADOW      = (  96, 96, 96) # Medium Grey

# Define gradient of colors for the waterfall graph.  Gradient goes from blue to
# yellow to cyan to red.
WATERFALL_GRAD = [(0, 0, 255), (0, 255, 255), (255, 255, 0), (255, 0, 0)]

# Configure default UI and button values.
ui.MAIN_FONT = MAIN_FONT
ui.Button.fg_color     = BUTTON_FG
ui.Button.bg_color     = BUTTON_BG
ui.Button.border_color = BUTTON_BORDER
ui.Button.padding_px   = 2
ui.Button.border_px    = 2


if __name__ == '__main__':
	# Initialize pygame and SDL to use the PiTFT display and touchscreen.
	os.putenv('SDL_VIDEODRIVER', 'fbcon')
	os.putenv('SDL_FBDEV'      , cfg['VIDEO_DEVICE'])
	os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
	os.putenv('SDL_MOUSEDEV'   , cfg['TOUCHSCREEN_DEVICE'])
	pygame.display.init()
	pygame.font.init()
	pygame.mouse.set_visible(True)
	# Get size of screen and create main rendering surface.
	size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
	screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
	# Display splash screen.
	splash = pygame.image.load('freqshow_splash.png')
	screen.fill(MAIN_BG)
	screen.blit(splash, ui.align(splash.get_rect(), (0, 0, size[0], size[1])))
	pygame.display.update()
	splash_start = time.time()
	# Create model and controller.
	fsmodel = model.FreqShowModel(size[0], size[1])
	fscontroller = controller.FreqShowController(fsmodel)
	time.sleep(2.0)
	# Main loop to process events and render current view.
	lastclick = 0
	while True:
		# Process any events (only mouse events for now).
		for event in pygame.event.get():
			if event.type is pygame.MOUSEBUTTONDOWN \
				and (time.time() - lastclick) >= CLICK_DEBOUNCE:
				lastclick = time.time()
				fscontroller.current().click(pygame.mouse.get_pos())
		# Update and render the current view.
		fscontroller.current().render(screen)
		pygame.display.update()
