# trackpoint-keyboard

Combines a keyboard and IBM trackpoint device into a single, virtual UInput
device, filtering some keys and remapping others.

The idea is to use the hard-keys in the trackpoint (typically above the
trackpad on thinkpads) as modifier keys like shift, alt, ctrl, etc. to avoid
straining pinky fingers while getting more use out of thumbs.

The ability to disable some keys from the keyboard itself is useful as a
learning tool, to force the user to adjust.

This can also support remappings typically achieved in XOrg, but with the
nice property that this should work anywhere (not tested, but at least
virtual terminals and Wayland come to mind). As an example, the mapping of
RIGHTALT to LEFTMETA below is useful for the thinkpad to make a window
manager's mod key easier to reach.
