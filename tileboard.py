import appdaemon.plugins.hass.hassapi as hass
import os, os.path
import random

#
# TileBoard
# This script is called from a YAML webhook exposed to TileBoard. It will be called when
# Tileboard loads and then at a set interval each time the list of screensaver files has been
# run through. It will update the list of files, shuffle them, and return them to TileBoard.
#
# apps.yaml usage:
# tileboard:
#   module: tileboard
#   class: TileBoard

class TileBoard(hass.Hass):

	def initialize(self):
		self.throttle_timer = None
		self.listen_event(self.tb_throttle, "tb_update")
		
	def tb_throttle(self, event_name, data, kwargs):
		#throttle function to ensure that we don't have a race condition
		#will wait until webhook hasn't been called in one minute before updating slides
		self.cancel_timer(self.throttle_timer)
		self.throttle_timer = self.run_in(self.tb_update, 60)

	def tb_update(self, kwargs):
		#update the list of files, randomize, and transmit back to tileboard
		self.list_dir = []
		self.slides = []
		self.list_dir = os.listdir("/config/www/tileboard/images/screensaver")
		for file in self.list_dir:
			if file.endswith(".jpg") or file.endswith(".jpeg"):
				self.slides.append(file)
		random.shuffle(self.slides)
		self.fire_event("tileboard", command="ss_update", slides=self.slides)