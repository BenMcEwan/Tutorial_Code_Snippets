# --------------------------------------------------------------
#  example_auto_bbox
#  Version: 0.1.1
#  Last Updated: February 21st, 2022
# --------------------------------------------------------------

# --------------------------------------------------------------
# TO DO
# - Add AutoCrop nodes above right-angle dots.
# --------------------------------------------------------------

import nuke
import nukescripts

def auto_bbox(speed, overscan_percentage):
    """
    Scrapes a Nuke script, and automatically crops Merge nodes' A-pipes when the incoming bbox is larger than the project's format + overscan.
    """

    # Ask the user for overscan, or quit if they choose "cancel"
    try:
        overscan = float(nuke.getInput("How much overscan (%) should I account for?", str(overscan_percentage)))
    except:
        return

    # 10% overscan will == 5% on either side...
    overscan = overscan/2

    first_frame = nuke.root().knob('first_frame').value()
    last_frame = nuke.root().knob('last_frame').value()
    middle_frame = first_frame+((last_frame-first_frame)/2)
    frame_count = 0

    # Start by deselecting any selected nodes.
    if nuke.selectedNodes() != []:
        for selected_nodes in nuke.selectedNodes():
            selected_nodes.setSelected(False)

    # Find the project's format + overscan
    format_x = nuke.root().width()*overscan/100*-1
    format_y = nuke.root().height()*overscan/100*-1
    format_w = nuke.root().width()+(nuke.root().width()*overscan/100)
    format_h = nuke.root().height()+(nuke.root().height()*overscan/100)



    # Print a string to kick out a user-friendly log of what's happening...
    print("\n\n\n###########   AUTO BBOX RESULTS   ###########")



    # Look at all Merge nodes...
    for i in nuke.allNodes('Merge2'):

        # If the merge node has a 'mask' or 'stencil' operation, set the bbox appropriately.
        if i.knob('operation').value() == "mask" and i.knob('bbox').value() != "A":
            i.knob('bbox').setValue("A")
            print(i.name()+" is set to mask, and is pulling in too much data from the B pipe. Using bbox from A...")

        elif i.knob('operation').value() == "stencil" and i.knob('bbox').value() != "B":
            i.knob('bbox').setValue("B")
            print(i.name()+" is set to stencil, and is pulling in too much data from the A pipe. Using bbox from B...")



        # Calculate the bbox of the node connected to Merge nodes' A pipes.
        x = i.input(1).bbox().x()
        y = i.input(1).bbox().y()
        w = i.input(1).bbox().w()+x
        h = i.input(1).bbox().h()+y



        # If the bbox exceeds the format + overscan...
        if x < format_x or y < format_y or w > format_w or h > format_h:

            # ...and if there is already a Crop node, or a node with a label saying "ignore bbox", CROP THAT SHIZ!
            if i.input(1).Class() != "Crop" and "ignore bbox" not in i.input(1).knob('label').value():

                i.input(1).setSelected(True)

                # If the fast option is selected, simply crop to format + overscan.
                if speed == "fast":
                    crop_node = nuke.createNode('Crop')
                    crop_node.knob('label').setValue("AutoCrop (fast)")

                    # Add some overscan to the newly-created crops
                    crop_node.knob('box').setValue(format_x, 0)
                    crop_node.knob('box').setValue(format_y, 1)
                    crop_node.knob('box').setValue(format_w, 2)
                    crop_node.knob('box').setValue(format_h, 3)

                # If the precise option is selected, run nukescripts.autocrop() and add overscan.
                elif speed == "precise":
                    nukescripts.autocrop()

                    # Add some overscan to the newly-created crops
                    for crop_node in nuke.allNodes('Crop'):
                        if crop_node.knob('label').value() == "AutoCrop":
                            crop_node.knob('box').setExpression('curve+'+str(format_x), 0)
                            crop_node.knob('box').setExpression('curve+'+str(format_y), 1)
                            crop_node.knob('box').setExpression('curve-'+str(format_x), 2)
                            crop_node.knob('box').setExpression('curve-'+str(format_y), 3)

                i.input(1).setSelected(False)

                # Move the Merge node to be in line with the crop.
                # nuke.autoplace(i)
                # i.knob('ypos').setValue(i.input(1).knob('ypos').value())

                print(i.name()+"'s A pipe has an oversized bbox. Autocropping...")



# Add menu items
nuke.menu("Nuke").addCommand("Utilities/Optimize bbox (fast)", 'example_auto_bbox.auto_bbox("fast", 10)')
nuke.menu("Nuke").addCommand("Utilities/Optimize bbox (precise + slow)", 'example_auto_bbox.auto_bbox("precise", 10)')
