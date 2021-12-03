# From the tutorial: "Ben, how do I use $gui when rendering locally?"
# https://youtu.be/Axb1zP0cvO8

# Add this code to your menu.py.

def toggle_nuke_executing():

    # Add the Python expression to the knob.
    nuke.thisKnob().setExpression('[python {nuke.executing()}]')

    # It is courteous to label nodes with dynamically-changing knobs, for other Compositors
    # who might have to open up, and work with your Nuke script...
    font = nuke.thisNode().knob('note_font').value()
    nuke.thisNode().knob('note_font').setValue(font+' Bold')
    nuke.thisNode().knob('label').setValue("nuke.executing() on this node")

# Add a menu item to any knob's right-click menu.
nuke.menu('Animation').addCommand('Add nuke.executing() to knob', 'toggle_nuke_executing()')
