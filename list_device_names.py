#!/usr/bin/env python3

from evdev import InputDevice, list_devices
print('\n'.join([InputDevice(path).name for path in list_devices()]))
