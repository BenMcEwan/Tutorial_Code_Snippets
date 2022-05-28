# From the tutorial: "Ben, how do I use topnode in my Python scripts?"
# https://youtu.be/Yj_ySBOBYKE

topnode_name = nuke.tcl("full_name [topnode %s]" % nuke.selectedNode().name())
topnode = nuke.toNode(topnode_name)
print(topnode.name())
