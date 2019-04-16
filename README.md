# AppDaemon
My AppDaemon Apps

This is a repository of my AppDaemon apps for Home Assistant. I'll add apps periodically that I think may be useful to the broader community.

Jump to: [STButton](#stbutton) | [TileBoard](#tileboard)

## <a name="stbutton"></a>STButton
### Version 2 Published 4/15/19
This application is a handler for SmartThings Button events. This works with either the SmartThings Integration or ZHA integration.

The application can handle single taps, double taps, and hold actions and can currently do one of three things:

* Toggle: Toggles a light or light group. If the light supports color temperature, it will set a default color temperature of 2700K. Currently toggle only supports lights, but supporting other entities is on the roadmap.
* Brightness: Will adjust the brightness of a light or group of lights.
If the light is currently brighter than 50%, it will change to 15%, otherwise it will change to 60%.
* Color: Will cycle through a defined list of color names.

Here's an example of using the app in your apps.yaml file:

```yaml
bar_button:
  module: stbutton #should not change
  class: STButton #should not change
  #use one of the following two, not both
  button_name: "Bar Button" #name of the SmartThings button
  device_ieee: "00:00:00:00:00:00:00:00" #ZHA device_ieee
  tap_action: toggle #action to take when the button is pressed (toggle, brightness, or color)
  tap_device: light.bar #device to take the tap action on - should only be one light device listed but can be a group of lights
  hold_action: brightness #same as above but for when the button is held
  hold_device: light.bar #same as above but for when the button is held
  double_action: color #same as above but for when the button is double tapped
  double_device: light.bar #same as above but for when the button is double tapped
  double_colors: white,blue,red,green #only required if the action field is "color" - list of colors to cycle through
  ```
  **ZHA support is new in version 2, but the YAML otherwise is functionally the same. If you're using SmartThings integration, define the button_name. Otherwise, define the device_ieee for ZHA.**
  
  Otherwise, the example above should be fairly self-explanatory. If you choose to use tap or hold to change colors, you would also need a
  tap_colors or hold_colors in your YAML.
  
  Feel free to let me know if you have any questions or would like to request any additional functionality! I started it pretty simple
  to meet the things I needed it for and replicate my previous SmartThings setup, but there are a number of additional things that could be added.
  
  ## <a name="tileboard"></a>TileBoard
### Version 2 Published 3/13/19 (See below for breaking changes)
This is a set of helper functions for the excellent TileBoard webapp. Primarily, this app makes it easy to have a photo screensaver that is constantly updated and randomized. The setup in apps.yaml is fairly self explanatory:

```yaml
tileboard:
  module: tileboard
  class: TileBoard
  #Breaking change in v2 - specify the length each slide is displayed for, in seconds, as defined in config.js
  slidesTimeout: 30
  #optional: schedule a daily refresh of TileBoard at 3am
  dailyRefresh: true
```

You will need to include two other pieces. In automations.yaml, add the following:

```yaml
- alias: 'Tileboard Webhook'
  trigger:
    platform: webhook
    webhook_id: tb_update
  action:
    event: tb_update
```

This creates a webhook that TileBoard can call to trigger the AppDaemon script. Eventually, I plan to phase this piece out and call the AppDaemon API directly, but that API doesn't currently support CORS so the YAML automation webhook must act as the middleman. Now, in the events portion of your TileBoard config.js, add the following:

```javascript
{
	command: 'ss_update',
	action: function(e) {
		CONFIG.screensaver.slides.length = 0;
		for (i = 0; i < e.slides.length; i++) {
			file = "images/screensaver/" + e.slides[i];
			CONFIG.screensaver.slides.push({
				bg: file
			});
		}
	}
}
```

Then, at the very bottom of config.js, add the following:

```javascript
var webhook_endpoint = CONFIG.serverUrl + "/api/webhook/tb_update";

var xhttp = new XMLHttpRequest;
xhttp.open("POST", webhook_endpoint, true);
xhttp.send();
```

The webhook will be called when TileBoard first loads or is refreshed. That will execute the AppDaemon script, which gets a list of all of the photos for the screensaver. **The files must be in an images/screensaver folder under tileboard.** The script is currently only configured to look in this folder, which you will have to create initially. It will look for any files with a .jpg or .jpeg extension, shuffle that list of files, and send it back to TileBoard. New in version 2, this is the only time TileBoard initiates the call to AppDaemon. From then on, AppDaemon will automatically attempt to send the update list of slides to TileBoard each time the list of photos has been gone through, so that any new photos in the folder can be picked up, and the photos can be randomized again. **To accommodate this, take note of the breaking change to apps.yaml listed above.** The ```slidesTimeout``` line must be configured and should match what is in TileBoard's config.js.

Also new in version 2 is an additional helper function to automatically refresh TileBoard at 3am daily. Running TileBoard on a Kindle Fire in Fully Kiosk, I notice that Fully tends to crash every few days. My hope is that by scheduling a refresh each night, it will clear out any leftover connections and data, and the fresh start each day will reduce the number of crashes. This functionality can be turned on optionally by including the ```dailyRefresh``` line in the apps.yaml configuration. You will also need to add the following code to the events portion of config.js:

```javascript
{
	command: 'refresh',
	action: function(e) {
		window.location.reload();
	}
}
```

I may implement additional helper functions in the future and am open to suggestions.
