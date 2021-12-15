# From the tutorial: "Ben, how do I expression-link Pulldown Knobs?"
# https://youtu.be/dDgMDL4bQSw

# Link Transform2's filter knob to Transform1's filter knob.
nuke.toNode('Transform2').knob('filter').setExpression('Transform1.filter')

# If Transform3's scale knob has a value greater than 1, set its filter to "Simon". Otherwise, use "Cubic".
nuke.toNode('Transform3').knob('filter').setExpression('scale > 1 ? 3 : 1')

# Programatically remove all animation / expression-links from Transform3's filter knob.
nuke.toNode('Transform3').knob('filter').clearAnimated()
