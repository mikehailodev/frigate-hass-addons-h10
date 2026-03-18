# Home Assistant Add-on: Frigate (Full Access) — Hailo-10H

![Supports aarch64 Architecture][aarch64-shield]

NVR with realtime local object detection using **Hailo-10H** AI accelerator.

This is a patched version of the official Frigate add-on that replaces
HailoRT 4.x with HailoRT 5.2.0 for Hailo-10H support.

You must create a config file as `config.yml` in your add-on configuration folder.

This version of the add-on requests full device access in order to turn off
protection mode for the Hailo device.

[Documentation](https://docs.frigate.video)

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
