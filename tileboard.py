import appdaemon.plugins.hass.hassapi as hass
import os, os.path
import random
import datetime

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
#   slidesTimeout: 30
#   dailyRefresh: true (optional)

class TileBoard(hass.Hass):

	def initialize(self):
		self.throttle_timer = None
		self.update_timer = None
		self.listen_event(self.tb_throttle, "tb_update")
		self.run_in(self.tb_update, 5)

		#set up daily refresh listener if defined in configuration
		if "dailyRefresh" in self.args:
			#refresh daily at 3am
			runtime = datetime.time(3, 0, 0)
			self.run_daily(self.daily_refresh, runtime)
		
	def tb_throttle(self, event_name, data, kwargs):
		#throttle function to ensure that we don't have a race condition
		#will wait until webhook hasn't been called in one minute before updating slides
		self.cancel_timer(self.throttle_timer)
		self.cancel_timer(self.update_timer)
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
		self.update_timer = self.run_in(self.tb_update, len(self.slides) * self.args["slidesTimeout"])

	def daily_refresh(self, kwargs):
		self.fire_event("tileboard", command="refresh")
