#!/usr/bin/env python3

# Combines a keyboard and IBM trackpoint device into a single, virtual UInput
# device, filtering some keys and remapping others.
#
# The idea is to use the hard-keys in the trackpoint (typically above the
# trackpad on thinkpads) as modifier keys like shift, alt, ctrl, etc. to avoid
# straining pinky fingers while getting more use out of thumbs.
#
# The ability to disable some keys from the keyboard itself is useful as a
# learning tool, to force the user to adjust.
#
# This can also support remappings typically achieved in XOrg, but with the
# nice property that this should work anywhere (not tested, but at least
# virtual terminals and Wayland come to mind). As an example, the mapping of
# RIGHTALT to LEFTMETA below is useful for the thinkpad to make a window
# manager's mod key easier to reach.

from typing import Sequence, Mapping, List
from evdev import InputDevice, list_devices, UInput, ecodes as e
from asyncio import get_event_loop, ensure_future

# Names of devices to grab (i.e. take exclusive access to) and combine into a
# single UInput device with the sum of their capabilities.
NAMES = ['TPPS/2 IBM TrackPoint', 'AT Translated Set 2 keyboard']
# Keys to filter out, i.e. these event codes originating from a grabbed device
# will be ignored rather than being forwarded to the UInput device.
DISABLED = [
    e.KEY_LEFTSHIFT,
    e.KEY_RIGHTSHIFT,
    e.KEY_LEFTCTRL,
    e.KEY_RIGHTCTRL,
    e.KEY_ENTER,
    e.KEY_CAPSLOCK]
# Keys to remap, i.e. if an event code from a grabbed device has an entry in
# this mapping, the code is updated to the corresponding value before the event
# is forwarded to the UInput device.
MAPPING = {
    e.BTN_LEFT: e.KEY_LEFTSHIFT,
    e.BTN_RIGHT: e.KEY_LEFTCTRL,
    e.BTN_MIDDLE: e.KEY_ENTER,
    e.KEY_RIGHTALT: e.KEY_LEFTMETA,
}


def find_devices_by_names(names: Sequence[str]) -> List[InputDevice]:
    """Find devices by the evdev InputDevice name attributes."""
    devices = []
    for path in list_devices():
        device = InputDevice(path)
        if device.name in names:
            devices.append(device)
    return devices


async def translate_input(device: InputDevice, ui: UInput, disabled: Sequence[int], mapping: Mapping[int, int]) -> None:
    """Read inputs from device, filter out disabled, apply mapping, and write to ui."""
    async for ev in device.async_read_loop():
        if ev.type == e.EV_KEY:
            if ev.code in disabled:
                continue
            if ev.code in mapping:
                ev.code = mapping[ev.code]
        ui.write_event(ev)
        ui.syn()


def main() -> None:
    devices = find_devices_by_names(NAMES)
    with UInput.from_device(*devices, name='trackpoint-keyboard') as ui:
        for device in devices:
            device.grab()
            ensure_future(translate_input(device, ui, DISABLED, MAPPING))
        get_event_loop().run_forever()


if __name__ == '__main__':
    main()
