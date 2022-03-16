# Code snippets from the tutorial: "Ben, how do I add icons to different areas in Nuke?"
#https://youtu.be/BslQGEOgJ74



# HTML for adding an icon in a node's label, and changing its size.
<img src="Blur.png" width="100">

# Add an icon to a node's hidden "icon" knob, so that the icon scales with the zoom level of the node.
nuke.selectedNode()['icon'].setValue("Blur.png")



# Add "Display Image in Node Graph" item in Nuke's Edit menu.
# This will create a StickyNote the same colour as your node graph, and add a selected image to it.

# Add this code to your menu.py.

def create_gui_image():

    # Get the filename of the image.
    img_path = nuke.getFilename("Path to Image")

    # Create a StickyNote node, set its colour to the Node Graph's Background Colour,
    # and add the HTML + image's filepath to the node's label.
    img = nuke.createNode('StickyNote')
    img.knob("tile_color").setValue(nuke.toNode('preferences').knob("DAGBackColor").value())
    img.knob('label').setValue("<img src='{x}' width='50'>".format(x=img_path))

# Add a menu item to the Edit menu.
nuke.menu('Nuke').addCommand('Edit/Display Image in Node Graph', 'create_gui_image()')



# Add Menu with icon.
benmcTools = nuke.menu('Nodes').addMenu('BenMc', icon="bm_icon.png")

# Add Menu item to previously-created menu with icon.
benmcTools.addCommand('bm_OpticalGlow', 'nuke.createNode("bm_OpticalGlow")', icon="bm_OpticalGlow_icon.png")
