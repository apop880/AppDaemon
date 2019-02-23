import appdaemon.plugins.hass.hassapi as hass

#
# STButton
#
# Args:
#  -button_name
#  -tap_action: toggle, brightness, color
#  -tap_device:
#  -tap_colors (optional)
#  -hold_action: toggle, brightness, color
#  -hold_device:
#  -hold_colors (optional)
#  -double_action: toggle, brightness, color
#  -double_device:
#  -double_colors (optional)

class STButton(hass.Hass):

	def initialize(self):
		#initialize any color loops
		self.tap_index = 0
		self.hold_index = 0
		self.double_index = 0
		if "tap_colors" in self.args:
			self.tap_colors = self.split_device_list(self.args["tap_colors"])
		if "hold_colors" in self.args:
			self.hold_colors = self.split_device_list(self.args["hold_colors"])
		if "double_colors" in self.args:
			self.double_colors = self.split_device_list(self.args["double_colors"])
		#listen for button events
		self.listen_event(self.button_event, "smartthings.button", value="pushed", name=self.args["button_name"], action = "tap_action", device = "tap_device")
		self.listen_event(self.button_event, "smartthings.button", value="held", name=self.args["button_name"], action = "hold_action", device = "hold_device")
		self.listen_event(self.button_event, "smartthings.button", value="double", name=self.args["button_name"], action = "double_action", device = "double_device")
		
	def button_event(self, event_name, data, kwargs):
		if self.args[kwargs["action"]] == "toggle":
			light = self.get_state(self.args[kwargs["device"]])
			if light == "off":
				self.turn_on(self.args[kwargs["device"]], brightness_pct=60, kelvin=2700)
				self.tap_index = 0
				self.hold_index = 0
				self.double_index = 0
			else:
				self.turn_off(self.args[kwargs["device"]])
		if self.args[kwargs["action"]] == "brightness":
			light = self.get_state(self.args[kwargs["device"]], attribute="brightness")
			if light != None and light < 128:
				self.turn_on(self.args[kwargs["device"]], brightness_pct=60)
			elif light != None and light >= 128:
				self.turn_on(self.args[kwargs["device"]], brightness_pct=15)
		if self.args[kwargs["action"]] == "color":
			if kwargs["action"] == "tap_action":
				self.tap_index += 1
				if self.tap_colors[self.tap_index % len(self.tap_colors)] == "white":
					self.turn_on(self.args[kwargs["device"]], kelvin=2700)
				else:
					self.turn_on(self.args[kwargs["device"]], color_name=self.tap_colors[self.tap_index % len(self.tap_colors)])
			if kwargs["action"] == "hold_action":
				self.hold_index += 1
				if self.hold_colors[self.hold_index % len(self.hold_colors)] == "white":
					self.turn_on(self.args[kwargs["device"]], kelvin=2700)
				else:
					self.turn_on(self.args[kwargs["device"]], color_name=self.hold_colors[self.hold_index % len(self.hold_colors)])
			if kwargs["action"] == "double_action":
				self.double_index += 1
				if self.double_colors[self.double_index % len(self.double_colors)] == "white":
					self.turn_on(self.args[kwargs["device"]], kelvin=2700)
				else:
					self.turn_on(self.args[kwargs["device"]], color_name=self.double_colors[self.double_index % len(self.double_colors)])