# Home Assistant Add-on: Hailo-10H for Frigate (Full Access)

![Supports aarch64 Architecture][aarch64-shield]

Hailo-10H AI accelerator support for Frigate NVR — realtime local object detection for IP cameras.

This is a community add-on based on the official [Frigate](https://frigate.video) Docker image (MIT licensed).
It replaces HailoRT 4.x with HailoRT 5.2.0 for Hailo-10H support. Not affiliated with or endorsed by Frigate, Inc.

You must create a config file as `config.yml` in your add-on configuration folder.

This version of the add-on requests full device access in order to turn off
protection mode for the Hailo device.

[Documentation](https://docs.frigate.video)

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
