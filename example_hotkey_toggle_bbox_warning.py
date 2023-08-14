# Put this code in your menu.py.

# Always import the nuke module in your menu.py, if you haven't already.
import nuke

# Define the function to run when you click a menu item / use the hotkey.
def bbox_warning_toggle():

    # Save the knob in preferences as a variable    .
    knob = nuke.toNode('preferences').knob('boundingBoxWarning')
    
    # If the checkbox is unchecked, then check it. Otherwise, if it's checked, uncheck it.
    if knob.value() == False:
        knob.setValue(True)
    else:
        knob.setValue(False)

# Add item to the Edit menu, with an alt+shift+b hotkey.
nuke.menu('Nuke').addCommand('Edit/Toggle BBOX warning', 'bbox_warning_toggle()', "alt+shift+b")
