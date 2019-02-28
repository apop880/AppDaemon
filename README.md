# AppDaemon
My AppDaemon Apps

This is a repository of my AppDaemon apps for Home Assistant. I'll add apps periodically that I think may be useful to the broader community.

Jump to: [STButton](#stbutton)

## <a name="stbutton"></a>STButton
### Version 1 Published 2/23/19
This application is a handler for SmartThings Button events. You must have the SmartThings Integration configured in Home Assistant.

The application can handle single taps, double taps, and hold actions and can currently do one of three things:

* Toggle: Toggles a light or light group. If the light supports color temperature, it will set a default color temperature of 2700K.
* Brightness: Will adjust the brightness of a light or group of lights.
If the light is currently brighter than 50%, it will change to 15%, otherwise it will change to 60%.
* Color: Will cycle through a defined list of color names.

Here's an example of using the app in your apps.yaml file:

```yaml
bar_button:
  module: stbutton #should not change
  class: STButton #should not change
  button_name: "Bar Button" #name of the SmartThings button
  tap_action: toggle #action to take when the button is pressed (toggle, brightness, or color)
  tap_device: light.bar #device to take the tap action on - should only be one light device listed but can be a group of lights
  hold_action: brightness #same as above but for when the button is held
  hold_device: light.bar #same as above but for when the button is held
  double_action: color #same as above but for when the button is double tapped
  double_device: light.bar #same as above but for when the button is double tapped
  double_colors: white,blue,red,green #only required if the action field is "color" - list of colors to cycle through
  ```
  
  The example above should be fairly self-explanatory. If you choose to use tap or hold to change colors, you would also need a
  tap_colors or hold_colors in your YAML.
  
  Feel free to let me know if you have any questions or would like to request any additional functionality! I started it pretty simple
  to meet the things I needed it for and replicate my previous SmartThings setup, but there are a number of additional things that could be added.
